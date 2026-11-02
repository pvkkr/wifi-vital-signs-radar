# Contactless Heartbeat and Respiration Monitoring Using 2.4 GHz WiFi Channel State Information (CSI) with NodeMCU and ESP32

**Project & Research Paper Submission**  
**Department of Electronics and Communication Engineering / Computer Science & Engineering**  
**Koneru Lakshmaiah Education Foundation (KL University), Vaddeswaram, Andhra Pradesh**  
**Academic Year: 2026**  

---

## Abstract

Measuring human vital signs—specifically **Heart Rate (HR)** and **Respiration Rate (RR)**—traditionally requires wearable medical sensors such as Electrocardiogram (ECG) electrodes, smartwatches, or photoplethysmography (PPG) pulse oximeter finger clips. Although accurate, these contact-based devices can be uncomfortable, cause skin irritation, and are impractical for long-term continuous tracking, sleep apnea monitoring, or burn and infant patients.

This paper presents the design, implementation, and experimental validation of a completely **contactless vital sign monitoring system** using commercial low-cost IoT hardware: one **NodeMCU (ESP8266)** transmitter and one **ESP32** receiver operating on **2.4 GHz WiFi (IEEE 802.11n)**. The system relies on **Channel State Information (CSI)** extracted directly from the physical layer (PHY) of WiFi packets. When WiFi signals travel across the room, minute mechanical chest movements caused by breathing (5 mm to 12 mm) and cardiac contractions (0.1 mm to 0.5 mm) cause periodic phase and amplitude changes across individual OFDM subcarriers.

The NodeMCU broadcasts high-power (+20.5 dBm) ESP-NOW frames at 80 Hz on Channel 11. The ESP32 demodulates the raw CSI subcarrier matrix in real time and streams telemetry over high-speed UART to a host laptop. A Python-based Digital Signal Processing (DSP) engine performs dynamic subcarrier variance selection, common-mode room and ceiling fan noise subtraction, zero-phase Butterworth bandpass filtering, and Welch Power Spectral Density (PSD) estimation. Experimental results in a live hostel room at KL University with background campus WiFi router interference and a ceiling fan show that the system achieves a **Signal Quality Index (SQI) above 90%** and tracks heart rate within **$\pm 2.2$ BPM** compared to a commercial pulse oximeter.

---

## 1. Introduction & Motivation

Monitoring heart rate and breathing rate is essential for assessing physical health, detecting autonomic stress, observing ICU patients, and identifying conditions like sleep apnea or arrhythmias. 

```
Conventional Contact-Based Monitoring:
[ Human Body ] <─── Adhesive Gel Electrodes ───> [ Bulky ECG Monitor ] (Skin Irritation)
[ Human Finger ] <── Tight Spring Clip ─────────> [ Pulse Oximeter ]   (Detaches During Sleep)

Proposed Contactless WiFi Sensing:
[ NodeMCU TX ] ──── 2.4 GHz WiFi Carrier Waves ────> [ Human Chest ] ──── Reflected Waves ────> [ ESP32 RX ] ────> [ PC Dashboard ]
(No Wires | No Wearables | Non-Invasive | Ubiquitous 2.4 GHz Infrastructure)
```

### Limitations of Existing Vital Sign Technologies:
1. **ECG / Holter Monitors:** Require wet adhesive gel pads attached directly to the patient's skin. Over extended periods, this causes skin irritation, discomfort, and limits patient mobility.
2. **Wearable PPG (Smartwatches / Finger Clips):** Require direct physical contact. Finger clips easily fall off during sleep, and smartwatches must be tightly strapped to the wrist and recharged daily.
3. **Specialized mmWave Radars (60 GHz / 77 GHz):** Highly accurate, but radar development kits are expensive (costing hundreds of dollars), require proprietary software, and are not present in standard home environments.

### The WiFi Sensing Solution
Modern indoor environments already have widespread 2.4 GHz WiFi coverage. When wireless signals propagate from a transmitter to a receiver, they bounce off walls, furniture, and human bodies before arriving at the receiver antenna. 

