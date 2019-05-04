import paho.mqtt.client as mqtt
import struct 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("c-base/#")
    client.subscribe("c-base/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = struct.Struct('7s B BBB BBB BBB BBB BBB BBB').unpack(msg.payload)

    print("Topic: " + msg.topic)
    print("Base color: #%02X%02X%02X" % (data[2],  data[3],  data[4])) 
    print("Variant 1:  #%02X%02X%02X" % (data[5],  data[6],  data[7]))
    print("Variant 2:  #%02X%02X%02X" % (data[8],  data[9],  data[10]))
    print("Variant 3:  #%02X%02X%02X" % (data[11], data[12], data[13]))
    print("Variant 4:  #%02X%02X%02X" % (data[14], data[15], data[16]))
    print("Contrast:   #%02X%02X%02X" % (data[17], data[18], data[19]))
    print("")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("broker.mqttdashboard.com", 8000, 60)
client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

