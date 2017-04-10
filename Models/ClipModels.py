import random

from Utils.Utils import *


class ClipModel():
    def __init__(self, parent_light, id=None, state=None):

        if state is not None:

            self.clip_length = state["clip_length"]
            self.clip_start = state["clip_start"]
            self.clip_end = state["clip_end"]
            self.id = state["id"]
            self.color = state["color"]

        else:

            self.id = id

            self.type = None

            self.clip_length = DEF_CLIP_LENGTH
            self.clip_start = DEF_CLIP_START
            self.clip_end = self.clip_start + self.clip_length

            self.color = convert_to_color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))

        self.parent_light = parent_light
        self.frames = None

    def __getstate__(self):
        d = self.__dict__
        del d["parent_light"]
        del d["clip_frames"]
        return d

    def send_update(self, message):
        self.parent_light.send_update(message)

    def clip_length_updated(self,length):
        self.clip_length = length
        self.clip_end = self.clip_start + length
        self.send_update("CLIP_LENGTH_UPDATED")

    def clip_start_updated(self, start):
      #  print(start)
        self.clip_start = start
        self.clip_end = start + self.clip_length
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
        self.clip_length = end - self.clip_start
        self.send_update("CLIP_END_UPDATED")

    def clip_type_updated(self,type):
        self.type = type
        self.send_update("CLIP_TYPE_UPDATED")



    def render_clip(clip):
        pass



