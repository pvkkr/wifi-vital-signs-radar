/**
 * WiFi Vital Signs Radar - High-Selectivity ESP32 Receiver (RX) Node
 * 
 * Target: ESP32 Dev Module
 * Features:
 * - Locks radio strictly to Channel 11 without channel scanning
 * - Hardware CSI demodulator on HT20 OFDM training sequence
 * - Rejects distant router noise (RSSI < -80 dBm)
 * - Streams high-speed formatted CSI telemetry over UART to PC
 */

#include <Arduino.h>
#include <WiFi.h>
#include "esp_wifi.h"
#include <esp_now.h>

#define WIFI_CHANNEL 11
#define LED_PIN 2
#define NUM_SUBCARRIERS_STREAM 16
#define MIN_RSSI_THRESHOLD -80  // Reject faint distant campus router beacons

static volatile uint32_t csiPacketCount = 0;
static volatile uint32_t lastPacketTimeMs = 0;
static uint32_t lastDiagTime = 0;

// Subcarrier indices evenly distributed across active OFDM subcarriers
static const int streamSubcarrierIndices[NUM_SUBCARRIERS_STREAM] = {
    6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 60, 62
};

// Hardware CSI Interrupt Callback
void IRAM_ATTR wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *info) {
    if (!info || !info->buf || info->len < 128) {
        return;
    }

    int8_t rssi = info->rx_ctrl.rssi;

    // Filter out weak background noise from campus routers down the hall
    if (rssi < MIN_RSSI_THRESHOLD) {
        return;
    }

    csiPacketCount++;
    lastPacketTimeMs = millis();

    int8_t *csi_raw = info->buf;
    float totalAmp = 0.0f;
    float selectedAmps[NUM_SUBCARRIERS_STREAM];

    for (int i = 0; i < NUM_SUBCARRIERS_STREAM; i++) {
        int scIdx = streamSubcarrierIndices[i];
        if (scIdx * 2 + 1 < info->len) {
            float imag = (float)csi_raw[scIdx * 2];
            float real = (float)csi_raw[scIdx * 2 + 1];
            float amp = sqrtf(real * real + imag * imag);
            selectedAmps[i] = amp;
            totalAmp += amp;
        } else {
            selectedAmps[i] = 0.0f;
        }
    }

    float meanAmp = totalAmp / (float)NUM_SUBCARRIERS_STREAM;

    // Stream formatted telemetry line over Serial
    // Format: CSI,<seq>,<time_ms>,<rssi>,<mean_amp>,<sc0>,...,<sc15>
    Serial.printf("CSI,%u,%u,%d,%.2f", csiPacketCount, millis(), rssi, meanAmp);
    for (int i = 0; i < NUM_SUBCARRIERS_STREAM; i++) {
        Serial.printf(",%.2f", selectedAmps[i]);
    }
    Serial.println();
}

void setup() {
    Serial.begin(115200);
    delay(400);

    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, HIGH);

    Serial.println("\n=================================================");
    Serial.println("  WiFi Vital Signs Radar - High-Selectivity RX");
    Serial.println("  Locked to Channel: 11 | Noise Rejection: ACTIVE");
    Serial.println("  Format: CSI,<seq>,<time_ms>,<rssi>,<mean>,<sc0..sc15>");
    Serial.println("=================================================");

    // 1. Initialize WiFi in Station mode locked to Channel 11
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    esp_wifi_set_promiscuous(true);
    esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

    // Initialize ESP-NOW layer
    esp_now_init();

    // 2. Configure CSI extraction
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

    Serial.println("[RX] CSI demodulator active. Waiting for NodeMCU TX...");
    digitalWrite(LED_PIN, LOW);
}

void loop() {
    uint32_t nowMs = millis();

    // Toggle LED on active local CSI packet reception
    if (nowMs - lastPacketTimeMs < 100) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    // Diagnostic log every 3 seconds
    if (nowMs - lastDiagTime >= 3000) {
        lastDiagTime = nowMs;
        if (nowMs - lastPacketTimeMs > 2000) {
            Serial.printf("[RX Status] Waiting for NodeMCU on Channel %d... (Received: %u)\n", 
                          WIFI_CHANNEL, csiPacketCount);
        } else {
            Serial.printf("[RX Status] Streaming vital signals! Total: %u packets\n", 
                          csiPacketCount);
        }
    }

    delay(10);
}
