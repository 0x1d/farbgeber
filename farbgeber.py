import os
import paho.mqtt.client as mqtt
import struct 
import json
from time import gmtime, strftime, sleep
from colour import Color

MQTT_PUBLISHER = bool(int(os.environ['MQTT_PUBLISHER']))
MQTT_BROKER_HOST = os.environ['MQTT_BROKER_HOST']
MQTT_BROKER_PORT = os.environ['MQTT_BROKER_PORT']
MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_CLIENT_ID = os.environ['MQTT_CLIENT_ID']
UPDATE_INTERVAL = os.environ['UPDATE_INTERVAL']
SCHEME_FORMAT = os.environ['SCHEME_FORMAT']
GENERATE_HTML = bool(int(os.environ['GENERATE_HTML']))
HTML_OUTPUT_PATH = os.environ['HTML_OUTPUT_PATH']

def gen_time_value():
    time_value = int(strftime("%M", gmtime())) * 60 + int(strftime("%S", gmtime()))
    time_value = float(time_value)
    return time_value

def generate_terminal_output(p):
    print(p['t'])
    print("base_color ", p['b'])
    print("baseColorVariant1 ", p['v1'])
    print("baseColorVariant2 ", p['v2'])
    print("baseColorVariant3 ", p['v3'])
    print("baseColorVariant4 ", p['v4'])
    print("contrast_color ", p['c'])
    print("###################################")

def generate_html_output(palette):
    time_value = palette['time_value']
    base_color = palette['base_color']
    base_color_variant_1 = palette['base_color_variant_1']
    base_color_variant_2 = palette['base_color_variant_2']
    base_color_variant_3 = palette['base_color_variant_3']
    base_color_variant_4 = palette['base_color_variant_4']
    contrast_color = palette['contrast_color']

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
    f = open(HTML_OUTPUT_PATH, 'w')
    outputtxt = str(htmlpreface) + str(css1) + str(css2) + str(css3) + str(css4) + str(css5) + str(css6) + str(
        htmlcontent) + str(zeitzeile) + str(htmlclosing)
    f.write(outputtxt)
    f.close()

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

def packRGB(palette):
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

def packHex(palette):
    p = dict()
    p['t'] = palette['time_value']
    p['b'] = palette['base_color'].hex
    p['v1'] = palette['base_color_variant_1'].hex
    p['v2'] = palette['base_color_variant_2'].hex
    p['v3'] = palette['base_color_variant_3'].hex
    p['v4'] = palette['base_color_variant_4'].hex
    p['c'] = palette['contrast_color'].hex
    return p

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.payload)

def mqtt_publisher():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT), 60)
    client.loop_start()
    return client

def generate_scheme():
    palette = generate_palette(time_value = gen_time_value())
    outPalette = None

    if GENERATE_HTML:
        generate_html_output(palette)
    
    if SCHEME_FORMAT == "HEX":
        outPalette = packHex(palette)
    else:
        outPalette = packRGB(palette)

    return outPalette

def mqtt_main():
    client = mqtt_publisher()
    while True:
        scheme = generate_scheme()
        client.publish(MQTT_TOPIC, json.dumps(scheme))
        sleep(int(UPDATE_INTERVAL))

def main ():

    while True:
        scheme = generate_scheme()
        generate_terminal_output(scheme)
        sleep(int(UPDATE_INTERVAL))

if __name__ == "__main__":
    print("Zentrale Farbgebeeinheit")
    if MQTT_PUBLISHER:
        print("MQTT Broker: " + MQTT_BROKER_HOST)
        print("MQTT ClientID: " + MQTT_CLIENT_ID)
        print("MQTT Topic: " + MQTT_TOPIC)
        mqtt_main()
    else:
        main()
