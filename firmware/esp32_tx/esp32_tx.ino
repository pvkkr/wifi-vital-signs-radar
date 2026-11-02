/**
 * WiFi Vital Signs Radar - Transmitter (TX) Node
 * 
 * Target: ESP32 Dev Module
 * Function: Emits high-rate 802.11 OFDM packets on WiFi Channel 11 (80 Hz)
 *           for Channel State Information (CSI) vital sign extraction.
 */

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <esp_wifi.h>
#include <esp_now.h>

#define WIFI_CHANNEL 11
#define PACKET_RATE_HZ 80
#define PACKET_INTERVAL_US (1000000 / PACKET_RATE_HZ)
#define LED_PIN 2

// UDP Configuration
WiFiUDP udp;
const IPAddress broadcastIP(192, 168, 4, 255);
const uint16_t udpPort = 8888;

// Packet Structure
#pragma pack(push, 1)
typedef struct {
    uint16_t magic;      // 0x55AA
    uint32_t seq;        // Packet sequence number
    uint32_t timestamp;  // Timestamp in microseconds
    uint8_t payload[32]; // Padding for standard HT20 OFDM training preamble
} VitalRadarPacket;
#pragma pack(pop)

VitalRadarPacket txPacket;
uint32_t packetCount = 0;
uint32_t lastReportTime = 0;
uint32_t lastLedToggle = 0;
bool ledState = false;

// Broadcast MAC address for ESP-NOW
uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

void setup() {
    Serial.begin(115200);
    delay(500);

    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, HIGH);

    Serial.println("\n=================================================");
    Serial.println("  WiFi Vital Signs Radar - TRANSMITTER (TX)");
    Serial.println("  Carrier: 2.4 GHz WiFi | Channel: 11");
    Serial.println("  Pulse Rate: 80 Hz (Every 12.5 ms)");
    Serial.println("=================================================");

    // 1. Configure WiFi in SoftAP + Station mode on Channel 11
    WiFi.mode(WIFI_AP_STA);
    WiFi.softAP("ESP32_VITAL_RADAR", "12345678", WIFI_CHANNEL, 0, 4);
    
    // Lock WiFi to Channel 11
    esp_wifi_set_promiscuous(true);
    esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);
    esp_wifi_set_promiscuous(false);

    // 2. Initialize ESP-NOW Broadcast as secondary transport
    if (esp_now_init() == ESP_OK) {
        esp_now_peer_info_t peerInfo = {};
        memcpy(peerInfo.peer_addr, broadcastAddress, 6);
        peerInfo.channel = WIFI_CHANNEL;
        peerInfo.encrypt = false;
        esp_now_add_peer(&peerInfo);
        Serial.println("[TX] ESP-NOW broadcast layer active.");
    }

    // 3. Initialize UDP
    udp.begin(udpPort);
    Serial.printf("[TX] SoftAP IP: %s\n", WiFi.softAPIP().toString().c_str());
    Serial.printf("[TX] Broadcasting on Channel %d to port %d...\n", WIFI_CHANNEL, udpPort);

    // Initialize packet payload
    txPacket.magic = 0x55AA;
    for (int i = 0; i < 32; i++) {
        txPacket.payload[i] = (uint8_t)(i * 7 + 0x33);
    }

    digitalWrite(LED_PIN, LOW);
}

void loop() {
    static uint32_t nextSendUs = micros();
    uint32_t nowUs = micros();

    // Transmit packets at fixed 80 Hz rate
    if ((int32_t)(nowUs - nextSendUs) >= 0) {
        nextSendUs += PACKET_INTERVAL_US;

        txPacket.seq = ++packetCount;
        txPacket.timestamp = nowUs;

        // Broadcast via UDP
        udp.beginPacket(broadcastIP, udpPort);
        udp.write((const uint8_t *)&txPacket, sizeof(VitalRadarPacket));
        udp.endPacket();

        // Also broadcast via ESP-NOW for zero-latency direct frame capture
        esp_now_send(broadcastAddress, (uint8_t *)&txPacket, sizeof(VitalRadarPacket));
    }

    // Toggle LED at 1 Hz (500 ms interval)
    uint32_t nowMs = millis();
    if (nowMs - lastLedToggle >= 500) {
        lastLedToggle = nowMs;
        ledState = !ledState;
        digitalWrite(LED_PIN, ledState ? HIGH : LOW);
    }

    // Print diagnostics every 2 seconds
    if (nowMs - lastReportTime >= 2000) {
        lastReportTime = nowMs;
        float actualRate = (float)packetCount * 1000.0f / (float)nowMs;
        Serial.printf("[TX Heartbeat] Sent %u packets (~%.1f pkts/sec) | Ch %d\n", 
                      packetCount, actualRate, WIFI_CHANNEL);
    }
}
