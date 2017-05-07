#!/usr/bin/python
# coding=utf-8

import farbgeber
from colour import Color
from Tkinter import *
import threading

def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
           "{0:x}".format(v) for v in RGB])


def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
        "r":[RGB[0] for RGB in gradient],
        "g":[RGB[1] for RGB in gradient],
        "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  
  
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
        int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
        for j in range(3)
        ]

        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return [Color(x) for x in color_dict(RGB_list)['hex']]


#cl = [Color("red"), Color("yellow"), Color("lime"), Color("cyan"), Color("blue"), Color("magenta")]
cl = [Color("red"), Color("lime"), Color("cyan"), Color("blue"), Color("magenta")] # skip yellow
hl = [c.hex_l for c in cl]

steps = 3600 / len(hl)
colors = list()

for i in range(len(hl)):
    colors.extend(linear_gradient(hl[i], hl[i + 1 if i < len(hl) - 1 else 0], steps))

def generate_cust_palette(time_value):    
    base_color = colors[int(time_value)]

    p = dict()
    p['time_value']           = base_color
    p['base_color']           = base_color
    p['base_color_variant_1'] = base_color
    p['base_color_variant_2'] = base_color
    p['base_color_variant_3'] = base_color
    p['base_color_variant_4'] = base_color
    p['base_color_variant_5'] = base_color
    p['contrast_color']       = base_color

    return p

def draw_line(no, index, base_color, canvas=0, width=0, height=0):
    w = (no + 1) * width / ((no + 1) * 12.0)
    x = (no + 1) * width / 4 - w / 4
    y = int(index)

    canvas.create_line(x, y, x + w, y, fill=base_color.hex)
    canvas.update()

if __name__ == "__main__":
    master = Tk()

    canvas_width = 800
    canvas_height = 600
    canvas = Canvas(master, width=canvas_width, height=canvas_height)
    canvas.pack()

    time_value = 0.0
    color_offset = 0.0
    while(time_value + color_offset < 3600):
        index = time_value / 6
        palette  = farbgeber.generate_palette(time_value = time_value + color_offset)
        palette2 = generate_cust_palette(time_value)

        draw_line(0, index, palette['base_color'], canvas, canvas_width, canvas_height)
        draw_line(2, index, palette2['base_color'], canvas, canvas_width, canvas_height)
        time_value += 6

    mainloop()

