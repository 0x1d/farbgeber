import os
import struct 
import output
import publisher
from time import gmtime, strftime, sleep
from colour import Color

MQTT_PUBLISHER = bool(int(os.environ['MQTT_PUBLISHER']))
UPDATE_INTERVAL = os.environ['UPDATE_INTERVAL']
SCHEME_FORMAT = os.environ['SCHEME_FORMAT']
GENERATE_HTML = bool(int(os.environ['GENERATE_HTML']))
HTML_OUTPUT_PATH = os.environ['HTML_OUTPUT_PATH']

def generate_time_value():
    time_value = int(strftime("%M", gmtime())) * 60 + int(strftime("%S", gmtime()))
    time_value = float(time_value)
    return time_value

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

def pack_rgb(palette):
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

def pack_hex(palette):
    p = dict()
    p['t'] = palette['time_value']
    p['b'] = palette['base_color'].hex
    p['v1'] = palette['base_color_variant_1'].hex
    p['v2'] = palette['base_color_variant_2'].hex
    p['v3'] = palette['base_color_variant_3'].hex
    p['v4'] = palette['base_color_variant_4'].hex
    p['c'] = palette['contrast_color'].hex
    return p

def generate_scheme():
    palette = generate_palette(time_value = generate_time_value())
    if GENERATE_HTML:
        output.html(palette, HTML_OUTPUT_PATH)
    if SCHEME_FORMAT == "HEX":
        return pack_hex(palette)
    else:
        return pack_rgb(palette)

if __name__ == "__main__":
    print("Zentrale Farbgebeeinheit")
    if MQTT_PUBLISHER:
        publisher.mqtt_handler(generate_scheme)
    else:
        # not publishing, just print to terminal
        while True:
            output.terminal(generate_scheme())
            sleep(int(UPDATE_INTERVAL))