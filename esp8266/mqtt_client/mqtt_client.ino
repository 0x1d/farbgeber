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

// Update these with values suitable for your network.

const char* ssid = "<put ssid here>";
const char* password = "<put password here>";
const char* mqtt_server = "iot.eclipse.org";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
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
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("farbgeber_client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("c-base/farbgeber");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
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
    // client.publish("outTopic", msg);
  }
}
