#!/usr/bin/python
# coding=utf-8

import farbgeber
from colour import Color
from Tkinter import *
import threading

def draw_color_circle(time_value, base_color, canvas=0, width=0, height=0):
    w = width / 12.0
    x = width / 2 - w / 2
    y = int(time_value / 6)

    canvas.create_line(x + 0 * width, y, x + w, y, fill=base_color.hex)
    canvas.update()

if __name__ == "__main__":
    master = Tk()

    canvas_width = 800
    canvas_height = 600
    canvas = Canvas(master, width=canvas_width, height=canvas_height)
    canvas.pack()

    time_value = 0.0
    while(time_value < 3600):
        palette = farbgeber.generate_palette(time_value = time_value)
        draw_color_circle(time_value, palette['base_color'], canvas, canvas_width, canvas_height)
        time_value += 6

    mainloop()

