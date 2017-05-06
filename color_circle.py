#!/usr/bin/python
# coding=utf-8

import farbgeber
from colour import Color
from Tkinter import *
import threading

def draw_line(index, base_color, canvas=0, width=0, height=0):
    w = width / 12.0
    x = width / 2 - w / 2
    y = int(index)

    canvas.create_line(x + 0 * width, y, x + w, y, fill=base_color.hex)
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
        palette = farbgeber.generate_palette(time_value = time_value + color_offset)
        draw_line(index, palette['base_color'], canvas, canvas_width, canvas_height)
        time_value += 6

#        if time_value == 600:
#            color_offset += 600

    mainloop()

