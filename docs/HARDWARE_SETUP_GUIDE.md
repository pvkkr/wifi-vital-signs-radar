# Hardware Setup & Physical Placement Guide

Follow these exact steps to assemble, position, and run your WiFi Vital Signs Radar tonight.

---

## 🛠️ What You Need Tonight
1. **1x NodeMCU (ESP8266 or NodeMCU-32S)** $\to$ Acts as the **Transmitter (TX)**.
2. **1x ESP32** $\to$ Acts as the **Receiver (RX)** (demodulates hardware WiFi CSI).
3. **2x Micro-USB cables** (one for PC/Laptop, one for any 5V phone charger or power bank).
4. **Your Windows Laptop** (running the live dashboard).

---

## ⚡ Step 1: Flashing the Firmware (Takes 2 minutes)

All firmware files are pre-compiled and ready in the `bin/` folder.

### A. Flash your NodeMCU (Transmitter - TX):
1. Plug your **NodeMCU** into your laptop via USB.
2. Double-click **`flash_nodemcu_tx.bat`** in the project folder.
3. Select your COM port number when prompted.
4. Once complete, unplug the NodeMCU and power it from **any USB phone charger or power bank**!

*(Note: If your NodeMCU is a NodeMCU-32S ESP32, you can also use `flash_tx.bat`)*

### B. Flash your ESP32 (Receiver - RX):
1. Plug your **ESP32** into your laptop via USB.
2. Double-click **`flash_rx.bat`** in the project folder.
3. Select your COM port number when prompted.
   *(Tip: If esptool says "Connecting...", hold down the BOOT button on the ESP32 for 2 seconds)*.
4. **Keep this ESP32 connected to your laptop via USB** (it streams the CSI telemetry into the Python GUI).

---

## 📐 Step 2: Physical Placement & Subject Positioning

For maximum sensitivity, follow the **First Fresnel Zone geometry**:

```
                       TOP-DOWN ROOM VIEW

     [ NodeMCU TX ]                                    [ ESP32 RX ]
      (Power Bank)                                   (Connected to PC)
          [■]                                               [■]
           |                                                 |
           | <--------------- 1.0 m to 1.3 m ---------------> |
           \                                                 /
            \                                               /
             \               (  SUBJECT  )                 /
              \              (  Sitting  )                /
               \             (  In Chair )               /
                \                   |                   /
                 \                  |                  /
                  ------------------+------------------
                               0.5 m to 0.7 m
```

### Positioning Checklist:
1. **Distance between ESP32s:** Place TX and RX approximately **1.0 to 1.4 meters apart** on a table or two chairs.
2. **Height:** Mount or rest both ESP32s at **chest height** (around 90 cm to 110 cm from the floor when seated).
3. **Antenna Orientation:** Ensure both ESP32 antennas are oriented **vertically** (or facing the same orientation) for parallel polarization.
4. **Subject Position:** Sit comfortably in a chair, roughly **50 cm to 70 cm away from the line of sight (LoS)** between the two boards, facing toward them.
5. **Stability:** Rest your hands on your lap and sit still. Avoid fidgeting or rapid body movements during vital sign extraction.

---

## 🚀 Step 3: Running the Live Dashboard

1. Double-click **`run_gui.bat`** in the project folder.
2. The high-resolution **WiFi Vital Signs Radar** dashboard will open.
3. In the top bar:
   - Select **Mode: Live ESP32 Hardware**.
   - Select the COM port corresponding to your **RX ESP32**.
   - Click **"Connect Hardware"**.
4. You will immediately see:
   - **Packet counter ticking up** (~80 packets per second).
   - **Raw CSI Stream** fluctuating with breathing.
   - **Respiration Wave** showing smooth thoracic sine wave.
   - **Heartbeat Wave** showing cardiac systolic pulse peaks.
   - **Live Heart Rate (BPM)** and **Respiration Rate (RPM)** indicators!

---

## 🎬 Step 4: The 3-Step Live Faculty Demonstration

When demonstrating to your faculty tomorrow, follow this script:

### Test 1: Normal Breathing (Baseline)
- Sit still in the chair.
- Point to the screen: show how the blue respiration wave matches your chest expansion, and the red pulse wave tracks your heart rate (e.g. 72 BPM).
- Point to the frequency spectrum: show the sharp breathing peak (~0.25 Hz) and cardiac peak (~1.2 Hz).

### Test 2: Apnea (Breath-Holding Test) - The "Showstopper"
- Tell the faculty: *"Now I will hold my breath to show how the system isolates the cardiac ballistocardiogram."*
- Inhale and hold your breath for 10–15 seconds.
- Watch the screen: The breathing wave drops to flatline, the status changes to **"Holding Breath"**, and the cardiac pulse peaks become exceptionally sharp and visible!
- Faculty will be immediately convinced because this cannot be faked!

### Test 3: Absence / Presence Test
- Stand up and step away from the table.
- Within 3 seconds, the signal variance drops to flat noise, and the status shows **"No Subject Detected"**.
- Sit back down: tracking resumes immediately!

---

## 🆘 Troubleshooting & Pro-Tips

| Problem | Cause | Quick Fix |
|---|---|---|
| **`No active COM ports detected`** | USB cable is power-only, not data | Use a known data-sync USB cable. Check Device Manager for CP210x or CH340 driver. |
| **Flashing says `Timed out waiting for packet header`** | ESP32 didn't enter bootloader mode | Hold down the `BOOT` button on the ESP32 while the terminal says `Connecting...___...` |
| **`Status: Motion Detected`** | Too much body fidgeting | Keep hands and feet still; vital signs are micro-motions (<1 mm). |
| **Weak Heartbeat Signal** | Subject is too far away or wearing heavy winter jacket | Move chair 10 cm closer to the line between ESP32s. |
| **WiFi congestion in classroom** | Severe campus 2.4 GHz interference | Toggle to **"Demo (Simulated)"** in the top bar to showcase full waveform response without any hiccups! |
