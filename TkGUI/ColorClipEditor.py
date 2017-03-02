from Utils import *




class ColorClipsEditor(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Color Clip Editor")
        self.parent = parent
        self.active_args_widget = None

        self.initialize()

    def initialize(self):
        self.grid()

        self.location_boxes = ClipSizeEntrys(self)
        self.location_boxes.grid(row=0, column=1)

        self.none_frame = self.make_none_frame()
        self.blink_frame = self.make_blink_frame()
        self.fade_frame = self.make_fade_frame()


        choices = ["None", "Blink", "Fade"]

        type_frame = tk.LabelFrame(self, text='Type')
        self.tkvar = tk.StringVar(self)
        self.tkvar.set('None')

        self.type_selection = tk.OptionMenu(type_frame, self.tkvar, *choices)
        self.type_selection.pack()

        type_frame.grid(row=0, column=0)
        self.tkvar.trace('w', self.set_active_args_window)

        self.set_active_args_window()



    def set_active_args_window(self, *args):
        if self.active_args_widget is not None:
            self.active_args_widget.grid_forget()

        type = str(self.tkvar.get())

        if type == "None":
            self.active_args_widget = self.none_frame
        elif type == "Blink":
            self.active_args_widget = self.blink_frame
        elif type == "Fade":
            self.active_args_widget = self.fade_frame

        self.active_args_widget.grid(column=0, row=1, columnspan=2, sticky="NS")


    def make_none_frame(self):
        hold_frame = tk.Frame(self)
        none_frame = tk.LabelFrame(hold_frame, text="Static Color")
        self.static_color_selector = ColorSelector(none_frame)

        self.static_color_selector.grid(column=0, row=0)
        none_frame.pack()

        return hold_frame

    def make_blink_frame(self):
        blink_frame = tk.LabelFrame(self, text="Blink Colors")

        color_1_frame = tk.LabelFrame(blink_frame,text="Color 1")
        color_2_frame = tk.LabelFrame(blink_frame, text="Color 2")

        self.color_1_time = EntryBoxWithFrame(color_1_frame, "Beats", 3)
        self.color_2_time = EntryBoxWithFrame(color_2_frame, "Beats", 3)

        self.color_1_selector = ColorSelector(color_1_frame)
        self.color_2_selector = ColorSelector(color_2_frame)

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

        self.from_color_selector = ColorSelector(from_color_frame)
        self.to_color_selector = ColorSelector(to_color_frame)

        self.from_color_selector.grid(column=0, row=0)
        self.to_color_selector.grid(column=0, row=0)

        from_color_frame.grid(column=0, row=0)
        to_color_frame.grid(column=1, row=0)

        return fade_frame