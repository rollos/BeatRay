import tkinter as tk
from Utils.Defaults import *
import TkGUI.SaveFile
import TkGUI.DisplayWindow
import mido
import os


class LiveMainApp(tk.Frame):
    def __init__(self, parent, view):
        tk.Frame.__init__(self, parent)

        self.blank_menu = tk.Menu()
        self.canvas = tk.Canvas(parent)
     #   self.canvas.pack()


        self.parent = parent

        self.parent.tk_focusFollowsMouse()

        self.view = view

        self.ss_panel = SceneSelectorPanel(self)

        self.bpm_area = BPMArea(self)

        self.file_loader = FileLoader(self)


        self.bpm_area.grid(row=0, column=0, sticky="NSW")

        self.ss_panel.grid(row=1, column=0)

        self.file_loader.grid(row=2, column=0)

        self.save_window = TkGUI.SaveFile.TkFileDialog(self)


        t = tk.Toplevel()
        t.wm_title("Display Window")
        # t.wm_overrideredirect(True)
        # t.wm_overrideredirect(False)


        self.displaywindow = TkGUI.DisplayWindow.DisplayWindow(t)
        self.displaywindow.pack(fill=tk.BOTH, expand=tk.YES, padx=0, pady=0)

        # t.attributes("-fullscreen",'true')
        t.config(menu=self.blank_menu)
        #self.displaywindow.canvas.bind("<Configure>", lambda *args:self.message_view("DISPLAY_WINDOW_RESIZED"))

        self.pack()

    def get_directory(self):
        return self.save_window.askdirectoryasfilepath()

    def message_view(self, message, value=None):
        self.view.notify_observers(message, value)


class SceneSelectorPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.mouseover=None



        self.squares = self.make_buttons()

    def message_view(self, message, value=None):
        self.parent.message_view(message, value)

    def make_buttons(self):
        w, h = DEF_SELECTION_PANEL_DIMENSIONS
        buttons = [[SceneSquare for x in range(w)] for y in range(h)]

        for x in range(w):
            for y in range(h):
                b = SceneSquare(self, position=(x,y))
                buttons[x][y] = b
                b.grid(column=x, row=y)

        return buttons

    def display_square(self, position, squaremodel):
        x,y = position

        self.squares[x][y].display_square(squaremodel)




    def show_load_state(self):
        for x in range(len(self.squares)):
            for y in range(len(self.squares[x])):
                self.squares[x][y].show_load_state()

    def show_play_state(self):
        for x in range(len(self.squares)):
            for y in range(len(self.squares[x])):
                self.squares[x][y].show_play_state()




class SceneSquare(tk.LabelFrame):
    def __init__(self,parent, position):
        super().__init__(parent, text="SceneName")
        self.parent = parent
        self.position = position

        # self.button = tk.Button(self, width=3, text="Load",
        #                         command = lambda *args: self.message_view("BUTTON_PRESSED"))

        self.button = PlayButton(self)

      #  self.button.bind("<ButtonPress-1>", lambda *args: self.message_view("BUTTON_DOWN"))
      #  self.button.bind("<ButtonRelease-1>", lambda *args: self.message_view("BUTTON_RELEASED"))



        self.sync_check = tk.Checkbutton(self, command=lambda *args: self.message_view("SYNC_CHECKED"))

        choices = ['Play Once', 'Hold', 'Loop']

        self.type_frame = tk.LabelFrame(self, text='Type')
        self.type_var = tk.StringVar(self)
        self.type_var.set('Play Once')

        self.type_var.trace('w', lambda *args: self.message_view("TYPE_UPDATED"))

        self.type_selection = tk.OptionMenu(self.type_frame, self.type_var, *choices)
        self.type_selection.pack()

        self.bind("<Enter>", self.mark_mouseover)

        self.button.grid(column=0, row=0)
        self.sync_check.grid(column=1, row=0)
        self.type_frame.grid(column=0, row=1, columnspan=2)

    def mark_mouseover(self, *args):
     #   print(self.position)
        self.parent.mouseover = self.position

    def message_view(self, message):
        self.parent.message_view(message, value=self.position)


    def set_state(self, state):
        self.button.set_state(state)

    def display_square(self, squaremodel):
        self.config(text=squaremodel.live_scene_model.filename)
        self.set_state(squaremodel.state)

class FileLoader(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        self.open_directory_button = tk.Button(self, text="Open Directory",
                                               command=lambda *args: self.message_view("OPEN_DIRECTORY"))

        self.open_directory_button.pack()

        self.file_frame = tk.Frame(self)

        scrollbar = tk.Scrollbar(self.file_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.list = tk.Listbox(self.file_frame, yscrollcommand=scrollbar.set)

        scrollbar.config(command = self.list.yview)


        self.list.pack()

        self.list_packed = False

        self.list.bind("<Button-1>", self.on_click)

        self.cur_index = 0

    def message_view(self, message, value=None):
        self.parent.message_view(message, value)


    def display_files(self, filelist):
        for file in filelist:
            self.list.insert(tk.END, file)

        if not self.list_packed:
            self.file_frame.pack()
            self.list_packed=True

    def on_click(self, event):
        self.cur_index = self.list.nearest(event.y)


    def get_selected_file(self):
        return self.list.get(self.cur_index)

class BPMArea(tk.LabelFrame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)

        self.resync_button = tk.Button(self, text="Resync", command = lambda *args: self.parent.message_view("RESYNC"))

        choices = mido.get_input_names()
        choices.append('None')

        clock_selector_frame = tk.LabelFrame(self, text='Clock Input')



        self.clock_var = tk.StringVar(self)
        self.clock_var.set('None')

        self.clock_var.trace('w', lambda *args: self.parent.message_view("CLOCK_INPUT_UPDATED"))

        self.type_selection = tk.OptionMenu(clock_selector_frame, self.clock_var, *choices)
        self.type_selection.pack()

        self.clock_display = tk.Canvas(self, width=10, height=10, bg="black")

        clock_selector_frame.pack(side=tk.LEFT)

        self.clock_display.pack(side=tk.LEFT)
        self.resync_button.pack(side=tk.LEFT)


    def flash_light(self):
        self.clock_display.config(bg="red")
        self.clock_display.after(100, lambda: self.clock_display.config(bg='black'))


class PlayButton(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, height=30, width=30, background="black")


        self.parent = parent

        self.play_img = tk.PhotoImage(file ="Images/PlayButton.gif")
        self.stop_img = tk.PhotoImage(file ="Images/StopButton.gif")
        self.load_img = tk.PhotoImage(file = "Images/LoadButton.gif")
        self.canvas.create_image(3, 3, image=self.load_img, anchor="nw")

        self.canvas.bind("<ButtonPress-1>", lambda *args: self.message_view("BUTTON_PRESSED"))
        self.canvas.bind("<ButtonRelease-1>", lambda *args: self.message_view("BUTTON_RELEASED"))

        self.canvas.pack()

    def message_view(self, message):
        self.parent.message_view(message)

    def set_state(self, state):
        self.canvas.delete("all")
        if state == LIVE_LOAD:
            self.canvas.create_image(3, 3, image=self.load_img, anchor="nw")
        elif state == LIVE_PLAY:
            self.canvas.create_image(3, 3, image=self.stop_img, anchor="nw")
        elif state == LIVE_PAUSE:
            self.canvas.create_image(3, 3, image=self.play_img, anchor="nw")


