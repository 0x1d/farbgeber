# farbgeber

## About
A central color generator to provide a uniform colorscheme that is harmonious, yet dynamically changing the color.

The color generator is a color Inklusionist and makes sure that all colors of the rainbow are represented equally often and the same length. It produces 6 colors for every second in an hour. Of these 5 colors are very similar and can be used for gradients or backgrounds with movement. The 6th color is in a harmony contrast with the first color and should be used only a little and as a contrast. Rule of thumb: 90-100% of the LEDs should be in one of the 5 basic variations and 0-10% in the contrasting color.

## Fork Info
Forked from [c-base/farbgeber](https://github.com/0x1d/farbgeber).  
  
Difference to c-base farbgeber:  
- runs on Docker
- connects to a MQTT broker to publish the colorscheme
- generates the current scheme as HTML to /output/farbgeber.html
- send the colors either as RGB array or Hex
- MsgFlo support dropped for now (will be added again maybe)

## Getting Started
Create a .env file and configure your environment
```
MQTT_PUBLISHER=1
MQTT_BROKER_HOST=broker
MQTT_BROKER_PORT=1883
MQTT_TOPIC=wirelos/farbgeber
MQTT_CLIENT_ID=farbgeber
UPDATE_INTERVAL=60
SCHEME_FORMAT=HEX
GENERATE_HTML=1
HTML_OUTPUT_PATH=/output/farbgeber.html
```
Build and Run with Docker:
```
docker build -t wirelos/farbgeber .
docker run -d --env-file=.env  wirelos/farbgeber
```
or docker-compose:
```
docker-compose up -d --build
```

## Example Output
RGB:
```
{
	"c": [206, 71, 235],
	"b": [35, 204, 0],
	"v1": [20, 184, 21],
	"v2": [78, 184, 20],
	"v3": [42, 240, 0],
	"v4": [29, 168, 0]
}
```

Hex:
```
{
	"t": 516.0, 
	"b": "#ccaf00", 
	"v1": "#b1b814", 
	"v2": "#b88314", 
	"v3": "#f0ce00", 
	"v4": "#a89100", 
	"c": "#475eeb"
}
```