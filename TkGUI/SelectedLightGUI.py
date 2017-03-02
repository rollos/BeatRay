from Utils import *

DEFAULT_ID = 123




#The GUI that has the selected light, and allows you to change its size and color
#Possible change the shape in the future?
class SelectedLightGUI(tk.LabelFrame):
    def __init__(self, parent):
        #Initialize the LabelFrame
        super().__init__(parent, padx=5, pady=5, border=5, relief=tk.GROOVE, text="Selected Light")
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        # Make a canvas to display the light
        self.light_displayer = tk.Canvas(self, bg="black", height=100, width=100)
        self.light_displayer.grid(row=1, column=0)


        # make a label for the ID
        id_label = tk.Label(self, text="ID: " + str(DEFAULT_ID), width=7)
        id_label.grid(row=0, column=0)


        # Make a LabelFrame to hold the size slider
        size_frame = tk.LabelFrame(self, border=2, relief=tk.GROOVE, text="Size")
        self.size_slider = tk.Scale(size_frame, from_=1, to_= 100, orient=tk.HORIZONTAL) #Create the slider for size, orient it horizontally
        self.size_slider.pack()
        size_frame.grid(row=2, column=0)


        # Make the color selector
        self.color_selector = ColorSelector(self)
        self.color_selector.grid(row=0,column=1,rowspan=3)

        #Make the Button Frame for duplicate and delete and others possibly in the future?
        button_frame = tk.Frame(self)
        #Make the buttons
        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_clicked)
        self.duplicate_button = tk.Button(button_frame, text="Duplicate", command=self.duplicate_clicked)
        self.delete_button.pack(side=tk.LEFT)
        self.duplicate_button.pack(side=tk.LEFT)
        button_frame.grid(row=3,column=0, columnspan=2)


        #Configure all of the rows to be resizable
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)



    def delete_clicked(self):
        print("Delete Clicked")

    def duplicate_clicked(self):
        print("Duplicate Clicked")

    def message_view(self,message):
        self.parent.message_view(message)