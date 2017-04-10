from FrameMakers.ObjectColors import color_render_to_frames
from Models.ClipModels import ClipModel
from Utils.Utils import beats_to_tick, convert_to_color
from Utils.Defaults import DEF_COLOR_CLIP_TYPE, DEF_STATIC_COLOR, DEF_COLOR_1_TIME, DEF_COLOR_2_TIME, DEF_COLOR_1, \
    DEF_COLOR_2, DEF_FROM_COLOR, DEF_TO_COLOR


class ColorClipModel(ClipModel):

    def __init__(self,parent, id=None,state=None):
        super().__init__(parent, id, state)

        if state is not None:
            self.type = state["type"]
            self.static_color = state["static_color"]
            self.color_1_time = state["color_1_time"]
            self.color_2_time = state["color_2_time"]
            self.color_1 = state["color_1"]
            self.color_2 = state["color_2"]
            self.from_color = state["from_color"]
            self.to_color = state["to_color"]
        else:
            self.type = DEF_COLOR_CLIP_TYPE
            self.static_color = DEF_STATIC_COLOR
            self.color_1_time = beats_to_tick(DEF_COLOR_1_TIME)
            self.color_2_time = beats_to_tick(DEF_COLOR_2_TIME)
            self.color_1 = DEF_COLOR_1
            self.color_2 = DEF_COLOR_2
            self.from_color = DEF_FROM_COLOR
            self.to_color = DEF_TO_COLOR




    def render_clip(self):
        self.clip_frames = color_render_to_frames(self)
        return self.clip_frames

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