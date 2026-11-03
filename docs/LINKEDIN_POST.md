# 🚀 LinkedIn & YouTube Showcase Kit

---

## 📱 Part 1: LinkedIn Post (Ready to Copy & Paste)

Can standard WiFi signals measure your heartbeat without touching your body? 🫀📡

Over the last few days, along with my teammates K. Kamalesh and T. Perumal, I built a completely contactless biometric radar using off-the-shelf microcontrollers: one **NodeMCU (ESP8266)** and one **ESP32**, running on standard **2.4 GHz WiFi (IEEE 802.11n)**!

In our live validation test comparing against a physical fingertip pulse sensor:
👉 **Physical Pulse Sensor:** 64 BPM  
👉 **WiFi CSI Radar:** 65 BPM  
🎯 **Difference: Only 1 BPM (~98.5% accuracy)!**

### 💡 How It Works (The Science):
Every time our heart beats, it creates subtle mechanical chest-wall micro-movements of just 0.2 mm to 0.5 mm (ballistocardiogram). 

1. **Transmitter (NodeMCU):** Emits high-rate (80 Hz) broadcast packets at +20.5 dBm on WiFi Channel 11.
2. **RF Multipath Modulation:** As the 2.4 GHz electromagnetic carrier waves (λ ≈ 12.2 cm) pass across the First Fresnel Zone, chest wall micro-motion causes periodic phase shifts (Δϕ = 4π/λ · Δd).
3. **Receiver (ESP32):** Captures physical-layer **Channel State Information (CSI)** across 16 active OFDM subcarriers.
4. **Digital Signal Processing Pipeline (Python):** 
   - Dynamically selects the most sensitive subcarriers using variance ranking.
   - Rejects ambient common-mode room flicker and ceiling fan noise.
   - Extracts respiration via a 0.10–0.45 Hz bandpass filter.
   - Isolates cardiac pulse via respiration cancellation + 0.80–2.00 Hz Butterworth filtering.
   - Computes Welch Power Spectral Density (PSD) to extract real-time BPM and RPM.

### 🛠️ Challenges Overcome:
Testing in a live university hostel room presented real RF noise:
- Room WiFi router congestion on 2.4 GHz was eliminated by enforcing hard RSSI noise gating (> -80 dBm).
- Spinning ceiling fan vibrations were suppressed through multi-subcarrier median subtraction.

The real-time dashboard is built using **PyQt5 + PyQtGraph**, running at a smooth 60 FPS.

👥 **Project Team (KL University):**
- **P. Venkata Kishor Kumar Reddy** (Lead / Project Creator)
- **K. Kamalesh** (Co-Developer)
- **T. Perumal** (Co-Developer)

💻 **Full Open-Source Code & Research Paper:** https://lnkd.in/drVB6jqX  
*(GitHub: https://github.com/pvkkr/wifi-vital-signs-radar)*

What are your thoughts on using ambient RF signals for non-invasive telemedicine and sleep monitoring?

#IoT #EmbeddedSystems #ESP32 #NodeMCU #WirelessSensing #SignalProcessing #Python #DSP #BiomedicalEngineering #HealthTech #Innovation #KLUniversity #Telehealth #Engineering

---

## 🎥 Part 2: YouTube Video Details

When uploading your proof video to YouTube, copy and paste this:

### 📌 Video Title:
```
Contactless Heartbeat & Respiration Detection Using WiFi (ESP32 & NodeMCU) | 64 vs 65 BPM Proof!
```

### 📝 Video Description:
```
In this video, we demonstrate a contactless vital signs radar that measures heart rate and respiration rate using 2.4 GHz WiFi Channel State Information (CSI) with just a NodeMCU (ESP8266) transmitter and an ESP32 receiver.

Watch the side-by-side comparison between a physical finger pulse sensor and our WiFi CSI Radar:
- Ground Truth Pulse Sensor: 64 BPM
- WiFi CSI Radar: 65 BPM
- Accuracy: ~98.5% (Only 1 BPM difference!)

🚀 Full Source Code, Pre-compiled Binaries & Academic Paper:
👉 https://github.com/pvkkr/wifi-vital-signs-radar

👥 Project Team:
- P. Venkata Kishor Kumar Reddy (Lead)
- K. Kamalesh
- T. Perumal

🛠️ Tech Stack:
- Hardware: ESP32 Dev Module, NodeMCU (ESP-12E / ESP8266)
- Protocol: IEEE 802.11n WiFi CSI @ 80 Hz on Channel 11 (ESP-NOW broadcast)
- Signal Processing: Python, SciPy, Butterworth Bandpass Filtering, Welch PSD
- GUI: PyQt5 & PyQtGraph (60 FPS real-time rendering)

Academic Affiliation:
Department of ECE / CSE, Koneru Lakshmaiah Education Foundation (KL University), A.P., India.

#WiFiCSI #ESP32 #NodeMCU #Heartbeat #IoT #SignalProcessing #Python #KLUniversity
```

### 🏷️ YouTube Tags:
```
WiFi CSI, ESP32, NodeMCU, Heart Rate Monitor, Contactless Vital Signs, Wireless Sensing, Channel State Information, Python DSP, PyQt5, Bio Radar, KL University, IoT Projects
```
