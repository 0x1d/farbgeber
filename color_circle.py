#!/usr/bin/python
# coding=utf-8

import time
import struct
from colour import Color
from Tkinter import *
import threading

def generate_terminal_output(base_color, base_color_variant_1, base_color_variant_2, base_color_variant_3, base_color_variant_4, contrast_color, time_value, canvas=0, width=0, height=0):
    w = width / 6.0
    y = int(time_value / 6)

    canvas.create_line(0 * width, y, w, y, fill=base_color.hex)
    canvas.update()

def generate_palette(time_value=0.0, base_saturation=1.0, base_luminance=0.4, hue_modifier=0.03, lum_modifier=0.07, sat_modifier=0.2, program_cycles=0, canvas=0, width=0, height=0):

    while(time_value < 3600):
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

        generate_terminal_output(base_color, base_color_variant_1, base_color_variant_2, base_color_variant_3,
                                     base_color_variant_4, contrast_color, time_value, canvas, width, height)

        time_value += 6

if __name__ == "__main__":
  master = Tk()

  canvas_width = 800
  canvas_height = 600
  w = Canvas(master, width=canvas_width, height=canvas_height)
  w.pack()

  generate_palette(canvas=w, width=canvas_width, height=canvas_height)
  mainloop()

