from Utils import *
from SceneModel import *
from ClipModels import *
from tkUtils import *

class MovementClipEditor(tk.LabelFrame):
    def __init__(self,parent, callback):
        super().__init__(parent,text="Movement Clip Editor")
        self.parent = parent
        self.callback = callback

        self.active_args_widget = None
        self.initialize()

    def initialize(self):

        self.location_boxes = ClipSizeEntrys(self,
                                             length_callback=lambda x: self.message_view("CLIP_LENGTH_UPDATED"),
                                             start_callback=lambda x: self.message_view("CLIP_START_UPDATED"),
                                             end_callback=lambda x: self.message_view("CLIP_END_UPDATED")
                                             )

        self.location_boxes.grid(row=0, column=1)

        self.line_frame = self.make_line_frame()
        self.circle_frame = self.make_circle_frame()
        self.spiral_frame = self.make_spiral_frame()
        self.none_frame = self.make_none_frame()

        choices= ['None', 'Line', 'Circle', 'Spiral']

        type_frame = tk.LabelFrame(self, text='Type')
        self.type_var = tk.StringVar(self)
        self.type_var.set('None')

        self.type_selection = tk.OptionMenu(type_frame, self.type_var, *choices)
        self.type_selection.pack()

        type_frame.grid(row=0,column=0)
        self.type_var.trace('w', self.clip_type_updated)

        self.set_active_args_window(message=True)



    def set_active_args_window(self, message=False, *args):

        if self.active_args_widget is not None:
            self.active_args_widget.grid_forget()

        type = str(self.type_var.get())

        if type == "None":
            self.active_args_widget = self.none_frame
        elif type == "Line":
            self.active_args_widget = self.line_frame
        elif type == "Circle":
            self.active_args_widget = self.circle_frame
        elif type == "Spiral":
            self.active_args_widget = self.spiral_frame

        self.active_args_widget.grid(column=0, row=1, columnspan=2, sticky="NS")
        if not message:
            self.message_view("CLIP_TYPE_UPDATED")



    def make_none_frame(self):
        none_frame = tk.LabelFrame(self, text="Static Location")
        self.static_location_entry = CoordinatesBox(none_frame, "",
                                                    callback=lambda *args:self.message_view("STATIC_LOCATION_UPDATED"))
        self.static_location_entry.grid(column=0, row=0)

        return none_frame

    def make_line_frame(self):
        line_frame = tk.LabelFrame(self, text="Edit Line Movement")

        self.start_location_entry = CoordinatesBox(line_frame,"Start",
                                                   callback=lambda *args:self.message_view("START_LOCATION_UPDATED"))
        self.start_location_entry.grid(column=0,row=0)

        self.end_location_entry = CoordinatesBox(line_frame, "End",
                                                 callback= lambda *args:self.message_view("END_LOCATION_UPDATED"))
        self.end_location_entry.grid(column=1, row=0)

        return line_frame

    def make_circle_frame(self):
        circle_frame = tk.LabelFrame(self, text="Edit Circle Movement")

        self.c_center_location_box = CoordinatesBox(circle_frame, "Center Point",
                                               callback=lambda *args:self.message_view("C_CENTER_LOCATION_UPDATED"))

        self.c_radius_box = EntryBoxWithFrame(circle_frame, "radius", width=3,
                                              callback=lambda *args:self.message_view("C_RADIUS_UPDATED"))

        self.c_start_degrees_box = EntryBoxWithFrame(circle_frame, "Start Degrees", width=3,
                                                     callback=lambda *args:self.message_view("C_START_DEGREES_UPDATED"))

        self.c_end_degrees_box = EntryBoxWithFrame(circle_frame, "End Degrees", width=3,
                                                   callback=lambda *args:self.message_view("C_END_DEGREES_UPDATED"))

        self.c_center_location_box.grid(column=0, row=0, rowspan=2)

        self.c_start_degrees_box.grid(column=1, row=0)
        self.c_end_degrees_box.grid(column=1,row=1)

        self.c_radius_box.grid(column=0, row=2)

        return circle_frame

    def make_spiral_frame(self):
        spiral_frame = tk.LabelFrame(self, text="Edit Spiral Movement")

        self.s_center_location_box = CoordinatesBox(spiral_frame, "Center Point",
                                                    callback=lambda *args: self.message_view("S_CENTER_LOCATION_UPDATED"))

        self.s_start_degrees_box = EntryBoxWithFrame(spiral_frame, "Start Degrees", width=3,
                                                     callback=lambda *args: self.message_view("S_START_DEGREES_UPDATED"))
        self.s_end_degrees_box = EntryBoxWithFrame(spiral_frame, "End Degrees", width=3,
                                                   callback=lambda *args: self.message_view("S_END_DEGREES_UPDATED"))
        self.s_start_radius_box = EntryBoxWithFrame(spiral_frame, "Start Radius", width=3,
                                                    callback=lambda *args: self.message_view("S_START_DEGREES_UPDATED"))
        self.s_end_radius_box = EntryBoxWithFrame(spiral_frame, "End Radius", width=3,
                                                  callback=lambda *args: self.message_view("S_END_RADIUS_UPDATED"))

        self.s_center_location_box.grid(column=0, row=0, rowspan=2)
        self.s_start_degrees_box.grid(column=1, row=0)
        self.s_end_degrees_box.grid(column=1, row=1)
        self.s_start_radius_box.grid(column=0, row=2)
        self.s_end_radius_box.grid(column=1, row=2)

        return spiral_frame


    def message_view(self, message):
        self.callback(message)


    def display_clip(self,clip:MovementClipModel):
        if clip is None:
            self.grid_forget()
        else:
            self.type_var.set(clip.type)

            self.location_boxes.set_end(clip.clip_end)
            self.location_boxes.set_length(clip.clip_length)
            self.location_boxes.set_start(clip.clip_start)

            self.static_location_entry.set_location(clip.static_location)

            self.start_location_entry.set_location(clip.start_location)
            self.end_location_entry.set_location(clip.end_location)

            self.c_center_location_box.set_location(clip.c_center_location)
            self.c_radius_box.set_entry(clip.c_radius)
            self.c_start_degrees_box.set_entry(clip.c_start_degrees)
            self.c_end_degrees_box.set_entry(clip.c_end_degrees)

            self.s_center_location_box.set_location(clip.s_center_location)
            self.s_start_radius_box.set_entry(clip.s_start_radius)
            self.s_end_radius_box.set_entry(clip.s_end_radius)
            self.s_start_degrees_box.set_entry(clip.s_start_degrees)
            self.s_end_degrees_box.set_entry(clip.s_end_degrees)

            self.grid(row=1, column=0, sticky="NSEW")

    def clip_type_updated(self, *args):
        self.message_view("CLIP_TYPE_UPDATED")
        self.set_active_args_window()