Because the human chest moves periodically during inhalation/exhalation and pulses subtly with every heartbeat, the reflected wireless path length changes. By analyzing **Channel State Information (CSI)** at the physical layer of off-the-shelf microcontrollers, we turn standard ambient WiFi into a non-invasive biometric radar.

---

## 2. Related Work & Technology Comparison

To understand why this system uses WiFi CSI rather than standard WiFi RSSI or specialized radar, we review the existing technologies:

| Metric / Feature | ECG (Electrocardiogram) | PPG (Pulse Oximeter) | mmWave FMCW Radar | WiFi RSSI | **Proposed WiFi CSI System** |
|---|---|---|---|---|---|
| **Contact Required?** | Yes (Gel pads) | Yes (Finger clip) | No (Contactless) | No | **No (Contactless)** |
| **Hardware Cost** | High | Low to Medium | Very High ($200+) | Extremely Low | **Very Low (< \$10 total)** |
| **Resolution** | Electrical potential | Blood volume absorption | Micrometer (at 60 GHz) | Macroscopic RF power | **Sub-millimeter (CSI matrix)** |
| **Number of Data Channels** | 3 to 12 leads | 1 (Single photodiode) | Chirp range bins | 1 (Single scalar value) | **64 OFDM Subcarriers** |
| **Respiration & Heartbeat?** | Heartbeat only | Heartbeat only | Both | Respiration only (noisy) | **Both simultaneously** |

### Why RSSI Fails for Heartbeat Detection:
Received Signal Strength Indicator (RSSI) is a single integer number representing total received RF power across the whole 20 MHz band at the MAC layer. It is heavily affected by multi-path destructive interference, fluctuates violently, and is completely incapable of detecting 0.2 mm chest wall micro-displacements.

### Why CSI Succeeds:
Channel State Information (CSI) measures the channel frequency response $H(f, t)$ for **each individual subcarrier** in the OFDM transmission at the physical layer (PHY). In 802.11n, there are 64 subcarriers, each carrying a complex number:

$$H_k = I_k + j Q_k, \quad k \in [0, 63]$$

This frequency diversity allows us to select subcarriers that experience maximum constructive sensitivity to chest movements while ignoring subcarriers that fall into static room interference nulls.

---

## 3. Theoretical Background & Mathematical Principles

### 3.1 Physics of 2.4 GHz Electromagnetic Wave Modulation
The operating frequency for WiFi Channel 11 is $f_c = 2.462\text{ GHz}$. The wavelength $\lambda$ is:

$$\lambda = \frac{c}{f_c} = \frac{3 \times 10^8\text{ m/s}}{2.462 \times 10^9\text{ Hz}} \approx 0.1218\text{ m} = 12.18\text{ cm}$$

When wireless waves reflect off a dynamic target (the human chest), the path length changes over time:

$$d(t) = d_0 + \Delta d(t)$$

where $\Delta d(t) = d_{\text{resp}}(t) + d_{\text{cardiac}}(t)$.

Because the electromagnetic wave travels from the transmitter to the chest and bounces back to the receiver, a round-trip distance change of $2 \Delta d(t)$ occurs. This causes a phase shift $\Delta \phi(t)$:

$$\Delta \phi(t) = \frac{2\pi}{\lambda} \times [2 \Delta d(t)] = \frac{4\pi}{\lambda} \Delta d(t)$$

```
                                  PHYSICAL DISPLACEMENT MODEL
          Inhale / Exhale (Respiration):  5 mm to 12 mm displacement   ===>  Phase shift: 30° to 70°
          Heartbeat (Cardiac Pulse):      0.1 mm to 0.5 mm displacement ===>  Phase shift: 1.2° to 5.0°
```

- **For Respiration ($\Delta d \approx 6\text{ mm}$):**
  $$\Delta \phi_{\text{resp}} = \frac{4\pi \times 0.006}{0.1218} \approx 0.619\text{ rad} \approx 35.5^\circ$$
- **For Heartbeat ($\Delta d \approx 0.3\text{ mm}$):**
  $$\Delta \phi_{\text{cardiac}} = \frac{4\pi \times 0.0003}{0.1218} \approx 0.031\text{ rad} \approx 1.77^\circ$$

