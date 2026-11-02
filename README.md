<div align="center">

# 🫀 WiFi Vital Signs Radar (CSI Heartbeat & Respiration Monitor)

**Non-Invasive, Contactless Cardiopulmonary Tracking using 2.4 GHz WiFi Channel State Information (CSI) with NodeMCU & ESP32**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![ESP32](https://img.shields.io/badge/Hardware-ESP32%20%7C%20NodeMCU-red.svg?logo=espressif&logoColor=white)](https://espressif.com)
[![Protocol](https://img.shields.io/badge/Protocol-802.11n%20CSI%20%40%2080Hz-green.svg)](https://en.wikipedia.org/wiki/Channel_state_information)
[![GUI](https://img.shields.io/badge/GUI-PyQt5%20%2B%20PyQtGraph-purple.svg)](https://pyqtgraph.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🌟 Highlights & Experimental Validation

In live testing against a commercial medical fingertip pulse sensor:
- **Physical Sensor Ground Truth:** **64 BPM**
- **WiFi CSI Radar Measurement:** **65 BPM**
- **Absolute Error:** **$\pm 1\text{ BPM}$ (~98.5% Accuracy)**
- **Signal Quality Index (SQI):** **$> 90\%$** in live indoor environment with active campus WiFi routers and ceiling fans.

---

## 📖 Overview

Traditional vital signs monitoring requires intrusive contact-based sensors (ECG adhesive electrodes or tight PPG finger clips) which cause skin irritation and easily detach during sleep. 

This project implements a completely **contactless vital signs radar** using standard, commercial IoT microcontrollers:
1. **Transmitter (NodeMCU ESP8266):** Emits high-rate (80 Hz) broadcast packets at maximum hardware RF output power (+20.5 dBm) on WiFi Channel 11.
2. **Receiver (ESP32):** Captures physical-layer **Channel State Information (CSI)** on incoming packets via Espressif hardware callbacks (`esp_wifi_set_csi_rx_cb`).
3. **Host PC (Python):** Demodulates 16 OFDM subcarrier amplitudes, filters room and ceiling fan noise, separates respiration and cardiac signals, and plots real-time biometrics at 60 FPS.

---

## 🔬 How It Works (Theoretical Physics)

```
                       FIRST FRESNEL ZONE (FFZ) GEOMETRY

         [ NodeMCU TX ]                             [ ESP32 RX ]
        (On Power Bank)                          (Plugged into PC)
              [■]                                         [■]
               |                                           |
               | <───────────── 80 cm to 1.0 m ──────────> |
               \                                           /
                \                                         /
                 \             (  SUBJECT SEATED  )      /
                  \            ( Chest Level 1.0m )      /
                   \           ( Hands Resting    )     /
                    \                  |                /
                     ------------------+-----------------
                                  30 to 50 cm
```

- **Wavelength:** At $f_c = 2.462\text{ GHz}$ (WiFi Channel 11), $\lambda \approx 12.18\text{ cm}$.
- **Chest Motion:**
  - Respiration: 5 mm to 12 mm displacement $\implies \Delta \phi \approx 30^\circ - 70^\circ$.
  - Heartbeat (Ballistocardiogram): 0.1 mm to 0.5 mm displacement $\implies \Delta \phi \approx 1.2^\circ - 5.0^\circ$.
- **Phase Modulation:**
  $$\Delta \phi(t) = \frac{4\pi}{\lambda} \left[ d_{\text{resp}}(t) + d_{\text{cardiac}}(t) \right]$$
- **Digital Signal Processing Pipeline:**
  - **Dynamic Sampling Rate:** Automatically tracks packet arrival interval to tune digital filters.
  - **Common-Mode Noise Rejection:** Computes median across subcarriers to cancel room flicker and ceiling fan vibration.
  - **Respiration Bandpass Filter:** 2nd-order Butterworth ($0.10 - 0.45\text{ Hz}$).
  - **Cardiac Bandpass Filter:** 3rd-order Butterworth ($0.80 - 2.00\text{ Hz}$) with respiration component cancellation.
  - **Welch Power Spectral Density (PSD):** Extracts sharp spectral peaks for real-time BPM and RPM estimation.

---

## ⚡ Quickstart Guide

### 1. Requirements
- 1x **NodeMCU (ESP8266)** or 2nd ESP32
- 1x **ESP32 Dev Module**
- 2x Micro-USB cables
- Python 3.10+ on Windows / Linux / macOS

```powershell
pip install pyserial pyqtgraph PyQt5 numpy scipy esptool
```

### 2. Flashing the Boards (1-Click)
Pre-compiled binaries are ready in `bin/`:
- **Flash NodeMCU (TX):** Double-click `flash_nodemcu_tx.bat` (select COM port).
- **Flash ESP32 (RX):** Double-click `flash_rx.bat` (select COM port).

### 3. Running the Live Dashboard
```powershell
# Double-click run_gui.bat or execute:
python gui\live_monitor.py
```
1. Select **Mode: Live ESP32 Hardware**.
2. Select your **ESP32 COM Port**.
3. Click **Connect Hardware**.
4. Sit 40 cm in front of the controllers and watch live pulse waves appear!

---

## 📊 Experimental Results

| Test Scenario | Finger Sensor (Ground Truth) | WiFi CSI Radar | Absolute Error | Relative Error | Signal Quality (SQI) |
|---|---|---|---|---|---|
| **Resting Normal (Trial 1)** | **64.0 BPM** | **65.0 BPM** | **1.0 BPM** | **1.56%** | **94.2%** |
| Resting Normal (Trial 2) | 71.0 BPM | 72.4 BPM | 1.4 BPM | 1.97% | 93.5% |
| Resting Normal (Trial 3) | 68.0 BPM | 69.5 BPM | 1.5 BPM | 2.20% | 95.0% |
| Apnea (Breath-Holding) | 65.0 BPM | 66.0 BPM | 1.0 BPM | 1.53% | 92.0% |
| Post-Exercise (Elevated) | 96.0 BPM | 98.4 BPM | 2.4 BPM | 2.50% | 89.5% |

---

## 📁 Repository Structure

```
WIFI_HEARTBEAT/
│
├── WiFi_CSI_Vital_Signs_Research_Paper.pdf  # Ready-to-submit Academic Research Paper
├── bin/                                     # Pre-compiled binaries for fast flashing
│   ├── nodemcu_tx/                          # ESP8266 NodeMCU firmware
│   ├── tx/                                  # ESP32 Transmitter firmware
│   └── rx/                                  # ESP32 Receiver CSI firmware
│
├── firmware/                                # Source code for Arduino / PlatformIO
│   ├── nodemcu_tx/                          # ESP-NOW high-power beacon (+20.5 dBm)
│   ├── esp32_tx/                            # ESP32 beacon
│   └── esp32_rx/                            # ESP32 hardware CSI demodulator
│
├── gui/                                     # Host PC Application
│   ├── live_monitor.py                      # PyQt5 + PyQtGraph 60 FPS Bio-Radar HUD
│   ├── signal_processor.py                  # DSP Engine (Butterworth, Welch PSD, SQI)
│   └── mock_data_generator.py               # Fallback synthetic CSI simulator
│
├── docs/                                    # Academic Paper & Guides
│   ├── RESEARCH_PAPER_SUBMISSION.md         # Full research paper (Markdown)
│   ├── RESEARCH_PAPER_PRINTABLE.html        # Print-ready HTML paper
│   ├── VIVA_DEFENSE_GUIDE.md                # Top 15 faculty viva questions & answers
│   ├── HARDWARE_SETUP_GUIDE.md              # Physical placement & desk geometry
│   └── LINKEDIN_POST.md                     # Ready-to-copy LinkedIn post
│
├── flash_nodemcu_tx.bat                     # 1-click flasher for NodeMCU
├── flash_rx.bat                             # 1-click flasher for ESP32
├── run_gui.bat                              # 1-click dashboard launcher
└── README.md                                # Project documentation
```

---



---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
