import tkinter as tk
# A small frame that contains entry boxes for the
# Length, Start, and End, points of a clip

#Default Values
DEF_BPM = 120
DEF_SCENE_LENGTH = 16   #Bars

DEF_SHAPE = "CIRCLE"

DEF_CLIP_LENGTH = 16    #Bars
DEF_CLIP_START = 0


DEF_MOVEMENT_CLIP_TYPE = "None"

DEF_STATIC_LOCATION = (.5, .5)
DEF_START_LOCATION = (0, 0)

DEF_END_LOCATION = (1, 1)

DEF_C_CENTER_LOCATION = (.5, .5)
DEF_C_START_DEGREES = 0
DEF_C_END_DEGREES = 360
DEF_C_RADIUS = .25

DEF_S_CENTER_LOCATION = (.5, .5)
DEF_S_START_DEGREES = 0
DEF_S_END_DEGREES = 360
DEF_S_START_RADIUS = 0
DEF_S_END_RADIUS = .5


DEF_COLOR_CLIP_TYPE = 'None'

DEF_STATIC_COLOR = (256,256,256)

DEF_COLOR_1_TIME = 1    #BEATS
DEF_COLOR_2_TIME = 1    #BEATS
DEF_COLOR_1 = (256,256,256)
DEF_COLOR_2 = (0,0,0)

DEF_FROM_COLOR = (0,0,0)
DEF_TO_COLOR = (256,256,256)



#Event types for things that aren't a part of TK
MODELUPDATE = 0
VIEWUPDATE = 1

PAUSE_STATE = 0
PLAY_STATE = 1




class ClipSizeEntrys(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

        self.initialize()

    def initialize(self):
        self.grid()

        self.length_entry = tk.Entry(self, width=3)
        self.start_entry = tk.Entry(self, width=3)
        self.end_entry = tk.Entry(self, width=3)

        length_label = tk.Label(self, text="Length")
        start_label = tk.Label(self, text="Start")
        end_label = tk.Label(self, text="End")

        self.length_entry.grid(row=1,column=0)
        self.start_entry.grid(row=1,column=1)
        self.end_entry.grid(row=1, column=2)

        length_label.grid(row=0, column=0)
        start_label.grid(row=0, column=1)
        end_label.grid(row=0, column=2)

class CoordinatesBox(tk.LabelFrame):
    def __init__(self,parent,title):
        super().__init__(parent, text=title)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        x_frame = tk.LabelFrame(self, text='x')
        self.x_coord = tk.Entry(x_frame, width=3)
        self.x_coord.pack()

        y_frame = tk.LabelFrame(self, text='y')
        self.y_coord = tk.Entry(y_frame, width=3)
        self.y_coord.pack()

        select_button = tk.Button(self, text='select', command=self.select_pressed)
        copy_button = tk.Button(self, text='c', command=self.copy_pressed)
        paste_button = tk.Button(self, text='p',command=self.paste_pressed)

        x_frame.grid(column=0,row=0,padx=(5,0))
        y_frame.grid(column=1,row=0,padx=(0,5))

        select_button.grid(column=0,row=1, columnspan=2)

        copy_button.grid(column=0,row=2)
        paste_button.grid(column=1, row=2)


    def copy_pressed(self):
        print("Copy Pressed")
    def select_pressed(self):
        print('Select Pressed')

    def paste_pressed(self):
        print('Paste Pressed')

def testmethod(*args):
    print("TESTMETHOD CALLED")

class EntryBoxWithFrame(tk.LabelFrame):
    def __init__(self,parent, label, width, callback=testmethod):
        super().__init__(parent,text=label)
        self.parent = parent

        self.svar = tk.IntVar(self)
        self.svar.trace('w', callback)



        self.entry_box = tk.Entry(self, width=width)#, textvariable=self.svar)
        self.entry_box.bind('<Return>', callback)
        self.entry_box.pack()



    def get_entry(self):
            return self.entry_box.get()

    def set_entry(self, value:int):
        self.entry_box.delete(0)
        self.entry_box.insert(0, value)

class ColorSelector(tk.Frame):


    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.initialize()

    def initialize(self):

        #Make the frames
        r_frame = tk.LabelFrame(self, text="Red", padx=3,pady=3)
        g_frame = tk.LabelFrame(self, text="Green", padx=3,pady=3)
        b_frame = tk.LabelFrame(self, text="Blue", padx=3,pady=3)


        #Make the sliders for each color
        self.r_slider = tk.Scale(r_frame, from_=0, to_=256, orient=tk.HORIZONTAL)
        self.g_slider = tk.Scale(g_frame, from_=0, to_=256, orient=tk.HORIZONTAL)
        self.b_slider = tk.Scale(b_frame, from_=0, to_=256, orient=tk.HORIZONTAL)


        #Pack the sliders and labels into their frames
        self.r_slider.pack()

        self.g_slider.pack()

        self.b_slider.pack()

        r_frame.pack()
        g_frame.pack()
        b_frame.pack()

    def get_rgb_tup(self):
        return (self.r_slider.get(),self.g_slider.get(),self.b_slider.get())



