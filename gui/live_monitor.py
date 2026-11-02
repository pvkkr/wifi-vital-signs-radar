"""
WiFi CSI Vital Signs Radar - Live Monitoring & Analytics Dashboard
Built with PyQt5 and PyQtGraph for 60 FPS real-time physiological signal visualization.
"""

import sys
import os

# Add local directory to path for robust imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import csv
from datetime import datetime
import serial
import serial.tools.list_ports
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QGroupBox, QGridLayout,
    QFileDialog, QMessageBox, QFrame, QSplitter
)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor, QPalette

import pyqtgraph as pg

from signal_processor import VitalSignsProcessor
from mock_data_generator import MockCsiGenerator

# Set pyqtgraph styling
pg.setConfigOption('background', '#12151c')
pg.setConfigOption('foreground', '#d0d7de')
pg.setConfigOptions(antialias=True)

class SerialWorker(QThread):
    sample_received = pyqtSignal(int, int, list)
    status_message = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(self, port, baud=115200):
        super().__init__()
        self.port = port
        self.baud = baud
        self.running = False
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1.0)
            self.running = True
            self.status_message.emit(f"Connected to {self.port} at {self.baud} baud.")
            
            while self.running:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line.startswith("CSI,"):
                        parts = line.split(',')
                        if len(parts) >= 6:
                            try:
                                seq = int(parts[1])
                                t_ms = int(parts[2])
                                rssi = int(parts[3])
                                # parts[4] is mean_amp, parts[5:] are subcarriers
                                sc_amps = [float(x) for x in parts[5:]]
                                self.sample_received.emit(t_ms, rssi, sc_amps)
                            except ValueError:
                                pass
                else:
                    time.sleep(0.005)
        except Exception as e:
            self.status_message.emit(f"Serial Error: {e}")
            self.connection_lost.emit()
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def stop(self):
        self.running = False
        self.wait(1000)


class VitalSignsRadarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Vital Signs Radar - CSI Heartbeat & Respiration Monitor")
        self.resize(1320, 840)
        self.setStyleSheet("""
            QMainWindow { background-color: #0b0e14; }
            QLabel { color: #e6edf3; font-family: 'Segoe UI', Arial, sans-serif; }
            QGroupBox { 
                color: #58a6ff; 
                font-weight: bold; 
                border: 1px solid #30363d; 
                border-radius: 8px; 
                margin-top: 10px; 
                padding-top: 12px;
                background-color: #161b22;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 4px; }
            QPushButton { 
                background-color: #21262d; 
                color: #c9d1d9; 
                border: 1px solid #30363d; 
                border-radius: 6px; 
                padding: 6px 14px; 
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #30363d; color: #ffffff; border-color: #8b949e; }
            QPushButton:pressed { background-color: #1f6feb; color: #ffffff; }
            QComboBox { 
                background-color: #21262d; 
                color: #c9d1d9; 
                border: 1px solid #30363d; 
                border-radius: 6px; 
                padding: 4px 10px; 
            }
            QComboBox QAbstractItemView {
                background-color: #161b22;
                color: #e6edf3;
                selection-background-color: #1f6feb;
            }
        """)

        # Core engines
        self.processor = VitalSignsProcessor(fs=80.0, buffer_seconds=12.0)
        self.mock_generator = MockCsiGenerator(fs=80.0)
        self.worker = None
        self.is_recording = False
        self.recorded_data = []

        # Heart pulse animation state
        self.pulse_phase = 0
        self.packet_counter = 0

        self._init_ui()

        # Update timer for GUI rendering (30 FPS)
        self.gui_timer = QTimer()
        self.gui_timer.timeout.connect(self._update_gui)
        self.gui_timer.start(33)

        # Simulation timer for mock mode (80 Hz = 12.5 ms)
        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self._generate_sim_sample)
        
        # Start in Demo Mode by default for instant feedback
        self.mode_combo.setCurrentText("Demo (Simulated)")
        self._toggle_mode()

    def _init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # --- Top Control Bar ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        # Mode Selection
        top_bar.addWidget(QLabel("<b>Mode:</b>"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Demo (Simulated)", "Live ESP32 Hardware"])
        self.mode_combo.currentIndexChanged.connect(self._toggle_mode)
        top_bar.addWidget(self.mode_combo)

        # Demo Scenario
        self.demo_label = QLabel("<b>Scenario:</b>")
        self.demo_combo = QComboBox()
        self.demo_combo.addItems([
            "Normal Breathing (72 BPM, 15 RPM)",
            "Holding Breath (Apnea Test)",
            "Elevated Heart Rate (96 BPM, 21 RPM)",
            "Empty Room (Noise Baseline)"
        ])
        self.demo_combo.currentIndexChanged.connect(self._change_demo_scenario)
        top_bar.addWidget(self.demo_label)
        top_bar.addWidget(self.demo_combo)

        top_bar.addSpacing(15)

        # Hardware COM Port
        self.port_label = QLabel("<b>Port:</b>")
        self.port_combo = QComboBox()
        self._refresh_ports()
        top_bar.addWidget(self.port_label)
        top_bar.addWidget(self.port_combo)

        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.clicked.connect(self._refresh_ports)
        top_bar.addWidget(self.btn_refresh)

        # Connect / Disconnect Button
        self.btn_connect = QPushButton("Connect Hardware")
        self.btn_connect.setStyleSheet("background-color: #238636; color: white;")
        self.btn_connect.clicked.connect(self._toggle_connection)
        top_bar.addWidget(self.btn_connect)

        top_bar.addStretch()

        # Record Session Button
        self.btn_record = QPushButton("⏺ Record Session")
        self.btn_record.clicked.connect(self._toggle_recording)
        top_bar.addWidget(self.btn_record)

        # Status Label
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet("color: #8b949e; font-size: 12px;")
        top_bar.addWidget(self.status_lbl)

        main_layout.addLayout(top_bar)

        # --- Vital Signs HUD Cards ---
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)

        self.card_bpm = self._create_metric_card("HEART RATE", "-- BPM", "❤️ Normal Rhythm", "#ff4d6d")
        self.card_rpm = self._create_metric_card("RESPIRATION", "-- RPM", "🫁 Active Breathing", "#00f0ff")
        self.card_sqi = self._create_metric_card("SIGNAL QUALITY", "-- %", "Fresnel Zone Alignment", "#2ea043")
        self.card_rf = self._create_metric_card("RF METRICS", "CH 11", "Subcarrier #-- | RSSI: -- dBm", "#f0883e")

        cards_layout.addWidget(self.card_bpm)
        cards_layout.addWidget(self.card_rpm)
        cards_layout.addWidget(self.card_sqi)
        cards_layout.addWidget(self.card_rf)

        main_layout.addLayout(cards_layout)

        # --- Waveform Plots Grid ---
        plots_splitter = QSplitter(Qt.Vertical)

        # Upper splitter: Raw CSI and FFT spectrum
        upper_widget = QWidget()
        upper_layout = QHBoxLayout(upper_widget)
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.setSpacing(8)

        # Plot 1: Raw CSI Multi-subcarrier
        self.plot_raw = pg.PlotWidget(title="<b>Raw Channel State Information (CSI Multi-Subcarrier Stream)</b>")
        self.plot_raw.setLabel('left', 'Amplitude')
        self.plot_raw.setLabel('bottom', 'Time (seconds)')
        self.plot_raw.showGrid(x=True, y=True, alpha=0.2)
        self.curve_raw = self.plot_raw.plot(pen=pg.mkPen('#58a6ff', width=1.5))
        upper_layout.addWidget(self.plot_raw, 2)

        # Plot 4: Frequency Spectrum (Welch PSD)
        self.plot_fft = pg.PlotWidget(title="<b>Frequency Spectrum (Welch Power Spectral Density)</b>")
        self.plot_fft.setLabel('left', 'Power (dB/Hz)')
        self.plot_fft.setLabel('bottom', 'Frequency (Hz)')
        self.plot_fft.setXRange(0.0, 2.5)
        self.plot_fft.showGrid(x=True, y=True, alpha=0.2)
        self.curve_fft_resp = self.plot_fft.plot(pen=pg.mkPen('#00f0ff', width=2), name="Resp Band")
        self.curve_fft_card = self.plot_fft.plot(pen=pg.mkPen('#ff4d6d', width=2), name="Cardiac Band")
        upper_layout.addWidget(self.plot_fft, 1)

        plots_splitter.addWidget(upper_widget)

        # Lower splitter: Respiration & Heartbeat Filtered Waves
        lower_widget = QWidget()
        lower_layout = QHBoxLayout(lower_widget)
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.setSpacing(8)

        # Plot 2: Filtered Respiration
        self.plot_resp = pg.PlotWidget(title="<b>Respiration Waveform (0.10 - 0.45 Hz | Thoracic Expansion)</b>")
        self.plot_resp.setLabel('left', 'Displacement (a.u.)')
        self.plot_resp.setLabel('bottom', 'Time (seconds)')
        self.plot_resp.showGrid(x=True, y=True, alpha=0.2)
        self.curve_resp = self.plot_resp.plot(pen=pg.mkPen('#00f0ff', width=2.5))
        lower_layout.addWidget(self.plot_resp)

        # Plot 3: Filtered Cardiac Pulse
        self.plot_cardiac = pg.PlotWidget(title="<b>Cardiac Ballistocardiogram (0.80 - 2.00 Hz | Systolic Micro-Pulse)</b>")
        self.plot_cardiac.setLabel('left', 'Cardiac Pulse (a.u.)')
        self.plot_cardiac.setLabel('bottom', 'Time (seconds)')
        self.plot_cardiac.showGrid(x=True, y=True, alpha=0.2)
        self.curve_cardiac = self.plot_cardiac.plot(pen=pg.mkPen('#ff4d6d', width=2.0))
        lower_layout.addWidget(self.plot_cardiac)

        plots_splitter.addWidget(lower_widget)
        main_layout.addWidget(plots_splitter, 1)

    def _create_metric_card(self, title, default_val, subtitle, accent_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #161b22;
                border: 1px solid #30363d;
                border-top: 3px solid {accent_color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #8b949e; font-size: 11px; font-weight: bold; letter-spacing: 1px;")

        lbl_val = QLabel(default_val)
        lbl_val.setStyleSheet(f"color: {accent_color}; font-size: 28px; font-weight: bold; font-family: 'Consolas', 'Segoe UI';")

        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet("color: #c9d1d9; font-size: 12px;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_sub)
        
        # Keep references to update them
        card.val_label = lbl_val
        card.sub_label = lbl_sub
        return card

    def _refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for p in ports:
            self.port_combo.addItem(f"{p.device} - {p.description}")

    def _toggle_mode(self):
        is_demo = self.mode_combo.currentText().startswith("Demo")
        self.demo_label.setVisible(is_demo)
        self.demo_combo.setVisible(is_demo)
        self.port_label.setVisible(not is_demo)
        self.port_combo.setVisible(not is_demo)
        self.btn_refresh.setVisible(not is_demo)
        self.btn_connect.setVisible(not is_demo)

        if is_demo:
            if self.worker:
                self.worker.stop()
                self.worker = None
                self.btn_connect.setText("Connect Hardware")
                self.btn_connect.setStyleSheet("background-color: #238636; color: white;")
            self.sim_timer.start(12)  # ~80 Hz
            self.status_lbl.setText("Running in Demo Simulation Mode.")
        else:
            self.sim_timer.stop()
            self.status_lbl.setText("Select ESP32 Receiver Port and click Connect.")

    def _change_demo_scenario(self):
        idx = self.demo_combo.currentIndex()
        modes = ["normal", "hold_breath", "elevated", "empty"]
        self.mock_generator.set_mode(modes[idx])

    def _generate_sim_sample(self):
        t_ms, rssi, sc_amps = self.mock_generator.get_sample()
        self._on_sample(t_ms, rssi, sc_amps)

    def _toggle_connection(self):
        if self.worker is None:
            # Connect
            selected = self.port_combo.currentText()
            if not selected:
                QMessageBox.warning(self, "No Port", "Please select an active ESP32 COM port.")
                return
            port = selected.split(' ')[0]
            self.worker = SerialWorker(port=port, baud=115200)
            self.worker.sample_received.connect(self._on_sample)
            self.worker.status_message.connect(self.status_lbl.setText)
            self.worker.connection_lost.connect(self._on_connection_lost)
            self.worker.start()

            self.btn_connect.setText("Disconnect")
            self.btn_connect.setStyleSheet("background-color: #da3633; color: white;")
        else:
            # Disconnect
            self.worker.stop()
            self.worker = None
            self.btn_connect.setText("Connect Hardware")
            self.btn_connect.setStyleSheet("background-color: #238636; color: white;")
            self.status_lbl.setText("Disconnected.")

    def _on_connection_lost(self):
        if self.worker:
            self.worker = None
        self.btn_connect.setText("Connect Hardware")
        self.btn_connect.setStyleSheet("background-color: #238636; color: white;")
        self.status_lbl.setText("Serial connection lost.")

    def _on_sample(self, t_ms, rssi, sc_amps):
        self.packet_counter += 1
        self.processor.add_sample(t_ms, rssi, sc_amps)

        if self.is_recording:
            self.recorded_data.append([t_ms, rssi] + sc_amps)

    def _toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.recorded_data = []
            self.btn_record.setText("⏹ Stop & Save CSV")
            self.btn_record.setStyleSheet("background-color: #da3633; color: white;")
            self.status_lbl.setText("Recording session data...")
        else:
            self.is_recording = False
            self.btn_record.setText("⏺ Record Session")
            self.btn_record.setStyleSheet("")
            
            # Save file
            filename = f"vital_signs_csi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            path, _ = QFileDialog.getSaveFileName(self, "Save Session CSV", filename, "CSV Files (*.csv)")
            if path:
                try:
                    with open(path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        header = ["timestamp_ms", "rssi"] + [f"subcarrier_{i}" for i in range(16)]
                        writer.writerow(header)
                        writer.writerows(self.recorded_data)
                    QMessageBox.information(self, "Session Saved", f"Successfully saved {len(self.recorded_data)} samples to:\n{path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error Saving", f"Failed to save file: {e}")

    def _update_gui(self):
        # Run DSP pipeline
        metrics = self.processor.process()

        # Update HUD Cards
        bpm = metrics["bpm"]
        rpm = metrics["rpm"]
        sqi = metrics["sqi"]
        state = metrics["state"]
        sc_idx = metrics["selected_idx"]

        # Animate Heartbeat Icon
        self.pulse_phase = (self.pulse_phase + 1) % 10
        heart_icon = "❤️" if self.pulse_phase < 5 else "💓"

        if bpm > 0:
            self.card_bpm.val_label.setText(f"{heart_icon} {bpm:.0f} BPM")
            self.card_bpm.sub_label.setText(f"Status: {state}")
        else:
            self.card_bpm.val_label.setText("-- BPM")
            self.card_bpm.sub_label.setText(f"Status: {state}")

        if rpm > 0:
            self.card_rpm.val_label.setText(f"{rpm:.0f} RPM")
            self.card_rpm.sub_label.setText(f"Respiratory cycle: {rpm/60.0:.2f} Hz")
        else:
            self.card_rpm.val_label.setText("-- RPM")
            self.card_rpm.sub_label.setText(f"Status: {state}")

        self.card_sqi.val_label.setText(f"{sqi:.0f} %")
        if sqi >= 70:
            self.card_sqi.sub_label.setText("Signal: Excellent (Strong Peak)")
        elif sqi >= 40:
            self.card_sqi.sub_label.setText("Signal: Moderate (Keep Still)")
        else:
            self.card_sqi.sub_label.setText("Signal: Weak / Align Subject")

        last_rssi = self.processor.rssi_history[-1] if self.processor.rssi_history else -55
        self.card_rf.val_label.setText(f"SC #{sc_idx}")
        self.card_rf.sub_label.setText(f"RSSI: {last_rssi} dBm | Total Pkts: {self.packet_counter}")

        # Update Plots with true physical time duration
        n_pts = len(self.processor.selected_raw)
        if n_pts > 0:
            duration = min(12.0, n_pts / max(1.0, self.processor.current_fs))
            time_axis = np.linspace(-duration, 0.0, n_pts)
        else:
            time_axis = []

        if len(self.processor.selected_raw) > 0:
            self.curve_raw.setData(time_axis, self.processor.selected_raw)

        if len(self.processor.resp_signal) > 0:
            self.curve_resp.setData(time_axis, self.processor.resp_signal)

        if len(self.processor.cardiac_signal) > 0:
            self.curve_cardiac.setData(time_axis, self.processor.cardiac_signal)

        # Frequency Spectrum
        if len(self.processor.freqs_resp) > 0 and len(self.processor.psd_resp) > 0:
            self.curve_fft_resp.setData(self.processor.freqs_resp, 10 * np.log10(self.processor.psd_resp + 1e-6))

        if len(self.processor.freqs_cardiac) > 0 and len(self.processor.psd_cardiac) > 0:
            self.curve_fft_card.setData(self.processor.freqs_cardiac, 10 * np.log10(self.processor.psd_cardiac + 1e-6))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitalSignsRadarApp()
    window.show()
    sys.exit(app.exec_())
