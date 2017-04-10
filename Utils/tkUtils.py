import tkinter as tk

class ClipSizeEntrys(tk.Frame):
    def __init__(self,parent, length_callback, start_callback, end_callback):
        super().__init__(parent)
        self.parent = parent


        self.length_box = EntryBoxWithFrame(self, label="Length", width=3, callback=length_callback)
        self.start_box = EntryBoxWithFrame(self, label="Start", width=3, callback=start_callback)
        self.end_box = EntryBoxWithFrame(self, label="End", width=3, callback=end_callback)


        self.length_box.grid(row=0, column=0, rowspan=2)
        self.start_box.grid(row=0, column=1, rowspan=2)
        self.end_box.grid(row=0, column=2, rowspan=2)

    def get_length(self):
        return self.length_box.get_entry()
    def set_length(self, value):
        self.length_box.set_entry(value)

    def get_start(self):
        return self.start_box.get_entry()
    def set_start(self,value):
        self.start_box.set_entry(value)

    def get_end(self):
        return self.end_box.get_entry()
    def set_end(self,value):
        return self.end_box.set_entry(value)


class CoordinatesBox(tk.LabelFrame):
    def __init__(self,parent,title, callback):
        self.callback = callback
        super().__init__(parent, text=title)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.x_coord = EntryBoxWithFrame(self,label='x',width=3,callback=self.callback)
        self.x_coord.pack()

        self.y_coord = EntryBoxWithFrame(self, label='y', width=3, callback=self.callback)
        self.y_coord.pack()

        select_button = tk.Button(self, text='select', command=self.select_pressed)
        copy_button = tk.Button(self, text='c', command=self.copy_pressed)
        paste_button = tk.Button(self, text='p',command=self.paste_pressed)

        self.x_coord.grid(column=0,row=0,padx=(5,0))
        self.y_coord.grid(column=1,row=0,padx=(0,5))

        select_button.grid(column=0,row=1, columnspan=2)

        copy_button.grid(column=0,row=2)
        paste_button.grid(column=1, row=2)


    def get_location(self):
        return (self.x_coord.get_entry(), self.y_coord.get_entry())

    def set_location(self, location:tuple):
        x,y = location
        self.x_coord.set_entry(x)
        self.y_coord.set_entry(y)


    def copy_pressed(self):
        print("Copy Pressed")
    def select_pressed(self):
        print('Select Pressed')

    def paste_pressed(self):
        print('Paste Pressed')

def testmethod(*args):
    print("TESTMETHOD CALLED")

class EntryBoxWithFrame(tk.LabelFrame):
    def __init__(self,parent, label, width, callback):
        super().__init__(parent,text=label)
        self.parent = parent

        self.entry_box = tk.Entry(self, width=width)#, textvariable=self.svar)
        self.entry_box.bind('<Return>', callback)
        self.entry_box.pack()



    def get_entry(self):
            return float(self.entry_box.get())

    def set_entry(self, value:float):
        self.entry_box.delete(0,tk.END)
        self.entry_box.insert(0, "%.2f" % value)

class ColorSelector(tk.Frame):


    def __init__(self, parent, callback):
        super().__init__(parent)
        self.parent = parent

        self.callback = callback

        self.initialize()

    def initialize(self):

        #Make the frames
        r_frame = tk.LabelFrame(self, text="Red", padx=3,pady=3)
        g_frame = tk.LabelFrame(self, text="Green", padx=3,pady=3)
        b_frame = tk.LabelFrame(self, text="Blue", padx=3,pady=3)

        self.r_var = tk.IntVar(self)
        self.g_var = tk.IntVar(self)
        self.b_var = tk.IntVar(self)

        self.r_var.trace('w', self.callback)
        self.g_var.trace('w', self.callback)
        self.b_var.trace('w', self.callback)

        #Make the sliders for each color
        self.r_slider = tk.Scale(r_frame, from_=0, to_=255, orient=tk.HORIZONTAL, variable=self.r_var)
        self.g_slider = tk.Scale(g_frame, from_=0, to_=255, orient=tk.HORIZONTAL, variable = self.g_var)
        self.b_slider = tk.Scale(b_frame, from_=0, to_=255, orient=tk.HORIZONTAL, variable = self.b_var)


        #Pack the sliders and labels into their frames
        self.r_slider.pack()

        self.g_slider.pack()

        self.b_slider.pack()

        r_frame.pack()
        g_frame.pack()
        b_frame.pack()

    def get_color(self) -> tuple:
        return (self.r_var.get(),self.g_var.get(),self.b_var.get())

    def set_color(self, color:tuple):
        self.r_var.set(color[0])
        self.g_var.set(color[1])
        self.b_var.set(color[2])



def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)