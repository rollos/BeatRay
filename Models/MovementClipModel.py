from FrameMakers.ObjectMovements import move_render_to_frames
from Models.ClipModels import ClipModel
from Utils.Defaults import DEF_MOVEMENT_CLIP_TYPE, DEF_STATIC_LOCATION, DEF_START_LOCATION, DEF_END_LOCATION, \
    DEF_C_CENTER_LOCATION, DEF_C_START_DEGREES, DEF_C_END_DEGREES, DEF_C_RADIUS, DEF_S_CENTER_LOCATION, \
    DEF_S_END_DEGREES, DEF_S_START_RADIUS, DEF_S_END_RADIUS


class MovementClipModel(ClipModel):

    def __init__(self, parent, id=None, state=None):
        super().__init__(parent, id, state)

        if state is not None:
            self.type = state["type"]
            self.static_location = state["static_location"]

            self.start_location = state["start_location"]
            self.end_location = state["end_location"]

            self.c_center_location = state["c_center_location"]
            self.c_start_degrees = state["c_start_degrees"]
            self.c_end_degrees = state["c_end_degrees"]
            self.c_radius = state["c_radius"]

            self.s_center_location = state["s_center_location"]
            self.s_start_degrees = state["s_start_degrees"]
            self.s_end_degrees = state["s_end_degrees"]
            self.s_start_radius = state["s_start_radius"]
            self.s_end_radius = state["s_end_radius"]
        else:
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
        self.c_end_degrees = degrees
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