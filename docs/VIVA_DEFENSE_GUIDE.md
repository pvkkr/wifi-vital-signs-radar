# Faculty Viva Defense Guide & Oral Examination Cheat Sheet

**Project:** Contactless Vital Signs Monitoring Using 2x ESP32 WiFi CSI  
**Target:** A+ Grade in Evaluation & Viva Voce  

---

## 🏆 Top 15 Tough Viva Questions & Perfect Model Answers

### Q1: What is the fundamental principle behind measuring heartbeats using WiFi?
**Model Answer:**  
> "WiFi operates at 2.4 GHz, which corresponds to a wavelength of approximately 12.2 cm. When WiFi signals travel between the Transmitter and Receiver, they reflect off the human torso. As the heart beats, it creates small mechanical chest wall displacements of about 0.2 to 0.5 mm due to ballistocardiographic micro-motion. This tiny periodic displacement changes the reflected path length, inducing a periodic phase shift ($\Delta \phi = \frac{4\pi}{\lambda}\Delta d$) and amplitude fluctuation in the Channel State Information (CSI) across OFDM subcarriers."

---

### Q2: Why did you use CSI instead of RSSI? Can't RSSI do this?
**Model Answer:**  
> "No, RSSI (Received Signal Strength Indicator) is fundamentally unsuitable for heartbeat detection. RSSI is a coarse, single scalar value that averages RF power across the entire 20 MHz band at the MAC layer. It suffers from severe multipath fading and cannot resolve sub-millimeter chest displacements. In contrast, CSI (Channel State Information) is extracted at the PHY layer and provides 64 distinct complex channel responses ($H_k = I_k + jQ_k$), allowing us to observe individual subcarriers that experience maximum sensitivity to chest movements."

---

### Q3: How do you separate the heartbeat signal from breathing, since breathing is so much bigger?
**Model Answer:**  
> "Breathing displacement is 5–12 mm, while cardiac displacement is only 0.2–0.5 mm—so respiration is roughly 10 to 20 times stronger. However, they occupy distinctly different frequency bands:
> 1. **Respiration band:** 0.10 Hz to 0.45 Hz (6 to 27 breaths per minute).
> 2. **Cardiac band:** 0.80 Hz to 2.00 Hz (48 to 120 beats per minute).
> 
> In our digital signal processing pipeline, we first filter out the breathing wave using a 2nd-order bandpass filter. Then, we subtract the reconstructed breathing component from the raw signal to eliminate respiratory harmonic leakage before feeding it into a tight 3rd-order Butterworth cardiac bandpass filter. Finally, Welch Power Spectral Density (PSD) extracts the dominant cardiac peak."

---

### Q4: Why are 2 ESP32s required? Can't we do it with just 1 ESP32?
**Model Answer:**  
> "To capture CSI in 802.11 standards, an active RF packet transmission must take place between a transmitter and a receiver so that the receiver's PHY hardware can decode the preamble training fields (LTF/STF). With one ESP32 acting as a continuous high-rate transmitter (80 Hz) and the other as a dedicated receiver, we establish a controlled, stable RF link across the First Fresnel Zone without relying on external home routers or third-party traffic."

---

### Q5: What packet transmission rate did you use and why?
**Model Answer:**  
> "We configured the Transmitter to emit packets at **80 Hz** (every 12.5 ms). According to the Nyquist-Shannon sampling theorem, to detect a maximum heart rate of 120 BPM (2.0 Hz) or cardiac harmonics up to 4.0 Hz, our minimum sampling rate must exceed 8.0 Hz. An 80 Hz rate provides 10× oversampling, which eliminates aliasing, enables high-order digital filtering, and allows real-time spectral estimation with low latency."

---

### Q6: What is the 'First Fresnel Zone' and why does it matter here?
**Model Answer:**  
> "The First Fresnel Zone is an elliptical region between the transmitter and receiver where the reflected path length differs from the direct line-of-sight path by less than half a wavelength ($\lambda/2$). By positioning the subject's anterior chest within the boundary of the First Fresnel Zone ($D = 1.2\text{ m}$, subject at $0.6\text{ m}$), the chest motion modulates the signal around the point of steepest slope between constructive and destructive interference, maximizing the amplitude response $\frac{\partial |H|}{\partial d}$."

---

