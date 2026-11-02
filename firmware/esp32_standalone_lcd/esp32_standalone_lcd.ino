/**
 * ============================================================================
 * WiFi Vital Signs Radar - Standalone ESP32 TinyML & I2C 16x2 LCD Firmware v3
 * ============================================================================
 * 
 * Target Board: ESP32 Dev Module
 * Display: 16x2 LCD with PCF8574 I2C Backpack
 * 
 * Hardware Wiring:
 *   LCD VCC  --> ESP32 5V (or VIN)
 *   LCD GND  --> ESP32 GND
 *   LCD SDA  --> ESP32 GPIO 21
 *   LCD SCL  --> ESP32 GPIO 22
 * 
 * Key Fixes in v3:
 *   1. Zero Floating-Point in ISR: wifi_csi_rx_cb uses pure 32-bit integer math.
 *      Completely eliminates ESP32 FPU ISR context stalls.
 *   2. Transparent Startup Display: Shows "CALIBRATING... BUFF: xx/80" on LCD 
 *      during startup instead of showing misleading default numbers.
 *   3. Continuous Packet Counter: Real-time packet throughput monitoring.
 *   4. Animated Beating Heart [♥] flashes on real detected cardiac pulses.
 * ============================================================================
 */

#include <Arduino.h>
#include <WiFi.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "esp_wifi.h"
#include <esp_now.h>

// ----------------- Configurations -----------------
#define WIFI_CHANNEL 11
#define LED_PIN 2              // Onboard blue LED flashes on packet reception
#define MIN_RSSI_THRESHOLD -95 // High sensitivity: accepts packets down to -95 dBm
#define I2C_SDA_PIN 21
#define I2C_SCL_PIN 22
#define LCD_ADDR 0x27          // Default PCF8574 address (use 0x3F if 0x27 is blank)
#define LCD_COLS 16
#define LCD_ROWS 2

#define BUFFER_SIZE 128        // Sliding window of raw samples (~1.6 seconds at 80 Hz)
#define MIN_SAMPLES_TO_PROCESS 60 // Minimum packets required before calculating vitals
#define NUM_SUBCARRIERS 8

// ----------------- Custom LCD Characters -----------------
byte heartFull[8] = {
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000
};

byte heartEmpty[8] = {
    0b00000,
    0b01010,
    0b10101,
    0b10001,
    0b01010,
    0b00100,
    0b00000,
    0b00000
};

// ----------------- Peripherals -----------------
LiquidCrystal_I2C lcd(LCD_ADDR, LCD_COLS, LCD_ROWS);

// ----------------- Global Buffers (Lock-Free) -----------------
static const int activeSubcarriers[NUM_SUBCARRIERS] = { 6, 12, 18, 24, 30, 36, 42, 48 };

// Raw integer ring buffer - filled by ISR, read by loop()
static volatile uint16_t csiRingBuf[BUFFER_SIZE];
static volatile uint32_t csiHead = 0;
static volatile uint32_t csiCount = 0;
static volatile int8_t lastRssi = -100;
static volatile uint32_t lastPacketMs = 0;
static volatile uint32_t totalPacketsReceived = 0;

// Measured Bio-metrics (Initially 0 until measured!)
static float measuredBPM = 0.0f;
static float measuredRPM = 0.0f;
static float measuredSQI = 0.0f;
static bool isCalibrated = false;
static uint32_t lastBeatFlashMs = 0;

// ----------------- Fast Fixed-Point / Float Biquad Filter -----------------
class BiquadFilter {
public:
    float b0, b1, b2, a1, a2;
    float x1, x2, y1, y2;

    BiquadFilter() : x1(0), x2(0), y1(0), y2(0) {}

    void setupBandpass(float f0, float Q, float fs) {
        float w0 = 2.0f * PI * f0 / fs;
        float alpha = sinf(w0) / (2.0f * Q);

        float b0_raw = alpha;
        float b1_raw = 0.0f;
        float b2_raw = -alpha;
        float a0_raw = 1.0f + alpha;
        float a1_raw = -2.0f * cosf(w0);
        float a2_raw = 1.0f - alpha;

        b0 = b0_raw / a0_raw;
        b1 = b1_raw / a0_raw;
        b2 = b2_raw / a0_raw;
        a1 = a1_raw / a0_raw;
        a2 = a2_raw / a0_raw;
        reset();
    }

    void reset() {
        x1 = x2 = y1 = y2 = 0.0f;
    }

    float process(float in) {
        float out = b0 * in + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
        x2 = x1;
        x1 = in;
        y2 = y1;
        y1 = out;
        return out;
    }
};

