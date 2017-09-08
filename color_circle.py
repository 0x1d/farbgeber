#!/usr/bin/python3

import threading
import math

import pygame

from colour import Color


class FarbgeberNew:
    def __init__(self, *colors):
        hex_list = [c.hex_l for c in colors]
        steps = int(3600 / len(hex_list))
        self.colors = list()

        for i, c in enumerate(hex_list):
            self.colors.extend(self.linear_gradient(hex_list[i], hex_list[i + 1 if i < len(hex_list) - 1 else 0], steps))


    def linear_gradient(self, start_hex, finish_hex="#FFFFFF", n=10):
        """ 
        returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF") 
        """

        def hex_to_rgb(hex_value):
            """ 
            #FFFFFF" -> [255,255,255] 
            """
            # Pass 16 to the integer function for change of base
            return [int(hex_value[i:i + 2], 16) for i in range(1, 6, 2)]


        def rgb_to_hex(rgb):
            """ 
            [255,255,255] -> "#FFFFFF" 
            """
            # Components need to be integers for hex to make sense
            rgb = [int(x) for x in rgb]
            return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                "{0:x}".format(v) for v in rgb])


        def color_dict(gradient):
            """ 
            Takes in a list of RGB sub-lists and returns dictionary of
            colors in RGB and hex form for use in a graphing function
            defined later on 
            """

            return {"hex":[rgb_to_hex(rgb) for rgb in gradient],
                    "r":[rgb[0] for rgb in gradient],
                    "g":[rgb[1] for rgb in gradient],
                    "b":[rgb[2] for rgb in gradient]}

        s = hex_to_rgb(start_hex)
        f = hex_to_rgb(finish_hex)

        rgb_list = [s]

        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
            rgb_list.append(curr_vector)

        return [Color(x) for x in color_dict(rgb_list)['hex']]


    def gen_palette(self, time_value):
        base_color = self.colors[int(time_value)]

        # TODO: add variant colors here

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


def draw_circle(screen, time_value, canvas=0, width=0, height=0):
    color = fb.gen_palette(time_value)["base_color"]

    i = 2 * math.pi * time_value / 3600.0

    r1 = 200
    r2 = 150
    x1 = 400 + r1 * math.cos(i)
    x2 = 400 + r2 * math.cos(i)
    y1 = 300 + r1 * math.sin(i)
    y2 = 300 + r2 * math.sin(i)

    pygame.draw.line(screen, (255 * color.red, 255 * color.green, 255 *
        color.blue), (x1, y1), (x2, y2), 1)
    pygame.display.update()

def setPixel(screen, x, y, color):
    pygame.draw.line(screen, \
      (255 * color.red, 255 * color.green, 255 * color.blue), (x, y), (x, y), 1)
    pygame.display.update()

def circleSym8(screen, xCenter, yCenter, radius, color):
    r2 = radius * radius
    setPixel(screen, xCenter, yCenter + radius, color)
    setPixel(screen, xCenter, yCenter - radius, color)
    setPixel(screen, xCenter + radius, yCenter, color)
    setPixel(screen, xCenter - radius, yCenter, color)

    y = radius
    x = 1
    y = int(math.sqrt(r2 - 1) + 0.5)

    dbgColor = Color("lime")

    while (x < y):
        setPixel(screen, xCenter + x, yCenter + y, color)
        setPixel(screen, xCenter + x, yCenter - y, color)
        setPixel(screen, xCenter - x, yCenter + y, color)
        setPixel(screen, xCenter - x, yCenter - y, color)
        setPixel(screen, xCenter + y, yCenter + x, color)
        setPixel(screen, xCenter + y, yCenter - x, color)
        setPixel(screen, xCenter - y, yCenter + x, color)
        setPixel(screen, xCenter - y, yCenter - x, color)
        x += 1
        y = int(math.sqrt(r2 - x*x) + 0.5)

    if (x == y):
        setPixel(screen, xCenter + x, yCenter + y, color)
        setPixel(screen, xCenter + x, yCenter - y, color)
        setPixel(screen, xCenter - x, yCenter + y, color)
        setPixel(screen, xCenter - x, yCenter - y, color)

if __name__ == "__main__":
    canvas_width = 800
    canvas_height = 600
    screen = pygame.display.set_mode((canvas_width, canvas_height))

    fb = FarbgeberNew(Color("red"), Color("yellow"), Color("lime"), Color("cyan"), Color("blue"), Color("magenta"))
    time_value = 0.0

    while(time_value < 3600):
      # draw_circle(screen, time_value, canvas_width, canvas_height)
      time_value += 1

    circleSym8(screen, 400, 300, 200, Color("red"))
    circleSym8(screen, 400, 300, 150, Color("red"))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

