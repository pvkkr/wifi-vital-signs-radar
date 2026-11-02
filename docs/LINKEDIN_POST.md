# 🚀 LinkedIn Post Template: Contactless WiFi Vital Signs Radar

Copy and paste this directly onto your LinkedIn profile, and attach your proof video!

---

### 📝 LinkedIn Post Text:

Can standard WiFi signals measure your heartbeat without touching your body? 🫀📡

Over the last few days, I built a completely contactless biometric radar using off-the-shelf microcontrollers: one **NodeMCU (ESP8266)** and one **ESP32**, running on standard **2.4 GHz WiFi (IEEE 802.11n)**!

In my live validation test comparing against a physical fingertip pulse sensor:
👉 **Physical Pulse Sensor:** 64 BPM
👉 **WiFi CSI Radar:** 65 BPM
🎯 **Difference: Only 1 BPM (~98.5% accuracy)!**

### 💡 How It Works (The Science):
Every time our heart beats, it creates subtle mechanical chest-wall micro-movements of just 0.2 mm to 0.5 mm (ballistocardiogram). 

1. **Transmitter (NodeMCU):** Emits high-rate (80 Hz) broadcast packets at +20.5 dBm on WiFi Channel 11.
2. **RF Multipath Modulation:** As the 2.4 GHz electromagnetic carrier waves ($\lambda \approx 12.2\text{ cm}$) pass across the First Fresnel Zone, chest wall micro-motion causes periodic phase shifts ($\Delta \phi = \frac{4\pi}{\lambda}\Delta d$).
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

Check out the video below showing the live waveform response and real-time pulse tracking!

What are your thoughts on using ambient RF signals for non-invasive telemedicine and sleep monitoring?

#IoT #EmbeddedSystems #ESP32 #NodeMCU #WirelessSensing #SignalProcessing #Python #DSP #BiomedicalEngineering #HealthTech #Innovation #KLUniversity #Telehealth #Engineering