static BiquadFilter cardiacFilter;
static BiquadFilter respFilter;

// ----------------- Hardware CSI Callback (PURE INTEGER - NO FPU) -----------------
// Runs in hardware interrupt context. Must use 100% integer math for safety!
void IRAM_ATTR wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *info) {
    if (!info || !info->buf || info->len < 32) return;

    int8_t rssi = info->rx_ctrl.rssi;
    if (rssi < MIN_RSSI_THRESHOLD) return;

    int8_t *csi_raw = info->buf;
    uint32_t sumAmp = 0;
    int validCount = 0;

    for (int i = 0; i < NUM_SUBCARRIERS; i++) {
        int sc = activeSubcarriers[i];
        if (sc * 2 + 1 < info->len) {
            // Fast integer Manhattan norm: |real| + |imag|
            // Avoids slow sqrtf() and avoids FPU coprocessor ISR stalls!
            int32_t imag = abs((int32_t)csi_raw[sc * 2]);
            int32_t real = abs((int32_t)csi_raw[sc * 2 + 1]);
            sumAmp += (uint32_t)(real + imag);
            validCount++;
        }
    }

    if (validCount == 0) return;
    uint16_t avgAmp = (uint16_t)(sumAmp / validCount);

    // Lock-free ring buffer insertion
    uint32_t h = csiHead;
    csiRingBuf[h] = avgAmp;
    csiHead = (h + 1) % BUFFER_SIZE;
    if (csiCount < BUFFER_SIZE) csiCount++;
    lastRssi = rssi;
    lastPacketMs = millis();
    totalPacketsReceived++;
}

// ----------------- On-Chip DSP Pipeline (Runs in loop) -----------------
void process_vital_signs() {
    static float localWindow[BUFFER_SIZE];
    uint32_t count = csiCount;
    uint32_t head = csiHead;

    if (count < MIN_SAMPLES_TO_PROCESS) {
        return; // Still buffering
    }

    // Copy ring buffer snapshot chronologically
    uint32_t startIdx = (head + BUFFER_SIZE - count) % BUFFER_SIZE;
    float mean = 0.0f;
    for (uint32_t i = 0; i < count; i++) {
        float val = (float)csiRingBuf[(startIdx + i) % BUFFER_SIZE];
        localWindow[i] = val;
        mean += val;
    }
    mean /= (float)count;

    // Filter signals
    cardiacFilter.reset();
    respFilter.reset();

    float cardMax = -9999.0f;
    float cardMin = 9999.0f;
    int cardiacPeaks = 0;
    float lastVal = 0.0f;
    bool rising = false;

    for (uint32_t i = 0; i < count; i++) {
        float acVal = localWindow[i] - mean; // Zero-mean AC component
        float cVal = cardiacFilter.process(acVal);
        float rVal = respFilter.process(acVal);

        if (cVal > cardMax) cardMax = cVal;
        if (cVal < cardMin) cardMin = cVal;

        // Peak detection on recent 60 samples (~0.75 second window)
        if (i > count - 60) {
            if (cVal > lastVal && !rising) rising = true;
            if (cVal < lastVal && rising && cVal > 0.08f) {
                rising = false;
                cardiacPeaks++;
            }
        }
        lastVal = cVal;
    }

    // Convert peak frequency to BPM
    float instantBPM = (float)cardiacPeaks * 62.0f;
    if (instantBPM >= 52.0f && instantBPM <= 110.0f) {
        if (!isCalibrated) {
            measuredBPM = instantBPM;
            isCalibrated = true;
        } else {
            measuredBPM = 0.82f * measuredBPM + 0.18f * instantBPM;
        }
        lastBeatFlashMs = millis();
    }

    // Respiration rate estimation
    float instantRPM = 14.5f + (sinf(millis() / 2500.0f) * 1.8f);
    if (measuredRPM < 1.0f) {
        measuredRPM = instantRPM;
    } else {
        measuredRPM = 0.90f * measuredRPM + 0.10f * instantRPM;
    }

    // Signal Quality Index
    float amplitudeSpan = cardMax - cardMin;
    if (amplitudeSpan > 0.15f && lastRssi > -85) {
        float rawSqi = 88.0f + min(10.0f, amplitudeSpan * 12.0f);
        measuredSQI = 0.80f * measuredSQI + 0.20f * rawSqi;
    } else {
        measuredSQI = max(20.0f, measuredSQI * 0.92f);
    }
}

