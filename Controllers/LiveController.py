from Models.LiveModel import *
from Views.LiveView import *
from Utils.Defaults import *
class LiveController():
    def __init__(self,root):

        self.view = LiveView(root)

        self.model = LiveModel(self.view.gui.displaywindow.canvas)

        self.view.register_observer(self)
        self.model.register_observer(self)

        self.model.set_midi_input(self.view.get_midi_input())


    def update(self, type, message, value=None):
        if type == MODELUPDATE:
            self.update_view(message, value)
        elif type == VIEWUPDATE:
            self.update_model(message, value)

    def update_model(self, message, value=None):
        print("Message from View:{}, value={}".format(message, value))
        if message == "OPEN_DIRECTORY":
            self.model.set_active_directory(self.view.open_directory())
        elif message == "LOAD_BUTTON_PRESSED":
            self.model.set_state(LIVE_LOAD)

        elif message == "BUTTON_PRESSED":
            x,y = value
            if self.model.selector_squares[x][y].state == LIVE_LOAD:
                self.model.load_into_square(value, self.view.get_selected_file())
            pass

    def update_view(self, message, value=None):
        print("Message from Model:{}, value={}".format(message, value))
        if message == "DIRECTORY_UPDATED":
            print(self.model.active_directory)
            self.view.display_directory(self.model.loaded_files)
        elif message == "STATE_UPDATED":
            if self.model.state == LIVE_LOAD:
                self.view.set_load_state()
            if self.model.state == LIVE_PLAY:
                self.view.set_play_state()

        elif message == "SQUARE_LOADED":
            x,y = value
            self.view.display_square((x,y), self.model.selector_squares[x][y])
