#!/usr/bin/python
# coding=utf-8

import time
import struct
import paho.mqtt.client as mqtt
from time import gmtime, strftime
from colour import Color


# zentraler zeitgeber, sollte immer <3600 und >0 sein und integer raustun

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("c-base/#")
    client.subscribe("c-base/#")

    # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def create_mqtt_publisher(broker_address, port, client_id, topic):
  mc = mqtt.Client(client_id)
  mc.on_connect = on_connect
  mc.on_message = on_message
  mc.connect(broker_address, port)

  return mc

def generate_terminal_output(base_color, base_color_variant_1, base_color_variant_2, base_color_variant_3, base_color_variant_4, contrast_color, time_value):
    print time_value
    print "base_color ", base_color.hex
    print "baseColorVariant1 ", base_color_variant_1.hex
    print "baseColorVariant2 ", base_color_variant_2.hex
    print "baseColorVariant3 ", base_color_variant_3.hex
    print "baseColorVariant4 ", base_color_variant_4.hex
    print "contrast_color ", contrast_color.hex
    print "###################################"


def generate_html_output(base_color, base_color_variant_1, base_color_variant_2, base_color_variant_3,
                         base_color_variant_4, contrast_color, time_value):
    # Weboutput
    htmlpreface = """<html><head><title>visuelle Ausgabeeinheit des zentralen Farbgebers</title><meta http-equiv="refresh" content="1" />
    <style type="text/css">
    """
    htmlcontent = """</style></head><body><h1>visuelle Ausgabeeinheit des zentralen Farbgebers</h1>
    <div>BaseColor """ + base_color.hex + """</div></ br>
    <div class="base_color_variant_1">baseColorVariant1 """ + base_color_variant_1.hex + """</div>
    <div class="base_color_variant_2">baseColorVariant2 """ + base_color_variant_2.hex + """</div>
    <div class="base_color_variant_3">baseColorVariant3 """ + base_color_variant_3.hex + """</div>
    <div class="base_color_variant_4">baseColorVariant4 """ + base_color_variant_4.hex + """</div>
    <div class="Contrastcolor">Contrastcolor """ + contrast_color.hex + """</div>"""
    zeitzeile = "<h3>Color-Seed " + str(time_value) + " " + strftime("%H:%M:%S", gmtime()) + "Uhr</h3>"
    htmlclosing = """</body></html>"""
    css1 = "body { font-size:20px; background-color:" + base_color.hex + "; color:" + contrast_color.hex + "; }"
    css2 = ".base_color_variant_1 { background-color:" + base_color_variant_1.hex + "; width:100%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css3 = ".base_color_variant_2 { background-color:" + base_color_variant_2.hex + "; width:50%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css4 = ".base_color_variant_3 { background-color:" + base_color_variant_3.hex + "; width:100%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css5 = ".base_color_variant_4 { background-color:" + base_color_variant_4.hex + "; width:50%; height:40px; padding: 40px; font-size:20px; } \n\r"
    css6 = ".Contrastcolor { background-color:" + contrast_color.hex + "; width:10%; height:900px; position:absolute; right:300px; top:0px; color:" + base_color.hex + "; padding: 40px; font-size:20px; } \n"
    f = open('/home/coon/public_html/farbgeber.html', 'w')
    outputtxt = str(htmlpreface) + str(css1) + str(css2) + str(css3) + str(css4) + str(css5) + str(css6) + str(
        htmlcontent) + str(zeitzeile) + str(htmlclosing)
    f.write(outputtxt)
    f.close()

def generate_palette(time_value=0.0, base_saturation=1.0, base_luminance=0.4, hue_modifier=0.03, lum_modifier=0.07,
                     sat_modifier=0.2, program_cycles=0, output='html'):
    print "zentrale Farbgebeeinheit"

    broker_address = 'iot.eclipse.org'
    port = 1883
    client_id = 'farbgeber'
    topic = 'c-base/farbgeber'

    print "connecting to mqtt broker: %s:%d @ topic %s" % (broker_address,
            port, topic)

    mc = create_mqtt_publisher(broker_address, port, client_id, topic)

    while True:
        time_value = int(strftime("%M", gmtime())) * 60 + int(strftime("%S", gmtime()))
        time_value = float(time_value)

        base_hue = time_value / 3600
        base_color = Color(hsl=(base_hue, base_saturation, base_luminance))

        base_color_variant_1 = Color(
            hsl=(base_color.hue + hue_modifier, base_saturation - sat_modifier, base_luminance))
        base_color_variant_2 = Color(
            hsl=(base_color.hue - hue_modifier, base_saturation - sat_modifier, base_luminance))
        base_color_variant_3 = Color(
            hsl=(base_color.hue, base_saturation, base_luminance + lum_modifier))
        base_color_variant_4 = Color(
            hsl=(base_color.hue, base_saturation, base_luminance - lum_modifier))

        base_degree = base_hue * 360
        if base_degree < 180:
            contrast_hue = base_degree + 180
        else:
            contrast_hue = base_degree - 180
        contrast_hue /= 360

        contrast_color = Color(hsl=(contrast_hue, base_saturation - sat_modifier, (base_luminance + 0.2)))

        if output == 'term':
            # Terminaloutput
            generate_terminal_output(base_color, base_color_variant_1, base_color_variant_2, base_color_variant_3,
                                     base_color_variant_4, contrast_color, time_value)

        elif output == 'html':
            generate_html_output(base_color, base_color_variant_1, base_color_variant_2, base_color_variant_3,
                                 base_color_variant_4, contrast_color, time_value)

        # publish on MQTT broker:

        def packedColor(color):
          return struct.pack("BBB", color.get_red() * 255, color.get_green() * 255, color.get_blue() * 255)

        data  = "Binary:" + struct.pack("B", 0)
        data += packedColor(base_color)
        data += packedColor(base_color_variant_1)
        data += packedColor(base_color_variant_2)
        data += packedColor(base_color_variant_3)
        data += packedColor(base_color_variant_4)
        data += packedColor(contrast_color)

        payload = bytearray(data)
        mc.publish(topic, payload)

        program_cycles += + 1
        time.sleep(1)


if __name__ == "__main__":
    generate_palette()