### Q7: Why do different subcarriers show different waveforms?
**Model Answer:**  
> "In OFDM, each subcarrier has a slightly different frequency ($f_k = f_c + k \cdot 312.5\text{ kHz}$). Because of multipath reflections, waves on certain subcarriers interfere constructively at the receiver, while others interfere destructively. Subcarriers sitting near destructive nulls have almost zero sensitivity, whereas subcarriers sitting on the slope of an interference fringe produce dramatic changes when the chest moves. Our algorithm dynamically ranks subcarriers by variance to select the optimal one."

---

### Q8: What happens if the person moves their hands or body?
**Model Answer:**  
> "Macroscopic body movement introduces large motion artifacts that overpower physiological micro-motions. Our software implements **Motion Artifact Rejection Gating**: when the variance of the raw signal spikes above our baseline threshold ($\sigma^2 > 150$), the system identifies gross motion, temporarily freezes the BPM estimate, illuminates a 'Motion Detected - Stand Still' warning, and waits 1 to 2 seconds for the channel to re-stabilize."

---

### Q9: What is the role of Welch's PSD instead of standard FFT?
**Model Answer:**  
> "A standard raw FFT on noisy biological signals suffers from spectral leakage and high variance in frequency bins. Welch's method splits the signal into overlapping segments, windows each segment with a Hann window, and computes the averaged periodogram. This significantly reduces noise variance and reveals a sharp, distinct cardiac peak even in the presence of thermal RF noise."

---

### Q10: What ESP-IDF APIs did you use on the ESP32 to get CSI?
**Model Answer:**  
> "We utilized Espressif's native CSI API:
> - `esp_wifi_set_csi_config(&csi_config)` to configure HT20 legacy and HT long training field acquisition.
> - `esp_wifi_set_csi_rx_cb(wifi_csi_rx_cb, NULL)` to register the hardware interrupt callback that fires upon every received packet.
> - `esp_wifi_set_csi(true)` to enable hardware demodulation of the subcarrier matrix in real time."

---

### Q11: How do you prove this works during a live demo?
**Model Answer:**  
> "We can prove this live through three clear tests:
> 1. **Breath-Holding Test (Apnea):** When I hold my breath, the slow respiration wave immediately drops to flatline, and the sharp cardiac pulse waveform becomes clearly isolated on the screen.
> 2. **Presence Test:** When I step away from between the two ESP32s, the signal returns to flat noise, and the status changes to 'No Subject Detected'.
> 3. **Verification against Pulse Oximeter:** Our measured BPM matches within $\pm 2$ to $3$ BPM of a standard fingertip pulse oximeter."

---

### Q12: Why did you choose WiFi Channel 11?
**Model Answer:**  
> "Channels 1, 6, and 11 are the three non-overlapping 20 MHz channels in the 2.4 GHz band. In most academic and residential buildings, Channel 1 and Channel 6 are heavily congested by default router configurations. Channel 11 typically has lower background interference, providing higher signal purity."

---

### Q13: Could this work through a wall?
**Model Answer:**  
> "Yes! 2.4 GHz electromagnetic waves penetrate drywall, wood, and standard indoor partitions with only a 3 to 5 dB attenuation per wall. While signal attenuation is higher, placing the TX and RX on either side of a wall allows through-wall respiration and presence detection, which is widely studied for search-and-rescue and non-intrusive patient monitoring."

---

### Q14: What is the baud rate of your serial link and why?
**Model Answer:**  
> "We use **115,200 baud** for universal compatibility and rock-solid stability across all USB-UART drivers. Since each telemetry frame is compact (~60 bytes) and transmitted at 80 Hz, total bandwidth is $4.8\text{ kB/s}$, which utilizes less than 45% of the 115,200 baud capacity, guaranteeing zero packet drops or buffer overruns."

---

### Q15: What are the main limitations and how would you improve this in future work?
**Model Answer:**  
> "Current limitations include sensitivity to gross body movement and difficulty separating multiple persons in the same room. In future work, we plan to implement:
> 1. Multi-input Multi-output (MIMO) antenna arrays to perform beamforming and spatial separation.
> 2. Machine learning models (such as Bi-LSTM or 1D-CNN autoencoders) trained to reconstruct pulse waveforms during walking or movement."

---

## 💡 Quick Tips for the Live Demo:
1. **Wear normal clothes:** Thin shirts or t-shirts work best (thick heavy down jackets slightly dampen reflections).
2. **Distance:** Sit approx 50–60 cm away from both ESP32s, facing the line connecting them.
3. **Stay still for 5 seconds:** Allow the 4-second sliding buffer to fill and calculate baseline variance.
4. **Use the "Holding Breath" demonstration:** This is the most impressive part of the demo because faculty can visibly see the large breathing waves vanish and the cardiac pulse train emerge clearly on the screen!