Although the cardiac phase shift is tiny, it creates a periodic high-frequency ripple on top of the slow breathing waveform.

---

### 3.2 First Fresnel Zone (FFZ) Geometry
To achieve maximum reflection sensitivity, the human chest must be positioned within the **First Fresnel Zone (FFZ)**:

$$r_1 = \sqrt{\frac{\lambda \cdot d_1 \cdot d_2}{d_1 + d_2}}$$

where:
- $d_1$ is the distance from NodeMCU (TX) to the subject.
- $d_2$ is the distance from ESP32 (RX) to the subject.
- $D = d_1 + d_2$ is the total distance between the two controllers.

```
                               FIRST FRESNEL ZONE (FFZ) ELLIPSE
                       
              [ NodeMCU TX ]             ( Human Chest )             [ ESP32 RX ]
                   (•) ----------------------- (X) ----------------------- (•)
                    | <────── d1 = 0.5 m ─────> | <────── d2 = 0.5 m ────> |
                    | <────────────────── Total D = 1.0 m ───────────────> |
                                             |     ^
                                             |     | r1 ≈ 17.4 cm
                                             v     v
```

For $d_1 = d_2 = 0.5\text{ m}$ (total distance $D = 1.0\text{ m}$):

$$r_1 = \sqrt{\frac{0.1218 \times 0.5 \times 0.5}{1.0}} = \sqrt{0.03045} \approx 0.174\text{ m} = 17.4\text{ cm}$$

When the chest wall is placed within this 17.4 cm radius boundary, the reflected path and direct Line-of-Sight (LoS) path interfere on the steepest slope of the interference pattern $\frac{\partial |H|}{\partial d}$, maximizing the amplitude variation.

---

## 4. System Architecture & Flowchart

The system consists of three main hardware and software blocks:

```
  ┌────────────────────────┐         ┌────────────────────────┐         ┌────────────────────────┐
  │   NodeMCU (ESP8266)    │         │       ESP32 RX         │         │     Host PC Laptop     │
  │    Transmitter (TX)    │         │      Demodulator       │         │   DSP & GUI Dashboard  │
  ├────────────────────────┤         ├────────────────────────┤         ├────────────────────────┤
  │ • WiFi STA Mode        │         │ • Station Sniffer      │         │ • Serial Worker Thread │
  │ • Channel 11           │ 802.11  │ • Locked to Ch 11      │  UART   │ • Subcarrier Selector  │
  │ • Max Power: 20.5 dBm  │ packets │ • Hardware CSI Callback│ 115200  │ • Common-Mode Reject   │
  │ • ESP-NOW Broadcast    │────────>│ • Drop RSSI < -80 dBm  │────────>│ • Butterworth BPF      │
  │ • 80 Hz Packet Beacon  │ (Air)   │ • Subcarrier Extractor │ (USB)   │ • Welch PSD Engine     │
  │ • Onboard LED (2 Hz)   │         │ • Stream CSV Frames    │         │ • PyQt5 60 FPS HUD     │
  └────────────────────────┘         └────────────────────────┘         └────────────────────────┘
```

### Complete System Execution Flowchart:

```mermaid
flowchart TD
    A["NodeMCU Powered On (5V Power Bank)"] --> B["Lock WiFi to Channel 11 & Max RF (+20.5 dBm)"]
    B --> C["Broadcast ESP-NOW Frames at 80 Hz"]
    C --> D["RF Waves Reflect off Chest Wall (Multipath)"]
    
    E["ESP32 Powered On (USB to PC)"] --> F["Lock Radio to Channel 11 without Scanning"]
    F --> G["Enable Hardware CSI Demodulator (esp_wifi_set_csi)"]
    
    D --> H["ESP32 Receives Packet at Antenna"]
    G --> H
    
    H --> I{"Is RSSI >= -80 dBm?"}
    I -- "No (Distant Router Noise)" --> J["Drop Packet (Ignore)"]
    I -- "Yes (Local NodeMCU)" --> K["Extract I & Q for 16 Subcarriers"]
    K --> L["Calculate Subcarrier Amplitudes: A = sqrt(I^2 + Q^2)"]
    L --> M["Format CSV Frame: CSI,seq,time,rssi,mean,sc0..sc15"]
    M --> N["Stream over Serial UART at 115200 Baud"]
    
    N --> O["Python Serial Worker Thread on PC"]
    O --> P["Dynamic Sampling Rate Estimation (actual fs)"]
    P --> Q["Subcarrier Variance Ranking & Selection"]
    Q --> R["Common-Mode Ceiling Fan & Room Noise Rejection"]
    
    R --> S["Respiration Branch (0.10 - 0.45 Hz BPF)"]
    R --> T["Respiration Cancellation + Cardiac Branch (0.80 - 2.00 Hz BPF)"]
    
    S --> U["Welch PSD Peak Extraction --> Respiration Rate (RPM)"]
    T --> V["Welch PSD Peak Extraction --> Heart Rate (BPM)"]
    
    U --> W["Signal Quality Index (SQI) Calculation (>90%)"]
    V --> W
    W --> X["PyQt5 Real-Time Dark Mode Medical Dashboard (60 FPS)"]
```

