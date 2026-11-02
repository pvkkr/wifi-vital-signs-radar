# Contactless Human Vital Signs Monitoring (Heart Rate & Respiration) Using 2.4 GHz WiFi Channel State Information (CSI) on Dual ESP32 Microcontrollers

**Academic Project & Research Report**  
*Course / Department: Electronics and Communication Engineering / Computer Science & Engineering / IoT Systems*  
*Submission Date: November 2026*  

---

## Abstract

Contactless vital sign monitoring represents a critical frontier in modern telehealth, neonatal care, sleep medicine, and smart home healthcare. Conventional physiological tracking relies on intrusive wearable sensors such as electrocardiograms (ECG) and photoplethysmography (PPG), which can cause skin irritation, discomfort, and non-compliance, particularly during sleep or long-term observation. 

This project demonstrates a completely non-invasive, low-cost vital sign radar system implemented using two commercial off-the-shelf **ESP32 microcontrollers** operating on standard **2.4 GHz WiFi (IEEE 802.11n)**. By leveraging the **Channel State Information (CSI)** extracted from the physical layer (PHY) of OFDM transmissions, the system detects minute phase and amplitude perturbations caused by thoracic chest wall displacement (respiration, $5\text{ mm} - 12\text{ mm}$) and cardiac ballistocardiographic micro-motions (heartbeat, $0.1\text{ mm} - 0.5\text{ mm}$). 

A dedicated Transmitter node (TX) emits 802.11 packets at 80 Hz on WiFi Channel 11, while a Receiver node (RX) demodulates raw subcarrier channel matrices via hardware CSI callbacks and streams telemetry to a real-time Digital Signal Processing (DSP) pipeline on a host computer. Multi-subcarrier variance ranking, dual-stage Butterworth bandpass filtering, Welch Power Spectral Density (PSD) analysis, and motion artifact suppression are combined to isolate the cardiac systolic peaks and respiratory cycles. Experimental evaluations demonstrate a heart rate measurement accuracy within $\pm 2.8\text{ BPM}$ compared to optical pulse oximeter ground truth, confirming the feasibility of low-cost ubiquitous vital sign sensing.

---

## 1. Introduction & Motivation

Monitoring cardiopulmonary activity—specifically **Heart Rate (HR)** and **Respiration Rate (RR)**—provides vital diagnostic insight into autonomic nervous system tone, cardiovascular health, sleep apnea, and clinical deterioration. 

However, existing monitoring modalities suffer from notable practical drawbacks:
1. **Electrocardiography (ECG):** Requires adhesive gel electrodes connected to the skin, causing skin irritation and movement restriction.
2. **Photoplethysmography (PPG):** Requires tight skin contact on fingertips, wrists, or earlobes; susceptible to detachment during sleep.
3. **Specialized mmWave Radars (e.g., 60 GHz / 77 GHz FMCW):** Highly accurate but expensive, proprietary, and absent in standard home infrastructure.

### The WiFi Sensing Paradigm
Modern living environments are saturated with 2.4 GHz and 5 GHz wireless local area networks (WLAN). Unlike Received Signal Strength Indicator (RSSI)—a coarse, single-value scalar that only measures macroscopic attenuation—**Channel State Information (CSI)** provides fine-grained subcarrier-level channel frequency response measurements across the entire Orthogonal Frequency Division Multiplexing (OFDM) spectrum. 

When an individual sits between two WiFi transceivers, their chest surface acts as a dynamic reflector. Thoracic expansion and myocardial contractions alter the multipath propagation length on a sub-millimeter scale, causing predictable, periodic phase shifts and constructive/destructive interference across individual subcarriers.

---

## 2. Theoretical Background & Mathematical Modeling

### 2.1 Physics of RF Propagation and Multipath Interference
The wireless propagation channel between a transmitter and receiver in an indoor environment consists of multiple propagation paths:

$$y(t) = \sum_{i=1}^{N} a_i(t) \cdot e^{-j \phi_i(t)} \cdot s(t - \tau_i(t)) + n(t)$$

where:
- $s(t)$ is the transmitted 802.11 baseband signal.
- $a_i(t)$ is the attenuation of the $i$-th propagation path.
- $\phi_i(t)$ is the phase shift of the $i$-th path.
- $\tau_i(t)$ is the propagation delay along the $i$-th path.
- $n(t)$ is additive white Gaussian noise (AWGN).

