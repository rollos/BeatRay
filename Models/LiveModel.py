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


        self.display_model = DisplayModel(self)





    def set_midi_input(self, input):
        self.midi_clock = input

       # self.run_clock()




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


    #This method is continuously run during the mainloop:
    #Handle all values here
    def single_loop(self):

        message = self.midi_clock.receive()
        if message.type == 'clock':
            self.display_model.clock_tick()

    def play_pressed(self, value):
        x,y = value
        if self.selector_squares[x][y].state == LIVE_PAUSE:
            self.display_model.pause_state_press(self.selector_squares[x][y])

        elif self.selector_squares[x][y].state == LIVE_PLAY:
            self.display_model.play_state_press(self.selector_squares[x][y])

        self.notify_observers("PLAY_PRESSED", value)

    def button_released(self, value):
        x, y = value
        if self.selector_squares[x][y].type == "Hold":

            self.display_model.delete_active_light()
            self.selector_squares[x][y].state = LIVE_PAUSE
            self.notify_observers("SQUARE_STATE_UPDATED", value)



class DisplayModel():
    def __init__(self,parent):
        self.parent = parent
        self.sync_counter = 0
        self.active_square = None
        self.sync_wait_scene = None
        self.active_scene_scrubber = 0

    def pause_state_press(self, selector_square):
        if selector_square.sync_state == False:
            self.set_active_scene(selector_square)
            selector_square.play_pressed()
        elif selector_square.sync_state == True:
            self.sync_wait_scene = selector_square


    def play_state_press(self, selector_square):
        self.delete_active_light()
        self.set_active_scene(None)
        selector_square.play_pressed()

    def clock_beat(self):
        if self.sync_wait_scene is not None:
            self.set_active_scene(self.sync_wait_scene)
            self.sync_wait_scene = None


        self.message_model("CLOCK_BEAT")

    def clock_tick(self):
        if self.sync_counter == 0:
            self.clock_beat()

        if self.active_square is not None and self.active_square.live_scene_model is not None:
            self.move_active_light(self.active_scene_scrubber)
            self.active_scene_scrubber += 1

        self.message_model("CLOCK_TICK")
        self.sync_counter = (self.sync_counter + 1) % 24

    def resync(self):
        self.sync_counter = 0

    def set_active_scene(self, scene):
        self.active_square = scene
        self.active_scene_scrubber = 0

        self.delete_active_light()

        if scene is None:
            return

        for light in self.active_square.live_scene_model.rendered_lights:
            light.draw_light()
            light.move_light_to_scrubber(0)

    def move_active_light(self, scrubber):
        for light in self.active_square.live_scene_model.rendered_lights:
            light.move_light_to_scrubber(scrubber)

    def delete_active_light(self):
        if self.active_square is None:
            return

        for light in self.active_square.live_scene_model.rendered_lights:
            light.delete_light()

        self.active_scene_scrubber = 0






    def message_model(self, message, value=None):
        self.parent.notify_observers(message, value)


class SelectorSquareModel():
    def __init__(self, position, canvas, parent):
        self.state = LIVE_LOAD
        self.position = position
        self.live_scene_model = None
        self.sync_state = False
        self.canvas = canvas
        self.parent = parent
        self.type = "Play Once"

    def load_file(self, path, filename):
        if filename is None:
            return
        self.live_scene_model = LiveSceneModel(path, filename, self.canvas)
        self.state = LIVE_PAUSE
        self.message_model("SQUARE_LOADED")

    def message_model(self, message):
        self.parent.notify_observers(message, value=self.position)

    def play_pressed(self):
        if self.state == LIVE_PLAY:
            self.state = LIVE_PAUSE

        elif self.state == LIVE_PAUSE:
            self.state = LIVE_PLAY

        else:
            raise Exception("Wrong square state ")

        self.message_model("SQUARE_STATE_UPDATED")

    def toggle_sync(self):
        if self.sync_state == False:
            self.sync_state = True
        elif self.sync_state == True:
            self.sync_state = False

        self.message_model("SYNC_STATE_UPDATED")

    def set_type(self, type):
        self.type = type



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

        self.rendered_lights = None

        self.render_schedules()







    def render_schedules(self):
        for light in self.scene_model.lights.values():
            light.render_schedules()
        self.rendered_lights = [light.rendered_light for light in self.scene_model.lights.values()]
