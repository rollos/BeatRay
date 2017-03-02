from TkGUI import *
from TkGUI.MainApp import *
from Utils import *


class SceneView():
    def __init__(self, gui: MainApplication):
        self.observers = []
        self.gui = gui

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            try:
                observer.update(VIEWUPDATE, message)
            except AttributeError:
                raise AttributeError("Observer does not have update() function")

    def set_bpm(self, bpm):
        self.gui.play_controls.bpm_entry.set_entry(bpm)

    def get_bpm(self):
        return self.gui.play_controls.bpm_entry.get_entry()

    def update_play_button_state(self,state):
        self.gui.play_controls.update_play_button(state)

    def get_scene_length(self):
        return self.gui.play_controls.scene_length_entry.get_entry()