The channel can be partitioned into:
1. **Static Paths:** Direct Line-of-Sight (LoS) path and reflections from static objects (walls, floor, furniture).
2. **Dynamic Path:** Reflection off the subject's anterior chest wall with instantaneous path length $d(t) = d_0 + \Delta d(t)$.

### 2.2 Phase Modulation Formula
For a carrier frequency $f_c = 2.462\text{ GHz}$ (WiFi Channel 11), the wavelength is:

$$\lambda = \frac{c}{f_c} \approx \frac{3 \times 10^8\text{ m/s}}{2.462 \times 10^9\text{ Hz}} \approx 12.18\text{ cm}$$

A physical displacement $\Delta d(t)$ of the thoracic wall alters the dynamic path length by approximately $2 \Delta d(t)$ (round-trip reflection), inducing a phase shift:

$$\Delta \phi(t) = \frac{4\pi}{\lambda} \Delta d(t) = \frac{4\pi}{\lambda} \left[ d_{\text{resp}}(t) + d_{\text{cardiac}}(t) \right]$$

- For **respiration**: $\Delta d_{\text{resp}} \approx 5\text{ mm} \implies \Delta \phi \approx \frac{4\pi \times 0.005}{0.1218} \approx 0.516\text{ radians} \approx 29.6^\circ$.
- For **cardiac ballistocardiogram**: $\Delta d_{\text{cardiac}} \approx 0.2\text{ mm} \implies \Delta \phi \approx \frac{4\pi \times 0.0002}{0.1218} \approx 0.0206\text{ radians} \approx 1.18^\circ$.

While the cardiac micro-displacement is subtle, it produces an observable high-frequency ripple modulated on top of the slow breathing envelope in sensitive OFDM subcarriers.

### 2.3 First Fresnel Zone Theory
The sensitivity of WiFi vital sign detection is governed by the geometry of the **First Fresnel Zone (FFZ)**:

$$r_1 = \sqrt{\frac{\lambda \cdot d_1 \cdot d_2}{d_1 + d_2}}$$

where $d_1$ is the distance from TX to the subject, $d_2$ is the distance from the subject to RX, and $d_1 + d_2 = D$ is the total baseline separation.

```
       [ TX ESP32 ]                    ( Subject's Chest )                    [ RX ESP32 ]
            o -------------------------------\ (X) /------------------------------- o
            | <--------- d1 = 0.6 m ---------> | <--------- d2 = 0.6 m ---------> |
            | <-------------------------- Total D = 1.2 m ------------------------> |
                                     ( First Fresnel Zone )
```

Placing the subject in the center ($d_1 = d_2 = 0.6\text{ m}$) yields an ellipse radius:

$$r_1 = \sqrt{\frac{0.1218 \times 0.6 \times 0.6}{1.2}} = \sqrt{0.0365} \approx 0.191\text{ m} = 19.1\text{ cm}$$

When the subject's anterior chest wall is positioned directly within this First Fresnel Zone boundary, the path length difference between the direct LoS path and reflected chest path satisfies the condition for maximum constructive/destructive slope $\frac{\partial |H|}{\partial d}$, maximizing detection sensitivity.

---

## 3. System Architecture & Hardware Implementation

### 3.1 Hardware Specifications
- **Microcontrollers:** 2x ESP32 Dev Module (Tensilica Xtensa Dual-Core 32-bit LX6 @ 240 MHz, 520 KB SRAM, 4 MB Flash).
- **RF Transceiver:** Integrated 802.11b/g/n HT20 WiFi radio, +20 dBm output power.
- **Interconnect:** USB-UART Bridge (CP2102 / CH340) streaming to PC at 115,200 baud.
- **Antenna:** On-board PCB inverted-F antenna (meandered dipole).

### 3.2 Dual-Node Topology
1. **Transmitter Node (TX):**
   - Configured in SoftAP + ESP-NOW mode on WiFi Channel 11 (2.462 GHz).
   - Generates high-rate 802.11 OFDM packets at $f_s = 80\text{ Hz}$ (interval $12.5\text{ ms}$).
   - Packet structure contains sequence counters, microsecond hardware timestamps, and 32 bytes of fixed training payload.
   - GPIO 2 status LED toggles at 1 Hz as an operational heartbeat indicator.

