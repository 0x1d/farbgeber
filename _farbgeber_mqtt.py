#import farbgeber

import paho.mqtt.client as mqtt
import struct 
import json
from time import gmtime, strftime, sleep
from colour import Color

def gen_time_value():
    time_value = int(strftime("%M", gmtime())) * 60 + int(strftime("%S", gmtime()))
    time_value = float(time_value)
    return time_value

def generate_terminal_output(palette):

    p = dict()
    p['t'] = palette['time_value']
    p['bc'] = palette['base_color'].hex
    p['bcv1'] = palette['base_color_variant_1'].hex
    p['bcv2'] = palette['base_color_variant_2'].hex
    p['bcv3'] = palette['base_color_variant_3'].hex
    p['bcv4'] = palette['base_color_variant_4'].hex
    p['cc'] = palette['contrast_color'].hex
    
    print(p['t'])
    print("base_color ", p['bc'])
    print("baseColorVariant1 ", p['bcv1'])
    print("baseColorVariant2 ", p['bcv2'])
    print("baseColorVariant3 ", p['bcv3'])
    print("baseColorVariant4 ", p['bcv4'])
    print("contrast_color ", p['cc'])
    print("###################################")

    return p

def generate_palette(time_value=0.0, base_saturation=1.0, base_luminance=0.4, hue_modifier=0.03, lum_modifier=0.07, sat_modifier=0.2): 
    base_hue = time_value / 3600
    base_color = Color(hsl=(base_hue, base_saturation, base_luminance))        
    base_color_variant_1 = Color(hsl=(base_color.hue + hue_modifier, base_saturation - sat_modifier, base_luminance))
    base_color_variant_2 = Color(hsl=(base_color.hue - hue_modifier, base_saturation - sat_modifier, base_luminance))
    base_color_variant_3 = Color(hsl=(base_color.hue, base_saturation, base_luminance + lum_modifier))
    base_color_variant_4 = Color(hsl=(base_color.hue, base_saturation, base_luminance - lum_modifier))

    base_degree = base_hue * 360
    if base_degree < 180:
        contrast_hue = base_degree + 180
    else:
        contrast_hue = base_degree - 180
        
    contrast_hue /= 360
    contrast_color = Color(hsl=(contrast_hue, base_saturation - sat_modifier, (base_luminance + 0.2)))

    p = dict()
    p['time_value'] = time_value
    p['base_color'] = base_color
    p['base_color_variant_1'] = base_color_variant_1
    p['base_color_variant_2'] = base_color_variant_2
    p['base_color_variant_3'] = base_color_variant_3
    p['base_color_variant_4'] = base_color_variant_4
    p['contrast_color'] = contrast_color

    return p

def pack(palette):
    def packedColor(color):
        FLOAT_ERROR = 0.0000005

        def colorToInt(c):
            return int(c*255 + 0.5 - FLOAT_ERROR)

        return [colorToInt(color.get_red()), colorToInt(color.get_green()), colorToInt(color.get_blue())]

    data = dict()
    data['b']  = packedColor(palette['base_color'])
    data['v1'] = packedColor(palette['base_color_variant_1'])
    data['v2'] = packedColor(palette['base_color_variant_2'])
    data['v3'] = packedColor(palette['base_color_variant_3'])
    data['v4'] = packedColor(palette['base_color_variant_4'])
    data['c']  = packedColor(palette['contrast_color'])

    return data

def hex(palette):
    return palette

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("c-base/farbgeber")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Topic: " + msg.topic)
    palette = generate_palette(time_value = gen_time_value())
    generate_terminal_output(palette)

def main ():
    client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.1.2", 2883, 60)
    client.loop_start()
    while True:
        sleep(10)
        palette = generate_palette(time_value = gen_time_value())
        p = generate_terminal_output(palette)
        client.publish("c-base/farbgeber", json.dumps(p));

if __name__ == "__main__":
    print("Zentrale Farbgebeeinheit")
    main()