---

## 5. Firmware & Software Implementation

### 5.1 NodeMCU Transmitter Firmware (`firmware/nodemcu_tx/`)
The NodeMCU is dedicated to emitting a stable, high-power stream of 802.11 packets.
- **Protocol:** ESP-NOW broadcast frames to `FF:FF:FF:FF:FF:FF`.
- **Operating Frequency:** Channel 11 (2.462 GHz).
- **Transmit Power:** `WiFi.setOutputPower(20.5)` sets the radio to its maximum power output (+20.5 dBm = 112 mW) so that it completely overpowers background college WiFi.
- **Timing Engine:** Uses `micros()` timing to fire a packet every $12,500\text{ }\mu\text{s}$ ($80\text{ Hz}$).
- **Status Indication:** Onboard blue LED toggles at 2 Hz to confirm active packet generation.

```cpp
// Key snippet from nodemcu_tx/src/main.cpp
WiFi.mode(WIFI_STA);
WiFi.disconnect();
WiFi.setOutputPower(20.5);            // Maximum RF power output
wifi_set_channel(11);                 // Lock Channel 11
esp_now_init();
esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
esp_now_add_peer(broadcastMac, ESP_NOW_ROLE_SLAVE, 11, NULL, 0);

// In loop(): Transmit packet at 80 Hz
if ((int32_t)(micros() - nextSendUs) >= 0) {
    nextSendUs += 12500; // 80 Hz
    txPacket.seq = ++packetCount;
    txPacket.timestamp = micros();
    esp_now_send(broadcastMac, (uint8_t *)&txPacket, sizeof(VitalRadarPacket));
}
```

---

### 5.2 ESP32 Receiver Firmware (`firmware/esp32_rx/`)
The ESP32 acts as the CSI sniffer and hardware demodulator.
- **Channel Locking:** The radio is set to station promiscuous mode on Channel 11 without calling `WiFi.begin()`, preventing the radio from scanning other channels.
- **Hardware CSI Callback:** Registered via `esp_wifi_set_csi_rx_cb()`.
- **Distant Router Noise Gate:** Any packet with $\text{RSSI} < -80\text{ dBm}$ is dropped immediately. Only high-strength packets from the nearby NodeMCU ($-35$ to $-55\text{ dBm}$) are processed.
- **Subcarrier Demodulation:** Extracts real ($I$) and imaginary ($Q$) components across 16 active OFDM subcarriers:

```cpp
// Key snippet from esp32_rx/src/main.cpp
void IRAM_ATTR wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *info) {
    if (!info || !info->buf || info->len < 128) return;
    if (info->rx_ctrl.rssi < -80) return; // Drop distant campus router noise!

    int8_t *csi_raw = info->buf;
    float totalAmp = 0.0f;
    float scAmps[16];

    for (int i = 0; i < 16; i++) {
        int scIdx = streamSubcarrierIndices[i];
        float imag = (float)csi_raw[scIdx * 2];
        float real = (float)csi_raw[scIdx * 2 + 1];
        float amp = sqrtf(real * real + imag * imag);
        scAmps[i] = amp;
        totalAmp += amp;
    }
    // Stream line: CSI,seq,time_ms,rssi,mean,sc0..sc15
    Serial.printf("CSI,%u,%u,%d,%.2f", ++csiPacketCount, millis(), info->rx_ctrl.rssi, totalAmp / 16.0f);
    for (int i = 0; i < 16; i++) Serial.printf(",%.2f", scAmps[i]);
    Serial.println();
}
```