2. **Receiver Node (RX):**
   - Configured in Station promiscuous mode locked to Channel 11.
   - Registers the ESP-IDF hardware callback `esp_wifi_set_csi_rx_cb()`.
   - Enables HT20 CSI configuration (`lltf_en = true`, `htltf_en = true`, `ltf_merge_en = true`).
   - For every incoming packet, demodulates the complex channel matrix:
     $$\mathbf{H}_k = I_k + j Q_k, \quad k \in [0, 63]$$
     $$A_k = |\mathbf{H}_k| = \sqrt{I_k^2 + Q_k^2}$$
   - Selects 16 active subcarriers evenly distributed across the 20 MHz band (avoiding DC null and guard carriers).
   - Formats and transmits a high-speed telemetry frame:
     `CSI,<seq>,<time_ms>,<rssi>,<mean_amp>,<sc_0>,...,<sc_15>`

---

## 4. Digital Signal Processing (DSP) Pipeline

The host software implements a multi-stage DSP architecture in Python:

```
  [ Raw CSI Stream (16 Subcarriers @ 80 Hz) ]
                     │
                     ▼
  [ Dynamic Variance Ranking & Subcarrier Selection ]
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
  [ Respiration BPF ]     [ Respiration Cancellation ]
  (0.10 - 0.45 Hz)               │
         │                       ▼
         │               [ Cardiac BPF ]
         │               (0.80 - 2.00 Hz)
         │                       │
         ▼                       ▼
  [ Welch PSD (0.1-0.5 Hz)] [ Welch PSD (0.8-2.0 Hz)]
         │                       │
         ▼                       ▼
  Respiration Rate (RPM)   Heart Rate (BPM)
```

### 4.1 Subcarrier Selection (Variance Maximization)
Due to frequency-selective multipath fading, not all subcarriers respond equally to chest motion. Subcarriers located in static interference nulls exhibit very low signal-to-noise ratio (SNR), while subcarriers on steep slope regions display strong dynamic amplitude modulation.
Over a sliding window of 4 seconds ($N = 320$ samples), the processor computes the empirical variance for each subcarrier $j$:

$$\sigma_j^2 = \frac{1}{N} \sum_{n=1}^{N} \left( A_j[n] - \bar{A}_j \right)^2$$

The subcarrier index $k^*$ exhibiting the maximum variance within the physiological range ($0.1 < \sigma_j^2 < 80$) is dynamically selected for vital sign extraction.

### 4.2 Motion Artifact Detection & Gating
Large macroscopic movements (e.g., coughing, limb repositioning) produce variance spikes exceeding $\sigma^2 > 150$. When detected, a motion artifact gate halts vital sign updates, sets the status flag to `"Motion Detected (Stand Still)"`, and decays the Signal Quality Index (SQI) until the signal stabilizes.

### 4.3 Respiration Filtering & Rate Extraction
A 2nd-order zero-phase Butterworth bandpass filter ($[0.10, 0.45]\text{ Hz}$, equivalent to 6 to 27 breaths/min) isolates the thoracic breathing displacement. 
Respiration Rate in Breaths Per Minute (RPM) is determined by computing Welch's Power Spectral Density (PSD) with a 6-second Hann window:

$$\text{RR} = f_{\text{resp, max}} \times 60 \quad (\text{RPM})$$

### 4.4 Cardiac Filtering & Pulse Rate Extraction
Because the respiratory wave is approximately $10\times$ larger in amplitude than cardiac micro-motion, residual respiration harmonics can contaminate the heart rate band. 
1. The estimated respiration wave is subtracted from the selected raw CSI signal.
2. A 3rd-order Butterworth bandpass filter ($[0.80, 2.00]\text{ Hz}$, equivalent to 48 to 120 beats/min) isolates the cardiac ballistocardiographic waveform.
3. Welch PSD with an 8-second window extracts the dominant spectral peak $f_{\text{card, max}}$:

$$\text{HR} = f_{\text{card, max}} \times 60 \quad (\text{BPM})$$

### 4.5 Signal Quality Index (SQI)
To prevent erroneous readings, an SQI metric is computed as the ratio of peak power to total power in the cardiac band:

$$\text{SQI} = \min\left(100, \, \frac{P_{\text{peak}}}{\sum_{f=0.85}^{2.0} P(f)} \times 220\right)$$

Readings are accepted only when $\text{SQI} \ge 30\%$.

---

## 5. Experimental Evaluation & Results

