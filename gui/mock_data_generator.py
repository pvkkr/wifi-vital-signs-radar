"""
Physiological WiFi CSI Signal Synthesizer
Generates realistic multi-subcarrier CSI streams simulating:
- Multipath thoracic displacement (breathing)
- Ballistocardiographic micro-displacements (heartbeat)
- Subcarrier spatial phase diversity
- Realistic Gaussian thermal noise and RF fading
"""

import numpy as np
import time

class MockCsiGenerator:
    def __init__(self, fs=80.0):
        self.fs = fs
        self.packet_idx = 0
        self.start_time = time.time()
        self.mode = "normal"  # "normal", "hold_breath", "elevated", "empty"
        
        # Subcarrier sensitivities across 16 subcarriers (spatial diversity)
        # Some subcarriers are near constructive peaks, others near destructive nulls
        np.random.seed(42)
        self.sc_gains_resp = np.array([
            0.4, 0.9, 1.4, 1.1, 0.3, 0.7, 1.5, 0.8,
            0.5, 1.3, 0.2, 0.9, 1.2, 0.6, 1.0, 0.4
        ], dtype=np.float32)
        
        self.sc_gains_card = np.array([
            0.2, 0.5, 0.8, 0.6, 0.1, 0.4, 0.9, 0.5,
            0.3, 0.7, 0.1, 0.5, 0.7, 0.3, 0.6, 0.2
        ], dtype=np.float32)

    def set_mode(self, mode):
        self.mode = mode

    def get_sample(self):
        """
        Generates a synthetic CSI sample simulating physics of chest micro-motion.
        Returns: (timestamp_ms, rssi, [16 subcarrier amplitudes])
        """
        self.packet_idx += 1
        t = self.packet_idx / self.fs
        timestamp_ms = int((time.time() - self.start_time) * 1000)
        
        if self.mode == "empty":
            # No person: only RF background noise
            noise = np.random.normal(0, 0.08, 16)
            sc_amps = (22.0 + noise).tolist()
            rssi = int(-58 + np.random.normal(0, 0.5))
            return timestamp_ms, rssi, sc_amps

        # Define physiological frequencies
        if self.mode == "normal":
            f_resp = 0.25      # 15 breaths/min (0.25 Hz)
            f_card = 1.20      # 72 beats/min (1.20 Hz)
            resp_amp = 1.8
            card_amp = 0.22
        elif self.mode == "hold_breath":
            f_resp = 0.0       # Breath held
            f_card = 1.13      # 68 beats/min
            resp_amp = 0.02    # Minimal baseline drift
            card_amp = 0.28    # Heartbeat becomes much clearer!
        elif self.mode == "elevated":
            f_resp = 0.35      # 21 breaths/min
            f_card = 1.60      # 96 beats/min
            resp_amp = 2.4
            card_amp = 0.30

        # Respiration wave (asymmetric thoracic cycle: faster inhale, slower exhale)
        resp_wave = resp_amp * (np.sin(2 * np.pi * f_resp * t) + 0.2 * np.sin(4 * np.pi * f_resp * t))
        
        # Cardiac ballistocardiogram wave (sharp systolic peak followed by dicrotic notch)
        card_wave = card_amp * (
            np.sin(2 * np.pi * f_card * t) + 
            0.35 * np.sin(4 * np.pi * f_card * t + 0.4) + 
            0.15 * np.sin(6 * np.pi * f_card * t + 0.8)
        )
        
        # Combine across subcarriers with spatial gain & phase variation
        sc_amps = []
        for i in range(16):
            base_dc = 24.0 + (i * 0.5)
            r_gain = self.sc_gains_resp[i]
            c_gain = self.sc_gains_card[i]
            noise = np.random.normal(0, 0.04)
            
            val = base_dc + (r_gain * resp_wave) + (c_gain * card_wave) + noise
            sc_amps.append(round(float(val), 2))
            
        rssi = int(-52 + (resp_wave * 0.4) + np.random.normal(0, 0.3))
        return timestamp_ms, rssi, sc_amps