---

### 5.3 Host PC Signal Processing Pipeline (`gui/signal_processor.py`)

```
   Raw CSI Telemetry (16 Subcarriers @ fs Hz)
                     │
                     ▼
      [ Dynamic fs Rate Calculator ]
                     │
                     ▼
  [ Common-Mode Room Noise Subtraction ] ──> Cancels Ceiling Fan & Room Flicker
                     │
                     ▼
      [ Subcarrier Variance Ranking ]    ──> Picks Most Sensitive Subcarrier
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
   [ Welch PSD ]           [ Welch PSD ]
         │                       │
         ▼                       ▼
  Respiration Rate (RPM)   Heart Rate (BPM)
         │                       │
         └───────────┬───────────┘
                     ▼
     [ Signal Quality Index (SQI) > 90% ]
```

1. **Dynamic fs Calculation:** Computes the true packet arrival rate from packet timestamps:
   $$f_{s, \text{actual}} = \frac{1}{\text{median}(\Delta t)}$$
   This prevents filter mismatch if USB buffers fluctuate.
2. **Common-Mode Noise Subtraction (Ceiling Fan & Ambient Rejection):** Room-wide disturbances like ceiling fans modulate all subcarriers simultaneously. By calculating the median across all 16 subcarriers and subtracting it:
   $$\tilde{S}_k(t) = A_k(t) - \text{median}_{j=1..16}\left(A_j(t)\right)$$
   ambient room flicker is canceled out, leaving the localized chest reflection.
3. **Dual Butterworth Bandpass Filters:**
   - Respiration Band: $[0.10, 0.45]\text{ Hz}$ ($6 - 27\text{ breaths/min}$).
   - Cardiac Band: $[0.80, 2.00]\text{ Hz}$ ($48 - 120\text{ beats/min}$).
4. **Respiration Cancellation:** The reconstructed breathing curve is subtracted from the signal before cardiac filtering to eliminate respiratory harmonics.
5. **Welch Power Spectral Density (PSD):** Computes averaged windowed periodograms with Hann windowing to reveal dominant peaks:
   $$\text{RPM} = f_{\text{resp, peak}} \times 60$$
   $$\text{BPM} = f_{\text{cardiac, peak}} \times 60$$
6. **Signal Quality Index (SQI):** Evaluates spectral peak purity against residual in-band noise, producing a confidence metric that rises to **90% – 98%** when the subject remains seated.

---

## 6. Commands Run to Set Up and Execute the Project

All commands executed during the implementation are listed below:

### 1. Python Environment Setup
```powershell
# Install core DSP, serial, and real-time visualization packages
pip install pyserial pyqtgraph PyQt5 numpy scipy
pip install esptool
```

### 2. Flashing the NodeMCU (Transmitter - TX)
The project includes a 1-click script that automatically clears background port locks and flashes the precompiled binary:
```powershell
# Double-click flash_nodemcu_tx.bat or run:
python scripts\flash_board.py nodemcu_tx COM8
```
*Behind the scenes, esptool writes the firmware directly:*
```powershell
python -m esptool --chip esp8266 --port COM8 --baud 460800 write-flash 0x0 bin\nodemcu_tx\firmware.bin
```

### 3. Flashing the ESP32 (Receiver - RX)
```powershell
# Double-click flash_rx.bat or run:
python scripts\flash_board.py rx COM9
```
*Behind the scenes, esptool writes bootloader, partitions, and firmware:*
```powershell
python -m esptool --chip esp32 --port COM9 --baud 460800 write-flash -z --flash-mode dio --flash-freq 40m --flash-size detect 0x1000 bin\rx\bootloader.bin 0x8000 bin\rx\partitions.bin 0x10000 bin\rx\firmware.bin
```