### 5.1 Experimental Setup
- **Environment:** Indoor lab room with ambient WiFi and multipath reflections.
- **Node Distance:** $D = 1.2\text{ m}$ between TX and RX boards mounted at chest height ($1.0\text{ m}$ above floor).
- **Subject Position:** Seated midway between nodes ($d_1 = 0.6\text{ m}, d_2 = 0.6\text{ m}$) facing the Line-of-Sight.
- **Ground Truth:** Concurrently recorded with a Contec CMS50D clinical fingertip pulse oximeter.

### 5.2 Performance Comparison

| Test Condition | Duration | Ground Truth HR (BPM) | WiFi CSI HR (BPM) | Absolute Error (BPM) | Error (%) | Ground Truth RR (RPM) | WiFi CSI RR (RPM) |
|---|---|---|---|---|---|---|---|
| Resting Normal 1 | 120 s | 71.4 | 72.8 | 1.4 | 1.96% | 15.0 | 15.2 |
| Resting Normal 2 | 120 s | 68.0 | 70.1 | 2.1 | 3.08% | 14.5 | 14.8 |
| Post-Walking (Elevated) | 90 s | 94.2 | 96.5 | 2.3 | 2.44% | 21.0 | 20.8 |
| Breath-Holding (Apnea) | 30 s | 69.5 | 71.0 | 1.5 | 2.15% | 0.0 | 0.0 |
| Empty Room (Baseline) | 60 s | -- | 0.0 | -- | -- | -- | 0.0 |

**Mean Absolute Error (MAE):** $\mathbf{1.82\text{ BPM}}$  
**Correlation Coefficient ($r$):** $\mathbf{0.962}$  
**Breath-Holding Detection Latency:** $\mathbf{< 2.5\text{ seconds}}$

---

## 6. Faculty Viva Defense & Discussion Points

### Why CSI over RSSI?
RSSI provides only a single scalar value representing the average RF power across the entire channel ($20\text{ MHz}$). It is heavily corrupted by multi-path destructive cancellation, resulting in extreme volatility and inability to detect millimeter-scale chest displacements. CSI provides 64 distinct complex channel response measurements, allowing subcarrier selection where multipath interference amplifies the physiological motion signature.

### How are Respiration and Heartbeat Separated?
The signals occupy disjoint frequency bands in the human body:
- **Respiration:** Large displacement ($5 - 12\text{ mm}$), low frequency ($0.15 - 0.45\text{ Hz}$).
- **Heartbeat:** Micro displacement ($0.1 - 0.5\text{ mm}$), higher frequency ($0.8 - 2.0\text{ Hz}$).
A multi-stage cascade combining respiration component subtraction, tight Butterworth bandpass filtering, and Welch PSD enables clean spectral separation.

---

## 7. Conclusion & Future Work

This project proves that contactless human vital sign monitoring can be achieved with exceptional cost-efficiency using two dual-core ESP32 microcontrollers. By harvesting 802.11n Channel State Information and applying digital signal processing techniques, both respiration rate and heart rate are accurately tracked in real time without any wearable electrodes or expensive radar hardware.

**Future Directions:**
1. Integration of Graph Neural Networks (GNN) or Long Short-Term Memory (LSTM) autoencoders to reconstruct cardiac pulse waveforms under moderate subject movement.
2. Extension to 5 GHz and WiFi 6 (802.11ax) Orthogonal Frequency Division Multiple Access (OFDMA) for multi-person simultaneous vital sign tracking.
3. Deployment of an on-chip DSP pipeline running directly on ESP32 dual cores using FreeRTOS tasks.

---

## References

1. Y. Wang, et al., *"Wi-Sleep: Contactless Sleep Monitoring via WiFi Signals,"* IEEE Transactions on Mobile Computing, 2017.
2. F. Adib, et al., *"Smart Homes that Monitor Breathing and Heart Rate,"* ACM CHI Conference on Human Factors in Computing Systems, 2015.
3. Espressif Systems, *"ESP-CSI: Channel State Information Programming Guide & Framework,"* Espressif Documentation, 2024.
4. X. Wang, et al., *"PhaseBeat: Exploiting CSI Phase for Non-Invasive Heartbeat Monitoring,"* IEEE ICC, 2017.
5. J. Liu, et al., *"Tracking Vital Signs During Sleep Using RFID and WiFi,"* ACM Transactions on Sensor Networks, 2018.
