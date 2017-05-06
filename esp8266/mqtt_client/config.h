// -------------------------------------------------------------
// !WARNING! >> DO NOT CHECK IN THIS FILE INTO GIT! << !WARNING!
// -------------------------------------------------------------

// WIFI:
const char* wifi_ssid = <put ssid here>
const char* wifi_password = <put wifi password here>

// MQTT:
const char* mqtt_server = <put mqtt server address here>
const char* mqtt_topic = <put farbgeber mqtt topic to subscribe to>

// LED stripe:
#define DATA_PIN 4 // Data pin where LED stripe is connected on Node MCU
#define NUM_LEDS 60 // Number of LEDs on the stripe
#define NUM_GROUPS 6 // base + variant1,2,3,4 + contrast


