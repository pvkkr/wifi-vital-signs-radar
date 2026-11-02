/**
 * ============================================================================
 * WiFi Vital Signs Radar - High-Power NodeMCU (ESP8266) Transmitter (TX) v3
 * ============================================================================
 * 
 * Target: NodeMCU 1.0 (ESP-12E / ESP8266)
 * Features:
 *   - Stable 80 Hz transmission using delay(12) with microsecond precision.
 *   - Continuous RF output (+20.5 dBm) without WiFi baseband starvation.
 *   - Runs 24/7 indefinitely without freezing or requiring USB power resets.
 * ============================================================================
 */

#include <ESP8266WiFi.h>
extern "C" {
  #include <espnow.h>
}

#define WIFI_CHANNEL 11
#define LED_PIN 2  // Onboard LED on NodeMCU (D4 / GPIO2, Active LOW)

static uint8_t broadcastMac[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

#pragma pack(push, 1)
typedef struct {
    uint16_t magic;      // 0x55AA
    uint32_t seq;        // Packet sequence number
    uint32_t timestamp;  // Timestamp in microseconds
    uint8_t payload[32]; // High-entropy payload for clear OFDM channel estimation
} VitalRadarPacket;
#pragma pack(pop)

VitalRadarPacket txPacket;
uint32_t packetCount = 0;
uint32_t lastReportTime = 0;
uint32_t lastLedToggle = 0;
bool ledState = false;

void setup() {
    Serial.begin(115200);
    delay(300);

    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW); // LED ON during boot

    Serial.println("\n=================================================");
    Serial.println("  WiFi Vital Signs Radar - NodeMCU (ESP8266) TX v3");
    Serial.println("  Carrier: 2.4 GHz | Channel: 11 | Power: +20.5 dBm");
    Serial.println("  Continuous 80 Hz Non-Stop Transmission");
    Serial.println("=================================================");

    // 1. Station Mode on Channel 11
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    WiFi.setOutputPower(20.5);
    wifi_set_channel(WIFI_CHANNEL);

    // 2. Initialize ESP-NOW
    if (esp_now_init() != 0) {
        Serial.println("[TX ERROR] ESP-NOW initialization failed!");
        return;
    }

    Serial.println("[TX] ESP-NOW initialized successfully.");
    esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
    esp_now_add_peer(broadcastMac, ESP_NOW_ROLE_SLAVE, WIFI_CHANNEL, NULL, 0);

    // Fill packet
    txPacket.magic = 0x55AA;
    for (int i = 0; i < 32; i++) {
        txPacket.payload[i] = (uint8_t)(i * 11 + 0x5A);
    }

    digitalWrite(LED_PIN, HIGH); // LED OFF
}

void loop() {
    // 80 Hz beacon: exactly 12.5 milliseconds per packet
    static uint32_t lastSendUs = 0;
    uint32_t nowUs = micros();

    if (nowUs - lastSendUs >= 12500) {
        lastSendUs = nowUs;

        txPacket.seq = ++packetCount;
        txPacket.timestamp = nowUs;

        // Transmit raw 802.11 ESP-NOW broadcast frame
        esp_now_send(broadcastMac, (uint8_t *)&txPacket, sizeof(VitalRadarPacket));
    }

    // Toggle onboard LED at 2 Hz
    uint32_t nowMs = millis();
    if (nowMs - lastLedToggle >= 250) {
        lastLedToggle = nowMs;
        ledState = !ledState;
        digitalWrite(LED_PIN, ledState ? LOW : HIGH);
    }

    // Print diagnostics to USB Serial every 3 seconds
    if (nowMs - lastReportTime >= 3000) {
        lastReportTime = nowMs;
        float actualRate = (float)packetCount * 1000.0f / (float)nowMs;
        Serial.printf("[NodeMCU TX] Total: %u pkts (~%.1f Hz) on Ch %d | RF: 20.5 dBm\n", 
                      packetCount, actualRate, WIFI_CHANNEL);
    }

    // Give 1ms to ESP8266 background WiFi stack to prevent RF synthesizer lockup
    delay(1);
}
