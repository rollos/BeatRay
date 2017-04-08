import tkinter as tk
from tkUtils import *

from Utils import *

class PlayControls(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.initialize()

    def initialize(self):

        #Make the Play Button
        self.playButton = tk.Button(self, text=">", command = lambda: self.message_view("PLAY_PRESSED"))

        #Make the Stop Button
        stopButton = tk.Button(self, text="[]", command = lambda: self.message_view("STOP_PRESSED"))

        #Make the BPM text Box
        self.bpm_entry = EntryBoxWithFrame(self, "BPM", width=3,  callback=lambda x: self.message_view("BPM_UPDATE"))

        #Make the scene length text box
        self.scene_length_entry = EntryBoxWithFrame(self, "Scene Length", width=3, callback=lambda x: self.message_view("SCENE_LENGTH_UPDATE"))

        self.playButton.pack(side=tk.LEFT)
        stopButton.pack(side=tk.LEFT)
        self.bpm_entry.pack(side=tk.LEFT)
        self.scene_length_entry.pack(side=tk.LEFT)




    #Update the text of the play button based on the state
    def update_play_button(self, state):
        if state == PLAY_STATE:
            self.playButton.config(text="||")
        if state == PAUSE_STATE:
            self.playButton.config(text=">")

    def message_view(self, message):
        self.parent.message_view(message)





