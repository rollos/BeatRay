import os
import tkinter as tk
from tkinter import Tk, Frame, BOTH, Button, ttk, RIGHT, RAISED, LEFT
from TkGUI import PlayControls as PC, DisplayWindow as DW, Timeline as TL
from TkGUI import SelectedLightGUI as SL, MovementClipEditor as SC, ColorClipEditor as CC
from Utils import *

tk.Frame = tk.LabelFrame

DEFAULT_BPM = 120
DEFAULT_SCENE_LENGTH = "16 bars"

class MainApplication(tk.Frame):
    def __init__(self,parent, showgrid=False):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.view = None

        self.initialize()

    def message_view(self, message, value=None):
        assert self.view is not None
        self.view.notify_observers(message, value)


    def set_view(self, view):
        self.view = view

    def initialize(self):

        self.grid()

        self.make_menu()

        self.play_controls = PC.PlayControls(self)
        self.play_controls.grid(column=1, row=0, columnspan = 2, sticky='EW')

        self.pygame_window = DW.DisplayWindow(self)
        self.pygame_window.grid(column=1,row=1, sticky='NSEW')

        self.timeline = TL.TimelineContainer(self)
        self.timeline.grid(column=1,row=2, sticky='NSEW')

        info_editor_frame = tk.Frame(self)

        self.selected_light = SL.SelectedLightGUI(info_editor_frame, callback=self.message_view)


        self.movement_clip = SC.MovementClipEditor(info_editor_frame, callback=self.message_view)


        self.color_clip = CC.ColorClipsEditor(info_editor_frame, callback=self.message_view)

        info_editor_frame.grid_columnconfigure(0, weight=0)

        self.selected_clip = None

        info_editor_frame.grid(column=2, row=1, rowspan=2, sticky='NS')
        info_editor_frame.grid_columnconfigure(0, minsize=270)


        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=0)

        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=2)
        self.grid_rowconfigure(2,weight=1)

        self.grid_columnconfigure(3, weight=0)

        self.grid_size()

    def make_menu(self):
        #Initialize base menu
        menubar = tk.Menu(self.parent)

        #Initialize File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Scene", command=lambda: self.message_view("NEW_SCENE"))
        filemenu.add_command(label="Load Scene", command=lambda: self.message_view("LOAD_SCENE"))
        filemenu.add_command(label="Save", command=lambda: self.message_view("SAVE_SCENE"))

        #Initialize Scene Menu
        scenemenu = tk.Menu(menubar, tearoff=0)

        #Initialize Scene New Menu
        scenenewmenu = tk.Menu(scenemenu, tearoff=0)
        scenenewmenu.add_command(label="Light", command=lambda: self.message_view("NEW_LIGHT"))

        scenemenu.add_cascade(label="New", menu=scenenewmenu)

        #Initialize Scene Selected Light Menu
        selectedlightmenu = tk.Menu(scenemenu, tearoff=0)

        #Initialize Selected Light New Menu
        selectedlightnewmenu= tk.Menu(selectedlightmenu, tearoff=0)
        selectedlightnewmenu.add_command(label="Movement Clip", command=lambda: self.message_view("NEW_MOVEMENT_CLIP"))
        selectedlightnewmenu.add_command(label="Color Clip", command=lambda: self.message_view("NEW_COLOR_CLIP"))


        def new_color_clip():
            self.message_view("NEW_MOVEMENT_CLIP")

        def new_movement_clip():
            self.message_view("NEW_COLOR_CLIP")

        selectedlightmenu.add_cascade(label="New", menu=selectedlightnewmenu)

        scenemenu.add_cascade(label="Selected Light", menu = selectedlightmenu)



        #Add the menus to the menubar
        menubar.add_cascade(label="File", menu=filemenu)

        menubar.add_cascade(label="Scene", menu=scenemenu)


        #Add the menubar to the app
        self.parent.config(menu=menubar)


def hello():
    print("HELLO WORLD")

if __name__ == "__main__":
    root = tk.Tk()
    app =  MainApplication(parent=root)
    root.mainloop()