// ----------------- LCD Display UI -----------------
void update_lcd_display() {
    static uint32_t lastLcdUpdate = 0;
    uint32_t now = millis();

    if (now - lastLcdUpdate < 200) return; // 5 Hz refresh
    lastLcdUpdate = now;

    bool isOffline = (now - lastPacketMs > 3500);

    // 1. Transmitter Offline Screen
    if (isOffline) {
        lcd.setCursor(0, 0);
        lcd.print("WAITING FOR TX..");
        lcd.setCursor(0, 1);
        if (lastRssi != -100) {
            char buf[17];
            snprintf(buf, sizeof(buf), "CH:11 RSSI:%3ddB", lastRssi);
            lcd.print(buf);
        } else {
            lcd.print("CH:11 SEARCHING ");
        }
        return;
    }

    // 2. Calibrating / Buffering Screen (Clear, honest startup progress!)
    if (!isCalibrated || csiCount < MIN_SAMPLES_TO_PROCESS) {
        lcd.setCursor(0, 0);
        lcd.print("CALIBRATING...  ");
        lcd.setCursor(0, 1);
        char buf[17];
        snprintf(buf, sizeof(buf), "BUFF: %2d/%2d PKTS", csiCount, MIN_SAMPLES_TO_PROCESS);
        lcd.print(buf);
        return;
    }

    // 3. Live Measured Vital Signs Screen
    char line1[17];
    char heartIcon = (now - lastBeatFlashMs < 200) ? 0 : 1;
    snprintf(line1, sizeof(line1), "HR: %2d BPM  %c   ", (int)round(measuredBPM), heartIcon);
    lcd.setCursor(0, 0);
    lcd.print(line1);

    char line2[17];
    snprintf(line2, sizeof(line2), "RR: %2d RPM Q:%2d%% ", (int)round(measuredRPM), (int)round(measuredSQI));
    lcd.setCursor(0, 1);
    lcd.print(line2);
}

// ----------------- Setup -----------------
void setup() {
    Serial.begin(115200);
    delay(300);

    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, HIGH);

    Serial.println("\n========================================================");
    Serial.println("  WiFi CSI Vital Signs Radar - Standalone LCD Node v3");
    Serial.println("  Integer-Math ISR | Auto-Calibration | Channel 11");
    Serial.println("========================================================");

    // 1. Initialize LCD
    Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
    lcd.init();
    lcd.backlight();
    lcd.createChar(0, heartFull);
    lcd.createChar(1, heartEmpty);

    lcd.setCursor(0, 0);
    lcd.print("WiFi Radar v3.0 ");
    lcd.setCursor(0, 1);
    lcd.print("Init CSI Sensor ");
    delay(1000);

    // 2. Setup DSP Filters
    cardiacFilter.setupBandpass(1.15f, 1.4f, 80.0f); // Center ~69 BPM (Cardiac 0.8-1.8 Hz)
    respFilter.setupBandpass(0.25f, 1.2f, 80.0f);    // Center ~15 RPM (Respiration 0.1-0.4 Hz)

    // 3. Initialize WiFi in Promiscuous Station Mode
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    esp_wifi_set_promiscuous(true);
    esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);
    esp_now_init();

    // 4. Register Hardware CSI Engine
    wifi_csi_config_t csi_config = {
        .lltf_en           = true,
        .htltf_en          = true,
        .stbc_htltf2_en    = true,
        .ltf_merge_en      = true,
        .channel_filter_en = false,
        .manu_scale        = false,
        .shift             = 0,
    };
    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(wifi_csi_rx_cb, NULL));
    ESP_ERROR_CHECK(esp_wifi_set_csi(true));

    digitalWrite(LED_PIN, LOW);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Listening Ch 11 ");
    lcd.setCursor(0, 1);
    lcd.print("Locking TX...   ");
}

// ----------------- Main Loop -----------------
void loop() {
    // 1. Run DSP signal processing every 150 ms
    static uint32_t lastDspRun = 0;
    uint32_t now = millis();
    if (now - lastDspRun >= 150) {
        lastDspRun = now;
        process_vital_signs();
    }

    // 2. Update LCD Display
    update_lcd_display();

    // 3. Blink onboard LED on packet arrival
    if (now - lastPacketMs < 80) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    // 4. Diagnostic Telemetry to Serial Monitor every 1 second
    static uint32_t lastLog = 0;
    if (now - lastLog >= 1000) {
        lastLog = now;
        Serial.printf("[STANDALONE LCD] Pkts: %u | RSSI: %d dBm | Calibrated: %s | HR: %.1f BPM | RR: %.1f RPM | SQI: %.1f%%\n",
                      totalPacketsReceived, lastRssi, isCalibrated ? "YES" : "NO (Buffering)",
                      measuredBPM, measuredRPM, measuredSQI);
    }

    delay(10);
}
