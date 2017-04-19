from Models.LiveModel import *
from Views.LiveView import *
from Utils.Defaults import *
class LiveController():
    def __init__(self,root):

        self.root = root

        self.view = LiveView(root)

        self.model = LiveModel(self.view.gui.displaywindow.canvas)

        self.view.register_observer(self)
        self.model.register_observer(self)

        self.model.set_midi_input(self.view.get_midi_input())


        #root.mainloop()
        self.run_clock()


    def update(self, type, message, value=None):
        if type == MODELUPDATE:
            self.update_view(message, value)
        elif type == VIEWUPDATE:
            self.update_model(message, value)

    def run_clock(self):
        while(True):
            self.root.update_idletasks()
            self.root.update()

            if self.model.midi_clock is not None:
                self.model.single_loop()



    def update_model(self, message, value=None):
        print("Message from View:{}, value={}".format(message, value))
        if message == "OPEN_DIRECTORY":
            self.model.set_active_directory(self.view.open_directory())
        elif message == "LOAD_BUTTON_PRESSED":
            self.model.set_state(LIVE_LOAD)

        elif message == "BUTTON_PRESSED":
            x,y = value
            square = self.model.selector_squares[x][y]
            if self.model.selector_squares[x][y].state == LIVE_LOAD:
                self.model.load_into_square(value, self.view.get_selected_file())

            else:
                self.model.play_pressed(value)
            pass

        elif message == "BUTTON_RELEASED":
            self.model.button_released(value)

        elif message == "CLOCK_INPUT_UPDATED":
            self.model.set_midi_input(self.view.get_midi_input())

        elif message == "TYPE_UPDATED":
            x,y = value
            self.model.selector_squares[x][y].set_type(self.view.get_type(value))

        elif message == "RESYNC":
            self.model.display_model.resync()

        elif message == "SYNC_CHECKED":
            x,y = value
            self.model.selector_squares[x][y].toggle_sync()

    def update_view(self, message, value=None):
        if message != "CLOCK_TICK":
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

        elif message == "SQUARE_STATE_UPDATED":
            x,y = value

            self.view.update_square_state((x,y), self.model.selector_squares[x][y].state)

        elif message == "CLOCK_BEAT":
            self.view.flash_bpm_light()
