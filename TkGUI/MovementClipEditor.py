from Utils import *


class MovementClipEditor(tk.LabelFrame):
    def __init__(self,parent):
        super().__init__(parent,text="Movement Clip Editor")
        self.parent = parent

        self.active_args_widget = None
        self.initialize()

    def initialize(self):
        self.grid()

        self.location_boxes = ClipSizeEntrys(self)
        self.location_boxes.grid(row=0, column=1)

        self.line_frame = self.make_line_frame()
        self.circle_frame = self.make_circle_frame()
        self.spiral_frame = self.make_spiral_frame()
        self.none_frame = self.make_none_frame()

        choices= ['None', 'Line', 'Circle', 'Spiral']

        type_frame = tk.LabelFrame(self, text='Type')
        self.tkvar = tk.StringVar(self)
        self.tkvar.set('None')

        self.type_selection = tk.OptionMenu(type_frame, self.tkvar, *choices)
        self.type_selection.pack()

        type_frame.grid(row=0,column=0)
        self.tkvar.trace('w', self.set_active_args_window)

        self.set_active_args_window()



    def set_active_args_window(self, *args):
        if self.active_args_widget is not None:
            self.active_args_widget.grid_forget()

        type = str(self.tkvar.get())

        if type == "None":
            self.active_args_widget = self.none_frame
        elif type == "Line":
            self.active_args_widget = self.line_frame
        elif type == "Circle":
            self.active_args_widget = self.circle_frame
        elif type == "Spiral":
            self.active_args_widget = self.spiral_frame

        self.active_args_widget.grid(column=0, row=1, columnspan=2, sticky="NS")



    def make_none_frame(self):
        none_frame = tk.LabelFrame(self, text="Static Location")
        self.static_location_entry = CoordinatesBox(none_frame, "")
        self.static_location_entry.grid(column=0, row=0)

        return none_frame

    def make_line_frame(self):
        line_frame = tk.LabelFrame(self, text="Edit Line Movement")

        self.start_location_entry = CoordinatesBox(line_frame,"Start")
        self.start_location_entry.grid(column=0,row=0)

        self.end_location_entry = CoordinatesBox(line_frame, "End")
        self.end_location_entry.grid(column=1, row=0)

        return line_frame

    def make_circle_frame(self):
        circle_frame = tk.LabelFrame(self, text="Edit Circle Movement")

        c_center_location_box = CoordinatesBox(circle_frame, "Center Point")

        self.c_radius_box = EntryBoxWithFrame(circle_frame, "radius", width=3)

        self.c_start_degrees_box = EntryBoxWithFrame(circle_frame, "Start Degrees", width=3)
        self.c_end_degrees_box = EntryBoxWithFrame(circle_frame, "End Degrees", width=3)

        c_center_location_box.grid(column=0, row=0, rowspan=2)

        self.c_start_degrees_box.grid(column=1, row=0)
        self.c_end_degrees_box.grid(column=1,row=1)

        self.c_radius_box.grid(column=0, row=2)

        return circle_frame

    def make_spiral_frame(self):
        spiral_frame = tk.LabelFrame(self, text="Edit Spiral Movement")

        self.s_center_location_box = CoordinatesBox(spiral_frame, "Center Point")

        self.s_start_degrees_box = EntryBoxWithFrame(spiral_frame, "Start Degrees", width=3)
        self.s_end_degrees_box = EntryBoxWithFrame(spiral_frame, "End Degrees", width=3)
        self.s_start_radius = EntryBoxWithFrame(spiral_frame, "Start Radius", width=3)
        self.s_end_radius = EntryBoxWithFrame(spiral_frame, "End Radius", width=3)

        self.s_center_location_box.grid(column=0, row=0, rowspan=2)
        self.s_start_degrees_box.grid(column=1, row=0)
        self.s_end_degrees_box.grid(column=1, row=1)
        self.s_start_radius.grid(column=0,row=2)
        self.s_end_radius.grid(column=1,row=2)

        return spiral_frame








