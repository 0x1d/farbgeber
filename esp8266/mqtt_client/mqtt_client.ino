/*
 Basic ESP8266 MQTT example

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library.

 It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

#define PIN D8
#define NUM_LEDS 6 // 150
#define NUM_GROUPS 6 // base + variant1,2,3,4 + contrast
#define LEDS_PER_GROUP NUM_LEDS / NUM_GROUPS

// Update these with values suitable for your network.

const char* ssid = "<enter ssid here>";
const char* password = "<enter password here>";
const char* mqtt_server = "iot.eclipse.org";

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);
long lastMsg = 0;
char msg[50];
int value = 0;

typedef struct Color {
  unsigned char red;
  unsigned char green;
  unsigned char blue;
} ;

typedef struct ColorElements {
  char pBinary[8];
  Color base;
  Color variant[4];
  Color contrast;
};

void setLedGroupColor(int group, Color color) {
  int startLed = group * LEDS_PER_GROUP;
  int brightnessDivider = 32;

  color.red   /= brightnessDivider;
  color.green /= brightnessDivider;
  color.blue  /= brightnessDivider;
    
  for(int i = startLed; i < startLed + LEDS_PER_GROUP; i++)    
    strip.setPixelColor(i, strip.Color(color.red, color.green, color.blue));

  strip.show();
  delayMicroseconds(100); // avoid glichtes (do not set below 100us)
}

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
    
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

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
  if (length != sizeof(ColorElements)) {
    Serial.println("Invalid packet format!");
       
    return;
  }

  Serial.println(topic);

  const ColorElements* pColors = (ColorElements*)payload;
  printColor("Base     ", pColors->base);
  printColor("Variant 1", pColors->variant[0]);
  printColor("Variant 2", pColors->variant[1]);
  printColor("Variant 3", pColors->variant[2]);
  printColor("Variant 4", pColors->variant[3]);
  printColor("Contrast ", pColors->contrast);

  setLedGroupColor(0, pColors->base);
  setLedGroupColor(1, pColors->variant[0]);
  setLedGroupColor(2, pColors->variant[1]);
  setLedGroupColor(3, pColors->variant[2]);
  setLedGroupColor(4, pColors->variant[3]);
  setLedGroupColor(5, pColors->contrast);
}

void reconnect() {  
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("farbgeber_client")) {
      Serial.println("connected");      
      client.subscribe("c-base/farbgeber");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "Heartbeat #%ld", value);
    Serial.println(msg);
  }
}
