import tkinter as tk
from Defaults import *
# A small frame that contains entry boxes for the
# Length, Start, and End, points of a clip








#Event types for things that aren't a part of TK
MODELUPDATE = 0
VIEWUPDATE = 1

PAUSE_STATE = 0
PLAY_STATE = 1



def ticks_to_beat(ticks):
    return ticks/24

def beats_to_tick(beats):
    return beats * 24

def beats_to_bar(beats):
    return beats/4

def bars_to_beats(bars):
    return bars*4

def ticks_to_bars(ticks):
    return beats_to_bar(ticks_to_beat(ticks))

def bars_to_ticks(bars):
    return beats_to_tick(bars_to_beats(bars))

def convert_to_color(r,g,b):
    de = ("%02x" % r)
    re = ("%02x" % g)
    we = ("%02x" % b)
    ge = "#"

    return ge + de + re + we


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def convert_relative_to_absolute(position, canvas):
    x,y = position

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    x_ratio = width / SCREEN_WIDTH
    y_ratio = height / SCREEN_HEIGHT
    abs_x = x * x_ratio
    abs_y = y * y_ratio

    return (abs_x, abs_y)
