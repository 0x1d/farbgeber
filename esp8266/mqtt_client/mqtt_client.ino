/*
 ESP8266 Farbgeber client

 Author: coon@c-base.org
 Last Maintenance: 06. May 2017
 
 Description: Connects to a WIFI and connectcs to a MQTT server and acts as 
 a client for the farbgeber.

 - Modify config.h first but do not check it in into github!
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>
#include "config.h"

#define LEDS_PER_GROUP NUM_LEDS / NUM_GROUPS

// Modify the following variables in config.h:
// ---------------------------------------------
extern const char* wifi_ssid;
extern const char* wifi_password;
extern const char* mqtt_server;
extern const char* mqtt_topic;
// ---------------------------------------------

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, DATA_PIN, NEO_GRB + NEO_KHZ800);


typedef struct Color {
  unsigned char red;
  unsigned char green;
  unsigned char blue;
};

void setLedGroupColor(int group, Color color) {
  int startLed = group * LEDS_PER_GROUP;
  int brightnessDivider = 1;

  color.red   /= brightnessDivider;
  color.green /= brightnessDivider;
  color.blue  /= brightnessDivider;
    
  for(int i = startLed; i < startLed + LEDS_PER_GROUP; i++)    
    strip.setPixelColor(i, strip.Color(color.red, color.green, color.blue));

  strip.show();
  delayMicroseconds(100); // avoid glichtes (do not set below 100us)
}

Color extractColorFromJson(const JsonObject& json, const char* pKey) {
  Color c;

  c.red   = json[pKey][0];
  c.green = json[pKey][1];
  c.blue  = json[pKey][2];

  return c;
}

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
    
  pinMode(BUILTIN_LED, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  long lastMsg = 0;
  char msg[50];
  int value = 0;

  while(true) {
    if (!client.connected())
      reconnect();
  
    client.loop();

    long now = millis();
    if (now - lastMsg > 2000) {
      lastMsg = now;
      ++value;
      snprintf (msg, 75, "Heartbeat #%ld", value);
      Serial.println(msg);
    }
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void printColor(const char* pDescription, struct Color color) {
  char pBuf[128];
  snprintf(pBuf, sizeof(pBuf) - 1, 
    "%s color: #%02X%02X%02X", pDescription, 
    color.red, color.green, color.blue);
  
  Serial.println(pBuf);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println(topic);
  StaticJsonBuffer<2048> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(payload);

  if (!root.success()) {
    Serial.println("parseObject() failed");
    return;
  }

  Color base;
  Color variant[5];
  Color contrast;

  base       = extractColorFromJson(root, "b");
  variant[0] = extractColorFromJson(root, "v1");
  variant[1] = extractColorFromJson(root, "v2");
  variant[2] = extractColorFromJson(root, "v3");
  variant[3] = extractColorFromJson(root, "v4");
  variant[4] = extractColorFromJson(root, "v5");
  contrast   = extractColorFromJson(root, "c");
  
  printColor("Base     ", base);
  printColor("Variant 1", variant[0]);
  printColor("Variant 2", variant[1]);
  printColor("Variant 3", variant[2]);
  printColor("Variant 4", variant[3]);
  printColor("Contrast ", contrast);

  setLedGroupColor(0, base);
  setLedGroupColor(1, variant[0]);
  setLedGroupColor(2, variant[1]);
  setLedGroupColor(3, variant[2]);
  setLedGroupColor(4, variant[3]);
  setLedGroupColor(5, contrast);
}

void reconnect() {  
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("farbgeber_client")) {
      Serial.println("connected");      
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  // DO NOT USE
}
