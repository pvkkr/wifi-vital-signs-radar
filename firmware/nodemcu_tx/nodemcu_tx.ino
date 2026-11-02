/**
 * ============================================================================
 * WiFi Vital Signs Radar - High-Power NodeMCU (ESP8266) Transmitter (TX) v2
 * ============================================================================
 * 
 * Target: NodeMCU 1.0 (ESP-12E / ESP8266)
 * Features:
 *   - Blasts continuous raw 802.11 ESP-NOW frames on Channel 11 at 80 Hz.
 *   - Maximum RF output power (+20.5 dBm) to penetrate room and body.
 *   - Calls yield() to keep ESP8266 software watchdog completely happy.
 *   - Blinks onboard LED at 1 Hz to prove continuous transmission.
 * ============================================================================
 */

#include <ESP8266WiFi.h>
extern "C" {
  #include <espnow.h>
}

#define WIFI_CHANNEL 11
#define LED_PIN 2  // Onboard LED on NodeMCU (D4 / GPIO2, Active LOW)

// Broadcast address for ESP-NOW (All devices receive)
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
    Serial.println("  WiFi Vital Signs Radar - NodeMCU (ESP8266) TX");
    Serial.println("  Carrier: 2.4 GHz | Channel: 11 | Power: +20.5 dBm");
    Serial.println("  Rate: 80 Hz Continuous Stream");
    Serial.println("=================================================");

    // 1. Set WiFi mode to Station mode (standard for ESP-NOW on ESP8266)
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    
    // Set Maximum RF output power (+20.5 dBm)
    WiFi.setOutputPower(20.5);

    // Lock to Channel 11
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
    static uint32_t lastSendUs = 0;
    uint32_t nowUs = micros();

    // Transmit packets at fixed 80 Hz rate (12,500 microseconds)
    if (nowUs - lastSendUs >= 12500) {
        lastSendUs = nowUs;

        txPacket.seq = ++packetCount;
        txPacket.timestamp = nowUs;

        // Blast raw 802.11 ESP-NOW frame directly onto Channel 11
        esp_now_send(broadcastMac, (uint8_t *)&txPacket, sizeof(VitalRadarPacket));
    }

    // Toggle onboard LED at 2 Hz to show active transmission
    uint32_t nowMs = millis();
    if (nowMs - lastLedToggle >= 250) {
        lastLedToggle = nowMs;
        ledState = !ledState;
        digitalWrite(LED_PIN, ledState ? LOW : HIGH); // Active LOW
    }

    // Diagnostics every 2 seconds
    if (nowMs - lastReportTime >= 2000) {
        lastReportTime = nowMs;
        float actualRate = (float)packetCount * 1000.0f / (float)nowMs;
        Serial.printf("[NodeMCU TX] Blasting %u pkts (~%.1f Hz) on Ch %d | RF: 20.5 dBm\n", 
                      packetCount, actualRate, WIFI_CHANNEL);
    }

    // Essential: Feed ESP8266 background tasks and watchdog timer
    yield();
}
