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
            #try:
                observer.update(MODELUPDATE, message)
           # except AttributeError:
           #     raise AttributeError("Observer does not have update() function")

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
        if light_id in self.lights.keys():
            self.selected_light_id = light_id

            self.notify_observers("LIGHT_SELECTED")
        else:
            print("Light does not exist")

    def new_scene(self):
        raise NotImplementedError

    def load_scene(self):
        raise NotImplementedError

    def save_scene(self):
        raise NotImplementedError

    def new_light(self):
        light = LightModel(self, self.light_id_counter)
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


class LightModel():

    def __init__(self, parent_scene, id):

        self.id = id
        self.parent_scene = parent_scene

        self.size = 10
        self.shape = DEF_SHAPE
        self.clip_id_counter = 0

        self.selected_clip_id = None

        self.movement_clips = {}
        self.color_clips = {}

    def select_clip(self, clip_id):
        if self.get_clip(clip_id) is not None:
            self.selected_clip_id = clip_id
            self.parent_scene.notify_observers("CLIP_SELECTED")
        else:
            self.parent_scene.notify_observers("Clip does not exist")

    def new_movement_clip(self):
        movement_clip = MovementClipModel(self, self.clip_id_counter)

        self.movement_clips[self.clip_id_counter] = movement_clip
        self.select_clip(self.clip_id_counter)

        self.clip_id_counter += 1

    def new_color_clip(self):
        color_clip = ColorClipModel(self, self.clip_id_counter)

        self.color_clips[self.clip_id_counter] = color_clip
        self.select_clip(self.clip_id_counter)
        self.clip_id_counter += 1

    def update_size(self, size):
        self.size = size

        self.send_update("SIZE_UPDATED")

    def update_shape(self, shape):
        self.shape = shape
        self.send_update("LIGHT_TYPE_UPDATED")



    def send_update(self, message):
        self.parent_scene.notify_observers(message)

    def get_clip(self, clip_id):
        if clip_id in self.movement_clips.keys():
            return self.movement_clips[clip_id]
        elif clip_id in self.color_clips.keys():
            return self.color_clips[clip_id]
        else:
            return None

    def get_selected_clip(self):
        return self.get_clip(clip_id=self.selected_clip_id)

class ClipModel():
    def __init__(self, parent_light):

        self.type = None
        self.parent_light = parent_light

        self.clip_length = DEF_CLIP_LENGTH
        self.clip_start = DEF_CLIP_START
        self.clip_end = self.clip_start + self.clip_length

    def send_update(self, message):
        self.parent_light.send_update(message)

    def clip_length_updated(self,length):
        self.clip_length = length
        self.send_update("CLIP_LENGTH_UPDATED")

    def clip_start_updated(self, start):
        self.clip_start = start
        self.send_update("CLIP_START_UPDATED")

    def clip_end_updated(self,end):
        self.clip_end = end
        self.send_update("CLIP_END_UPDATED")

    def clip_type_updated(self,type):
        self.type = type
        self.send_update("CLIP_TYPE_UPDATED")


class MovementClipModel(ClipModel):

    def __init__(self, parent, id):
        super().__init__(parent)

        self.id = id

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

    def static_location_updated(self, location):
        self.static_location = location
        self.send_update("STATIC_LOCATION_UPDATED")

    def start_location_updated(self,location):
        self.start_location = location
        self.send_update("START_LOCATION_UPDATED")

    def end_location_updated(self,location):
        self.end_location = location
        self.send_update("END_LOCATION_UPDATED")

    def c_center_location_updated(self,location):
        self.c_center_location = location
        self.send_update("C_CENTER_LOCATION_UPDATED")

    def c_start_degrees_updated(self, degrees):
        self.c_start_degrees = degrees
        self.send_update("C_START_DEGREES_UPDATED")

    def c_end_degrees_updated(self,degrees):
        self.c_end_degrees(degrees)
        self.send_update("C_END_DEGREES_UPDATED")

    def c_radius_updated(self, radius):
        self.c_radius = radius
        self.send_update("C_RADIUS_UPDATED")

    def s_center_location_updated(self, location):
        self.s_center_location = location
        self.send_update("S_CENTER_LOCATION_UPDATED")

    def s_start_degrees_updated(self,degrees):
        self.s_start_degrees = degrees
        self.send_update("S_START_DEGREES_UPDATED")

    def s_end_degrees_updated(self, degrees):
        self.s_end_degrees = degrees
        self.send_update("S_END_DEGREES_UPDATED")

    def s_start_radius_updated(self, radius):
        self.s_start_radius = radius
        self.send_update("S_START_RADIUS_UPDATED")

    def s_end_radius_updated(self, radius):
        self.s_end_radius = radius
        self.send_update("S_END_RADIUS_UPDATED")



class ColorClipModel(ClipModel):

    def __init__(self,parent:LightModel, id):
        super().__init__(parent)
        self.id = id

        self.type = DEF_COLOR_CLIP_TYPE
        self.static_color = DEF_STATIC_COLOR
        self.color_1_time = DEF_COLOR_1_TIME
        self.color_2_time = DEF_COLOR_2_TIME
        self.color_1 = DEF_COLOR_1
        self.color_2 = DEF_COLOR_2
        self.from_color = DEF_FROM_COLOR
        self.to_color = DEF_TO_COLOR


    def type_updated(self, type):
        self.type = type
        self.send_update("TYPE_UPDATED")

    def static_color_updated(self, color):
        self.static_color = color
        self.send_update("STATIC_COLOR_UPDATED")


    def color_1_time_updated(self, time):
        self.color_1_time =  time
        self.send_update("COLOR_1_TIME_UPDATED")

    def color_2_time_updated(self, time):
        self.color_2_time =  time
        self.send_update("COLOR_2_TIME_UPDATED")

    def color_1_updated(self,color):
        self.color_1 = color
        self.send_update("COLOR_1_UPDATED")

    def color_2_updated(self,color):
        self.color_2 = color
        self.send_update("COLOR_2_UPDATED")

    def from_color_updated(self, color):
        self.from_color = color
        self.send_update("FROM_COLOR_UPDATED")

    def to_color_updated(self,color):
        self.to_color = color
        self.send_update("TO_COLOR_UPDATED")

