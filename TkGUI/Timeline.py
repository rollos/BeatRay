import tkinter as tk
from Utils import *

class TimelineContainer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initialize()
        self.scene_length = DEF_SCENE_LENGTH



    def initialize(self):
        self.move_timeline = MovementTimeline(self)
        self.color_timeline = ColorTimeline(self)

        self.move_timeline.pack( fill=tk.BOTH, expand=tk.YES)
        self.color_timeline.pack( fill=tk.BOTH, expand=tk.YES)
        
    def create_clip(self):
        #length of clip in beats
        length=4
        
    def set_length(self, beats):



class MovementTimeline(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent, height=200, padx=5, relief=tk.GROOVE, borderwidth=5)
        self.initialize()

    def initialize(self):
        self.label = tk.Label(self,text="MovementTimeline")
        self.label.pack(side=tk.LEFT)
        pass

    def set_length(self):
        pass

class ColorTimeline(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent, padx=5, relief=tk.GROOVE, borderwidth=5)
        self.initialize()

    def initialize(self):
        self.label = tk.Label(self,text="ColorTimeline")
        self.label.pack(side=tk.LEFT)
        pass
    
class Clip(tk.Frame):
    def __init__(self,parent, start=0):
        super().__init__(parent,bg="red")
        self.parent = parent
        self.start = start
        
        self.initialize()

    def initialize(self):
        pass
        
        
