from os import listdir

import mido
import pickle

from Utils.Defaults import *


class LiveModel():

    def __init__(self, canvas):
        self.active_directory = None
        self.observers = []

        self.loaded_files = []

        self.state = LIVE_EDIT

        w,h = DEF_SELECTION_PANEL_DIMENSIONS

        self.selector_squares = [[SelectorSquareModel((x,y), canvas, self) for y in range(w)] for x in range(h)]

        self.canvas = None

        self.midi_clock = None



    def set_midi_input(self, input):
        self.midi_input = input

        self.run_clock()

    def run_clock(self):
        if self.midi_input is None: return
        while(True):
            for message in self.midi_input:
                print(message)

                if message.type == 'clock':
                    self.run_frame()




    def run_frame(self):
        print("frame")

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message, value=None):
        for observer in self.observers:
            observer.update(MODELUPDATE, message, value)

    def display_directory(self, directory):
        for f in listdir(directory):
            print(f)

    def set_active_directory(self, directory):
        self.active_directory = directory

        for f in listdir(directory):
            self.loaded_files.append(f)

        self.notify_observers("DIRECTORY_UPDATED")

    def load_file(self, f):
        return f

    def load_into_square(self, position, file):
        if self.active_directory is None:
            return
        x,y = position
        self.selector_squares[x][y].load_file(self.active_directory, file)

        self.notify_observers("SQUARE_LOADED", value=position)

    def set_state(self, state):
        self.state = state

        self.notify_observers("STATE_UPDATED")

class SelectorSquareModel():
    def __init__(self, position, canvas, parent):
        self.state = LIVE_LOAD
        self.position = position
        self.live_scene_model = None
        self.canvas = canvas
        self.parent = parent

    def load_file(self, path, filename):
        if filename is None:
            return
        self.live_scene_model = LiveSceneModel(path, filename, self.canvas)
        self.state = LIVE_PLAY
        self.message_model("SQUARE_LOADED", value= self.position)

    def message_model(self, message, value=None):
        self.parent.notify_observers(message, value=value)


class LiveSceneModel():
    def __init__(self, path, filename, canvas):
        self.filepath = path + '/' + filename
        self.filename = None
        if filename.endswith(FILE_EXTENSION):
            self.filename = filename[:-len(FILE_EXTENSION)]
        else:
            self.filename = filename


        f = open(self.filepath, "rb")

        self.scene_model = pickle.load(f)

        self.scene_model.canvas = canvas

        self.scene_model.make_lights_from_state()

        for light in self.scene_model.lights.values():
            light.render_schedules()


        self.rendered_lights = [light.rendered_light for light in self.scene_model.lights.values()]





