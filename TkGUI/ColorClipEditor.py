from Utils import *
from ClipModels import ColorClipModel
from tkUtils import *



class ColorClipsEditor(tk.LabelFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, text="Color Clip Editor")
        self.parent = parent
        self.callback = callback
        self.active_args_widget = None

        self.initialize()

    def initialize(self):


        self.location_boxes = ClipSizeEntrys(self,
                                             length_callback=lambda x:self.message_view("CLIP_LENGTH_UPDATED"),
                                             start_callback=lambda x:self.message_view("CLIP_START_UPDATED"),
                                             end_callback=lambda x:self.message_view("CLIP_END_UPDATED")
                                             )

        self.location_boxes.grid(row=0, column=1)

        self.none_frame = self.make_none_frame()
        self.blink_frame = self.make_blink_frame()
        self.fade_frame = self.make_fade_frame()


        choices = ["None", "Blink", "Fade"]

        type_frame = tk.LabelFrame(self, text='Type')
        self.type_var = tk.StringVar(self)
        self.type_var.set('None')


        self.type_selection = tk.OptionMenu(type_frame, self.type_var, *choices)
        self.type_selection.pack()

        type_frame.grid(row=0, column=0)
        self.type_var.trace('w', self.color_type_change)

        self.set_active_args_window(message=True)


    def color_type_change(self, *args):
        self.message_view("CLIP_TYPE_UPDATED")
        self.set_active_args_window()


    def set_active_args_window(self, message=False, *args):

        if self.active_args_widget is not None:
            self.active_args_widget.grid_forget()

        type = str(self.type_var.get())

        if type == "None":
            self.active_args_widget = self.none_frame
        elif type == "Blink":
            self.active_args_widget = self.blink_frame
        elif type == "Fade":
            self.active_args_widget = self.fade_frame

        self.active_args_widget.grid(column=0, row=1, columnspan=2, sticky="NS")
        print("WIDTH:{}".format(self.winfo_width()))

        if not message:
            self.message_view("CLIP_TYPE_UPDATED")



    def make_none_frame(self):
        hold_frame = tk.Frame(self)
        none_frame = tk.LabelFrame(hold_frame, text="Static Color")
        self.static_color_selector = ColorSelector(none_frame, callback=lambda *args:self.message_view("STATIC_COLOR_UPDATED"))

        self.static_color_selector.grid(column=0, row=0)
        none_frame.pack()

        return hold_frame

    def make_blink_frame(self):
        blink_frame = tk.LabelFrame(self, text="Blink Colors")

        color_1_frame = tk.LabelFrame(blink_frame,text="Color 1")
        color_2_frame = tk.LabelFrame(blink_frame, text="Color 2")

        self.color_1_time = EntryBoxWithFrame(color_1_frame, "Beats", 3,
                                              callback=lambda x:self.message_view("COLOR_1_TIME_UPDATED"))
        self.color_2_time = EntryBoxWithFrame(color_2_frame, "Beats", 3,
                                              callback=lambda x:self.message_view("COLOR_2_TIME_UPDATED"))

        self.color_1_selector = ColorSelector(color_1_frame,
                                              callback=lambda *args:self.message_view("COLOR_1_UPDATED"))
        self.color_2_selector = ColorSelector(color_2_frame,
                                              callback=lambda *args:self.message_view("COLOR_2_UPDATED"))

        self.color_1_selector.grid(column=0, row=0)
        self.color_2_selector.grid(column=0, row=0)

        self.color_1_time.grid(column=0,row=1)
        self.color_2_time.grid(column=0,row=1)

        color_1_frame.grid(column=0, row=0)
        color_2_frame.grid(column=1, row=0)

        return blink_frame



    def make_fade_frame(self):
        fade_frame = tk.LabelFrame(self, text="Blink Colors")

        from_color_frame = tk.LabelFrame(fade_frame, text="From Color")
        to_color_frame = tk.LabelFrame(fade_frame, text="To Color")

        self.from_color_selector = ColorSelector(from_color_frame, callback=lambda *args:self.message_view("FROM_COLOR_UPDATED"))
        self.to_color_selector = ColorSelector(to_color_frame, callback=lambda *args:self.message_view("TO_COLOR_UPDATED"))

        self.from_color_selector.grid(column=0, row=0)
        self.to_color_selector.grid(column=0, row=0)

        from_color_frame.grid(column=0, row=0)
        to_color_frame.grid(column=1, row=0)

        return fade_frame

    def display_clip(self, clip:ColorClipModel):
        if clip is None:
            self.grid_forget()
        else:
            self.type_var.set(clip.type)

            self.location_boxes.set_end(clip.clip_end)
            self.location_boxes.set_length(clip.clip_length)
            self.location_boxes.set_start(clip.clip_start)

            self.static_color_selector.set_color(clip.static_color)

            self.color_1_time.set_entry(clip.color_1_time)
            self.color_2_time.set_entry(clip.color_2_time)
            self.color_1_selector.set_color(clip.color_1)
            self.color_2_selector.set_color(clip.color_2)

            self.from_color_selector.set_color(clip.from_color)
            self.to_color_selector.set_color(clip.to_color)

            self.grid(row=1, column=0, sticky="NSEW")





    def message_view(self, message):
        self.callback(message)