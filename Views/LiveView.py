import mido

from TkGUI.LiveGUI.LiveMainGUI import LiveMainApp
from Utils.Defaults import VIEWUPDATE

class LiveView():
    def __init__(self, root ):
        self.observers = []
        self.gui = LiveMainApp(root, self)



    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message, value=None):
        for observer in self.observers:
            observer.update(VIEWUPDATE, message, value)

    def get_midi_input(self):
        try:
            return mido.open_input(self.gui.bpm_area.clock_var.get())
        except OSError:
            print("No Longer Open")

    def open_directory(self):
        return self.gui.get_directory()

    def set_gui(self, gui):
        self.gui = gui

    def display_directory(self, directory):

        self.gui.file_loader.display_files(directory)

    def get_mouseover(self):
        return self.gui.ss_panel.mouseover

    def set_load_state(self):
        self.gui.ss_panel.show_load_state()

    def get_selected_file(self):
        return self.gui.file_loader.get_selected_file()

    def set_play_state(self):
        self.gui.ss_panel.show_play_state()

    def display_square(self, position, square):
        x,y = position
        self.gui.ss_panel.display_square(position, square)

    def flash_bpm_light(self):
        self.gui.bpm_area.flash_light()