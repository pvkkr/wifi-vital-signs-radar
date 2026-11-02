/**
 * WiFi Vital Signs Radar - High-Power NodeMCU (ESP8266) Transmitter (TX)
 * 
 * Target: NodeMCU 1.0 (ESP-12E / ESP8266)
 * Uses ESP-NOW broadcast + UDP to emit high-power (+20.5 dBm) 802.11 frames
 * on Channel 11 at 80 Hz. Connectionless: Blasts packets immediately on power-up!
 */

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
extern "C" {
  #include <espnow.h>
}

#define WIFI_CHANNEL 11
#define PACKET_RATE_HZ 80
#define PACKET_INTERVAL_US (1000000 / PACKET_RATE_HZ)
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

WiFiUDP udp;
const IPAddress broadcastIP(255, 255, 255, 255);
const uint16_t udpPort = 8888;

void setup() {
    Serial.begin(115200);
    delay(300);

    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW); // LED ON

    Serial.println("\n=================================================");
    Serial.println("  WiFi Vital Signs Radar - NodeMCU (ESP8266) TX");
    Serial.println("  Carrier: 2.4 GHz | Channel: 11 | Power: +20.5 dBm MAX");
    Serial.println("  Protocol: ESP-NOW Broadcast @ 80 Hz");
    Serial.println("=================================================");

    // 1. Set WiFi mode to Station mode (standard for ESP-NOW) on Channel 11
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    
    // Set Maximum RF output power (+20.5 dBm) to overpower room router noise
    WiFi.setOutputPower(20.5);

    // Lock to Channel 11
    wifi_set_channel(WIFI_CHANNEL);

    // 2. Initialize ESP-NOW
    if (esp_now_init() != 0) {
        Serial.println("[TX ERROR] ESP-NOW initialization failed!");
    } else {
        Serial.println("[TX] ESP-NOW initialized successfully.");
        esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
        esp_now_add_peer(broadcastMac, ESP_NOW_ROLE_SLAVE, WIFI_CHANNEL, NULL, 0);
    }

    // 3. Initialize UDP as dual-beacon
    udp.begin(udpPort);

    // Fill packet
    txPacket.magic = 0x55AA;
    for (int i = 0; i < 32; i++) {
        txPacket.payload[i] = (uint8_t)(i * 11 + 0x5A);
    }

    digitalWrite(LED_PIN, HIGH); // LED OFF
}

void loop() {
    static uint32_t nextSendUs = micros();
    uint32_t nowUs = micros();

    // Transmit packets at fixed 80 Hz rate
    if ((int32_t)(nowUs - nextSendUs) >= 0) {
        nextSendUs += PACKET_INTERVAL_US;

        txPacket.seq = ++packetCount;
        txPacket.timestamp = nowUs;

        // Blast ESP-NOW packet directly onto Channel 11
        esp_now_send(broadcastMac, (uint8_t *)&txPacket, sizeof(VitalRadarPacket));

        // Also blast UDP broadcast
        udp.beginPacket(broadcastIP, udpPort);
        udp.write((const uint8_t *)&txPacket, sizeof(VitalRadarPacket));
        udp.endPacket();
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
}
