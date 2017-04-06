from ObjectMovements import move_render_to_frames
from Utils import*
import random



class ClipModel():
    def __init__(self, parent_light, id):

        self.id = id

        self.type = None
        self.parent_light = parent_light

        self.clip_length = DEF_CLIP_LENGTH
        self.clip_start = DEF_CLIP_START
        self.clip_end = self.clip_start + self.clip_length

        self.color = convert_to_color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))

        self.frames = None


    def send_update(self, message):
        self.parent_light.send_update(message)

    def clip_length_updated(self,length):
        self.clip_length = length
        self.send_update("CLIP_LENGTH_UPDATED")

    def clip_start_updated(self, start):
        print(start)
        self.clip_start = start
        self.send_update("CLIP_START_UPDATED")

    def clip_resized(self, value:dict):
        self.clip_start = value["start"]
        self.clip_end = value["end"]
        self.clip_length = self.clip_end - self.clip_start
        self.render_clip()

        if self.id == self.parent_light.selected_clip_id:
            self.send_update("SELECTED_CLIP_RESIZED")




    def clip_end_updated(self,end):
        self.clip_end = end
        self.send_update("CLIP_END_UPDATED")

    def clip_type_updated(self,type):
        self.type = type
        self.send_update("CLIP_TYPE_UPDATED")



    def render_clip(clip):
        pass



class MovementClipModel(ClipModel):

    def __init__(self, parent, id):
        super().__init__(parent, id)



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



    #Render to a dictionary of LightFranes
    def render_clip(self):
        self.clip_frames = move_render_to_frames(self)
        return self.clip_frames



class ColorClipModel(ClipModel):

    def __init__(self,parent, id):
        super().__init__(parent, id)

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
        self.color = convert_to_color(*color)
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

