from Utils import *

from SceneModel import LightModel
from tkUtils import *
from Defaults import *

DEFAULT_ID = 123




#The GUI that has the selected light, and allows you to change its size and color
#Possible change the shape in the future?
class SelectedLightGUI(tk.LabelFrame):
    def __init__(self, parent, callback):
        #Initialize the LabelFrame
        super().__init__(parent, padx=5, pady=5, border=5, relief=tk.GROOVE, text="Selected Light")
        self.parent = parent
        self.callback = callback
        self.initialize()


    def initialize(self):

        # Make a canvas to display the light
        self.light_displayer = tk.Canvas(self, bg="black", height=100, width=100)
        self.light_displayer.grid(row=1, column=0)


        # make a label for the ID
        self.id_label = tk.Label(self, text="ID: " + str(DEFAULT_ID), width=7)
        self.id_label.grid(row=0, column=0)

        self.light_selector_box = EntryBoxWithFrame(self, "LightSelector", 3, callback=lambda *args: self.message_view("LIGHT_SELECTED"))
        self.light_selector_box.grid(row=0,column=1)

        # Make a LabelFrame to hold the size slider
        size_frame = tk.LabelFrame(self, border=2, relief=tk.GROOVE, text="Size")
        self.size_slider = tk.Scale(size_frame, from_=1, to_= 100, orient=tk.HORIZONTAL, command= lambda x: self.message_view("SIZE_UPDATED")) #Create the slider for size, orient it horizontally
        self.size_slider.pack()
        size_frame.grid(row=2, column=0)

        choices = ["Circle", "Line", "Entire Screen"]

        light_type_frame = tk.LabelFrame(self, text='Light Type')
        self.light_type_var = tk.StringVar(self)
        self.light_type_var.set('Circle')

        self.light_type_var.trace_variable('w', callback=lambda *args: self.message_view("LIGHT_TYPE_UPDATED"))

        self.type_selection = tk.OptionMenu(light_type_frame, self.light_type_var, *choices)
        self.type_selection.pack()


        light_type_frame.grid(column=1, row =1)

        self.clip_selector_box = EntryBoxWithFrame(self, "Clip Selector", 3,
                                                   callback=lambda *args: self.message_view("CLIP_SELECTED"))
        self.clip_selector_box.grid(column=1, row=2)

        #Make the Button Frame for duplicate and delete and others possibly in the future?
        button_frame = tk.Frame(self)
        #Make the buttons
        self.delete_button = tk.Button(button_frame, text="Delete", command=lambda: self.message_view("SELECTED_LIGHT_DELETE"))
        self.duplicate_button = tk.Button(button_frame, text="Duplicate", command= lambda: self.message_view("SELECTED_LIGHT_DUPLICATED") )
        self.delete_button.pack(side=tk.LEFT)
        self.duplicate_button.pack(side=tk.LEFT)
        button_frame.grid(row=3,column=0, columnspan=2)


        #Configure all of the rows to be resizable
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def selector_box(self, *args):
        self.message_view("LIGHT_SELECTED")

    def get_light_size(self):
        return self.size_slider.get()

    def set_light_size(self, size):
        self.light_type_var.set(size)

    def set_id(self, text):
        self.id_label.config(text="ID: " + str(text))

    def display_light(self, light:LightModel):
       #self.light_displayer.set_light()
        if light is None:
            self.grid_forget()
        else:
            self.grid(row=0, column=0)

            self.set_id(light.id)
            self.size_slider.set(light.size)
            self.light_type_var.set(light.shape)





    def message_view(self,message):
        self.callback(message)