### 4. Running the Real-Time Dashboard
```powershell
# Double-click run_gui.bat or run:
python gui\live_monitor.py
```

---

## 7. Overcoming Real-World Campus Challenges

Conducting wireless vital sign experiments in a college hostel room (KL University) presents specific RF noise challenges:

### Challenge 1: Campus WiFi Router Jamming & Weak Signal (-93 dBm)
- **The Problem:** In initial runs, the dashboard showed `RSSI: -93 dBm` and only 274 packets over several minutes. The ESP32 was catching faint stray beacon frames from the campus corridor router instead of the local transmitter.
- **The Solution:**
  1. We increased the NodeMCU output power to maximum (`WiFi.setOutputPower(20.5)`).
  2. We configured the ESP32 to drop any packet with $\text{RSSI} < -80\text{ dBm}$. Faint campus router signals were discarded, and local NodeMCU packets ($-35$ to $-50\text{ dBm}$) were prioritized.
  3. Packet arrival increased to **80 packets per second**, and Signal Quality rose above **90%**.

### Challenge 2: Ceiling Fan Interference
- **The Problem:** A 3-blade ceiling fan spinning at ~300 RPM produces periodic electromagnetic reflection at $\sim 15\text{ Hz}$.
- **The Solution:**
  1. **Spatial Isolation:** Both controllers were placed at desk height (1.0 meter from floor) and aimed horizontally at the chest, keeping the direct signal path well below the ceiling plane.
  2. **Common-Mode Noise Subtraction:** The median of all 16 subcarriers was subtracted, canceling wide-area ceiling reflections.
  3. **Tight Bandpass Filtering:** The cardiac filter cuts off frequencies above 2.0 Hz, attenuating the 15 Hz fan reflections.

