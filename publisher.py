import os
import paho.mqtt.client as mqtt
import json
from time import sleep

MQTT_BROKER_HOST = os.environ['MQTT_BROKER_HOST']
MQTT_BROKER_PORT = os.environ['MQTT_BROKER_PORT']
MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_CLIENT_ID = os.environ['MQTT_CLIENT_ID']
UPDATE_INTERVAL = os.environ['UPDATE_INTERVAL']

# TODO subscribe to topic in order to calculate a colorscheme based on a custom value
def mqtt_handler(generator):
    
    GENERATOR_TOPIC = MQTT_TOPIC + "/generate"

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(GENERATOR_TOPIC)

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        # TODO renable when while loop is removed
        #if msg.topic == GENERATOR_TOPIC:
        #    client.publish(MQTT_TOPIC, json.dumps(generator(int(msg.payload))))

    print("MQTT Broker: " + MQTT_BROKER_HOST)
    print("MQTT ClientID: " + MQTT_CLIENT_ID)
    print("MQTT Topic: " + MQTT_TOPIC)

    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT), 60)
    client.loop_start()

    while True:
        client.publish(MQTT_TOPIC, json.dumps(generator()))
        sleep(int(UPDATE_INTERVAL))
