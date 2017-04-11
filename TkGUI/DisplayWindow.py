import tkinter as tk
from Defaults import RES_RATIO

from Utils.Defaults import RES_RATIO


class DisplayWindow(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent, borderwidth=0, width=200, height=200)
        self.parent = parent
        self.canvas = None
        self.initialize()


    def initialize(self):
        self.content_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.content_frame, background="black")
        self.canvas.pack( fill=tk.BOTH, expand=tk.YES)

        set_aspect(self.content_frame, self, aspect_ratio=RES_RATIO)

def set_aspect(content_frame, pad_frame, aspect_ratio):
    # a function which places a frame within a containing frame, and
    # then forces the inner frame to keep a specific aspect ratio

    def enforce_aspect_ratio(event):
        # when the pad window resizes, fit the content into it,
        # either by fixing the width or the height and then
        # adjusting the height or width based on the aspect ratio.

        # start by using the width as the controlling dimension
        desired_width = event.width
        desired_height = int(event.width / aspect_ratio)

        # if the window is too tall to fit, use the height as
        # the controlling dimension
        if desired_height > event.height:
            desired_height = event.height
            desired_width = int(event.height * aspect_ratio)

        # place the window, giving it an explicit size
        content_frame.place(in_=pad_frame, x=0, y=0,
            width=desired_width, height=desired_height)

    pad_frame.bind("<Configure>", enforce_aspect_ratio)




