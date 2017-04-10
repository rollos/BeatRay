import time

from Models.LightModel import LightModel
from Utils.Utils import *


class SceneModel():

    def __init__(self):

        self.canvas = None

        self.bpm = DEF_BPM
        self.scene_length = DEF_SCENE_LENGTH
        self.selected_light_id = None

        self.play_state = PAUSE_STATE

        self.light_id_counter = 0

        self.lights = {}

        self.observers = []

        self.scrub_time = 0

        self.lights_state = None








    def bpm_delay(self):
        seconds_per_beat = (float(60) / self.bpm / 24)

        time.sleep(seconds_per_beat)

    def update_scrubber(self, value):
        self.scrub_time = value
        self.update_display_lights()

        self.notify_observers("SCRUB_TIME_UPDATED")


    def advance_scrubber(self):
        self.scrub_time += 1

        self.update_scrubber(self.scrub_time)

        if self.scrub_time >= self.scene_length * 4 * 24:
            self.stop_pressed()


    def render_schedules(self):
        for light in self.lights.values():
            light.render_schedules()

    #Enable accesing lights by their key
    #Example:
    # Light a = self[10]

    def __getstate__(self):
        d = {}
        d["bpm"] = self.bpm
        d["scene_length"] = self.scene_length
        d["light_id_counter"] = 0
        d["play_state"] = PAUSE_STATE

        lights = {}

        for id in self.lights:
            lights[id] = self.lights[id].__getstate__()

        d["lights"] = lights
        print("test")
        print(d)

        return d

    def __setstate__(self,state):
        self.lights_state = state["lights"]
        self.bpm = state["bpm"]
        self.scene_length = state["scene_length"]
        self.light_id_counter = 0
        self.play_state = PAUSE_STATE
        self.selected_light_id = 0

        self.canvas = None

        self.selected_light_id = 0

        self.lights = {}

        self.observers = []

        self.scrub_time = 0








    def __getitem__(self, key):
        try:
            return self.lights[key]
        except KeyError:
            return None

    #Enable setting lights by their key
    def __setitem__(self, key, value):
        self.lights[key] = value

    def __delitem__(self, key):
        del self.lights[key]

    #Register an observer to this model
    def register_observer(self, observer):
        self.observers.append(observer)


    #Notify the observers with a message
    def notify_observers(self, message):
        for observer in self.observers:
            #try:
                observer.update(MODELUPDATE, message)
           # except AttributeError:
           #     raise AttributeError("Observer does not have update() function")

    def set_BPM(self, BPM):
        self.bpm = BPM
        self.notify_observers("BPM_UPDATE")


    def set_scene_length(self, length):
        self.scene_length = length
        self.notify_observers("SCENE_LENGTH_UPDATE")

    def switch_play_state(self):

        self.render_schedules()

        if self.play_state == PAUSE_STATE:
            self.play_state = PLAY_STATE

        elif self.play_state == PLAY_STATE:
            self.play_state = PAUSE_STATE

        self.notify_observers("PLAY_STATE_UPDATE")

    def stop_pressed(self):
        if self.play_state == PLAY_STATE:
            self.play_state = PAUSE_STATE

            self.update_scrubber(0)
            self.notify_observers("PLAY_STATE_UPDATE")

    def select_light(self, light_id):
        if light_id in self.lights.keys():
            self.selected_light_id = light_id

            self.notify_observers("LIGHT_SELECTED")
        else:
            print("Light does not exist")


    def new_light(self, state=None, duplicate=False):
        light = LightModel(self, id=self.light_id_counter, state=state, duplicate=duplicate)
        self.lights[self.light_id_counter] = light

        self.selected_light_id = self.light_id_counter

        #This is what sends the message
        self.select_light(self.light_id_counter)

        self.light_id_counter += 1




    def new_movement_clip(self):
        self.lights[self.selected_light_id].new_movement_clip()


    def new_color_clip(self):
        self.lights[self.selected_light_id].new_color_clip()

    def size_updated(self, size):
        if self.selected_light_id is not None:
            self.lights[self.selected_light_id].update_size(size)
        else:
            self.notify_observers("NO_LIGHT_SELECTED")

    def light_type_updated(self, type):
        self.lights[self.selected_light_id].update_shape(type)

    def get_selected_light(self):
        if self.selected_light_id in self.lights.keys():
            return self.lights[self.selected_light_id]

    def get_selected_clip(self):
        return self.get_selected_light().get_selected_clip()

    def update_display_lights(self):
        for light in self.lights.values():
            light.update_display_light(self.scrub_time)

    def make_lights_from_state(self):
        for light_state in self.lights_state.values():
            self.new_light(light_state)