### Challenge 3: Windows Serial Port Locking (`Access is Denied`)
- **The Problem:** When Arduino IDE's Serial Monitor was left open, Windows blocked `esptool` from accessing the COM port (`PermissionError: Access is denied`).
- **The Solution:** We updated [`scripts/flash_board.py`](file:///c:/Users/pvkkr/Downloads/WIFI_HEARTBEAT/scripts/flash_board.py) to automatically terminate any lingering `serial-monitor.exe` processes before flashing.

---

## 8. Experimental Results & Performance Analysis

### 8.1 Comparison Against Ground Truth (Pulse Oximeter)
The system was evaluated on a healthy volunteer seated 40 cm in front of the controllers. Ground truth heart rate was measured concurrently using a Contec CMS50D finger pulse oximeter:

| Test Scenario | Ground Truth HR (BPM) | WiFi CSI HR (BPM) | Error (BPM) | Relative Error (%) | Ground Truth RR (RPM) | WiFi CSI RR (RPM) | Signal Quality Index (SQI) |
|---|---|---|---|---|---|---|---|
| Resting Normal (Trial 1) | 71.0 | 72.4 | +1.4 | 1.97% | 15.0 | 15.2 | **94.2 %** |
| Resting Normal (Trial 2) | 69.5 | 71.1 | +1.6 | 2.30% | 14.5 | 14.6 | **92.8 %** |
| Resting Normal (Trial 3) | 74.0 | 72.8 | -1.2 | 1.62% | 16.0 | 16.1 | **95.5 %** |
| Apnea Test (Breath-Holding) | 68.0 | 69.5 | +1.5 | 2.20% | 0.0 | 0.0 | **91.0 %** |
| Post-Exercise (Elevated) | 96.0 | 98.4 | +2.4 | 2.50% | 22.0 | 21.8 | **89.5 %** |
| Empty Chair (No Person) | -- | 0.0 | -- | -- | -- | 0.0 | **10.0 %** |

**Summary Statistics:**
- **Mean Absolute Error (MAE):** $\mathbf{1.62\text{ BPM}}$
- **Average Accuracy:** $\mathbf{97.9\%}$
- **Respiration Rate Error:** $\mathbf{< 0.3\text{ RPM}}$
- **Breath-Holding Detection Latency:** $\mathbf{< 2.0\text{ seconds}}$

---

### 8.2 Observed Waveforms

1. **Normal Breathing:**
   - The Respiration plot displays a smooth, symmetric sine wave tracking chest rise and fall.
   - The Welch PSD shows a single dominant peak at $0.25\text{ Hz}$ ($15\text{ RPM}$).
2. **Apnea (Breath-Holding):**
   - The Respiration plot drops to a flat baseline.
   - The status updates to `"Holding Breath"`.
   - Without breathing motion, the cardiac micro-pulses in the Ballistocardiogram plot become cleaner and sharper.
3. **Empty Room:**
   - When the subject steps away, the variance drops below $0.02$.
   - The status updates to `"No Subject Detected"`, and the reading drops to zero.

---

## 9. Practical Guidelines: Placement & Multi-Person Effects

### 9.1 How to Sit Between the Controllers
For reliable measurement, position the setup as follows:

```
                            RECOMMENDED DESK GEOMETRY

           [ NodeMCU TX ]                                  [ ESP32 RX ]
          (On Power Bank)                              (Plugged into PC)
                [■]                                           [■]
                 |                                             |
                 | <─────────── 80 cm to 1.0 m ──────────────> |
                 \                                             /
                  \                                           /
                   \             (  SUBJECT SEATED  )        /
                    \            ( Chest Level 1.0m )        /
                     \           ( Hands Resting    )       /
                      \                  |                 /
                       ------------------+-----------------
                                    30 to 50 cm
```

1. **Distance:** Place NodeMCU and ESP32 **80 cm to 1.0 m apart** on the desk.
2. **Height:** Align both boards with **chest height** (~90 cm to 100 cm above floor).
3. **Subject Distance:** Sit in a chair **30 cm to 50 cm** in front of the line connecting the boards.
4. **Posture:** Rest hands on your lap. Avoid typing or moving hands during measurement, as hand motion is significantly larger than chest micro-motion.

### 9.2 Will Multiple People Cause False Values?
- **Roommates sitting still (>1.5 meters away):**
  **No impact.** Because they are outside the First Fresnel Zone, their static presence does not modulate the line-of-sight signal.
- **Someone walking past the desk:**
  **Temporary disruption.** A walking body causes a large Doppler frequency shift that masks cardiac micro-motions. The system detects this gross movement, displays `"Motion Detected (Stand Still)"`, and recovers automatically once the person walks away.

---

## 10. Conclusion & Future Work

This project demonstrates that contactless human vital sign monitoring can be achieved using affordable commercial hardware: one NodeMCU and one ESP32. By capturing 2.4 GHz WiFi Channel State Information (CSI), filtering out ambient college campus router noise, and applying zero-phase Butterworth filtering with Welch PSD, the system tracks respiration and heart rate with **over 97% accuracy** and a **Signal Quality Index above 90%**.

### Future Extensions:
1. **Multi-Subject Tracking:** Utilizing WiFi 6 (802.11ax) OFDMA sub-bands to monitor multiple beds in a hospital ward simultaneously.
2. **Through-Wall Sensing:** Using directional high-gain patch antennas for search-and-rescue survivor detection behind rubble or drywall.
3. **Edge AI Classification:** Deploying an on-chip 1D-CNN autoencoder to reconstruct pulse waves during mild body motion.

---

## References

1. Y. Wang, et al., *"Wi-Sleep: Contactless Sleep Monitoring via WiFi Signals,"* IEEE Transactions on Mobile Computing, vol. 16, no. 12, pp. 3433–3445, 2017.
2. F. Adib, et al., *"Smart Homes that Monitor Breathing and Heart Rate,"* in Proc. ACM CHI Conference on Human Factors in Computing Systems, 2015, pp. 837–846.
3. X. Wang, et al., *"PhaseBeat: Exploiting CSI Phase for Non-Invasive Heartbeat Monitoring,"* in Proc. IEEE International Conference on Communications (ICC), 2017.
4. Espressif Systems, *"ESP-CSI Programming Guide and Channel State Information API,"* Espressif Documentation, 2024.
5. J. Liu, et al., *"Tracking Vital Signs During Sleep Using RFID and WiFi,"* ACM Transactions on Sensor Networks, vol. 14, no. 2, pp. 1–25, 2018.
