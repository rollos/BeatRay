from Utils import *


class SceneModel():

    def __init__(self):
        self.BPM = DEF_BPM
        self.scene_length = DEF_SCENE_LENGTH
        self.selected_light_id = None

        self.play_state = PLAY_STATE

        self.light_id_counter = 0

        self.lights = {}

        self.observers = []

        self.scrub_time = 0

    #Enable accesing lights by their key
    #Example:
    # Light a = self[10]
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
            try:
                observer.update(MODELUPDATE, message)
            except AttributeError:
                raise AttributeError("Observer does not have update() function")

    def set_BPM(self, BPM):
        self.BPM = BPM
        self.notify_observers("BPM_UPDATE")
        print("BPM UPDATED:{}".format(self.BPM))

    def set_scene_length(self, length):
        self.scene_length = length
        self.notify_observers("SCENELENGTH_UPDATE")

    def switch_play_state(self):
        if self.play_state == PAUSE_STATE:
            self.play_state = PLAY_STATE



        elif self.play_state == PLAY_STATE:
            self.play_state = PAUSE_STATE

        self.notify_observers("PLAY_STATE_UPDATE")

    def stop_pressed(self):
        if self.play_state == PLAY_STATE:
            self.play_state = PAUSE_STATE

        self.scrub_time = 0
        self.notify_observers("PLAY_STATE_UPDATE")

    def select_light(self, light_id):
        self.selected_light_id = light_id

    def new_scene(self):
        pass

    def load_scene(self):
        pass

    def save_scene(self):
        pass

    def new_light(self):
        light = LightModel()
        self.lights[self.light_id_counter] = light
        self.light_id_counter += 1

    def new_movement_clip(self):
        pass

    def new_color_clip(self):
        pass


class LightModel():

    def __init__(self, parent_scene):
        assert type(parent_scene) is SceneModel
        self.parent_scene = self.parent_scene

        self.shape = DEF_SHAPE
        self.movement_clip_id_counter = 0
        self.color_clip_id_counter = 0

        self.movement_clips = {}
        self.color_clips = {}

    def add_movement_clip(self, movement_clip):
        assert type(movement_clip) is MovementClipModel

        self.movement_clips[self.movement_clip_id_counter] = movement_clip
        self.movement_clip_id_counter += 1

        self.send_update("MOVEMENT_CLIP_ADDED")

    def add_color_clip(self,color_clip):
        assert type(color_clip) is ColorClipModel

        self.color_clips[self.color_clip_id_counter] = color_clip
        self.color_clip_id_counter += 1

        self.send_update("COLOR_CLIP_ADDED")

    def send_update(self, message):
        self.parent_scene.notify_observers(message)

class ClipModel():
    def __init__(self, parent_light):

        assert type(parent_light) is LightModel

        self.parent_light = parent_light

        self.clip_length = DEF_CLIP_LENGTH
        self.clip_start = DEF_CLIP_START
        self.clip_end = self.clip_start + self.clip_length

    def send_update(self, message):
        self.parent_light.send_update(message)

class MovementClipModel(ClipModel):

    def __init__(self):
        super().__init__()
        self.type = DEF_MOVEMENT_CLIP_TYPE
        self.static_location = DEF_STATIC_LOCATION

        self.start_location = DEF_START_LOCATION
        self.end_location = DEF_END_LOCATION

        self.c_center_location = DEF_C_CENTER_LOCATION
        self.c_start_degrees = DEF_C_START_DEGREES
        self.c_end_degrees = DEF_C_END_DEGREES
        self.c_radius = DEF_C_RADIUS

        self.s_center_location = DEF_S_CENTER_LOCATION
        self.s_start_degrees = DEF_C_START_DEGREES
        self.s_end_degrees = DEF_S_END_DEGREES
        self.s_start_radius = DEF_S_START_RADIUS
        self.s_end_radius = DEF_S_END_RADIUS

class ColorClipModel(ClipModel):

    def __init__(self):
        super().__init__()
        self.type = DEF_COLOR_CLIP_TYPE
        self.static_color = DEF_STATIC_COLOR
        self.color_1_time = DEF_COLOR_1_TIME
        self.color_2_time = DEF_COLOR_2_TIME
        self.color_1 = DEF_COLOR_1
        self.color_2 = DEF_COLOR_2
        self.from_color = DEF_FROM_COLOR
        self.to_color = DEF_TO_COLOR







