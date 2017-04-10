from FrameMakers.Render import RenderedLight
from Models.ColorClipModel import ColorClipModel
from Models.MovementClipModel import MovementClipModel
from Utils.Defaults import *


class LightModel():

    def __init__(self, parent_scene, id=None, state=None, duplicate=False):
        self.parent_scene = parent_scene
        self.movement_clips = {}
        self.color_clips = {}

        if state is None:
            self.id = id


            self.size = DEF_LIGHT_SIZE
            self.shape = DEF_SHAPE
            self.clip_id_counter = 0



            self.selected_clip_id = None


        else:
            print(state)
            if duplicate:
                self.id = id
            else:
                self.id = state["id"]
            self.size = state["size"]
            self.shape = state["shape"]
            self.clip_id_counter = state["clip_id_counter"]

            self.selected_clip_id = None

            for clip in state["color_clips"]:
                self.color_clips[clip["id"]] = ColorClipModel(self, id, clip)

            for clip in state["movement_clips"]:
                self.movement_clips[clip["id"]] = MovementClipModel(self, id, clip)


        self.rendered_light = RenderedLight(self, self.parent_scene.canvas)


        print(self.__dict__)

    def update_display_light(self, scrubber):
        #self.render_schedules()
        self.rendered_light.move_light_to_scrubber(scrubber)

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
        self.render_schedules()

        self.clip_id_counter += 1

    def new_color_clip(self):
        color_clip = ColorClipModel(self, self.clip_id_counter)

        self.color_clips[self.clip_id_counter] = color_clip
        self.select_clip(self.clip_id_counter)
        self.render_schedules()
        self.clip_id_counter += 1

    def update_size(self, size):
        self.size = size
        self.rendered_light.resize_light(size)

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


    #Render all the schedules into the RenderedLight for this Lightmodel
    def render_schedules(self):
        move_frames = []

        #create a list of dictionaries that represent the frames in each clip
        for clip in self.movement_clips.values():
            move_frames.append(clip.render_clip())

        #Do this for color frames as well
        color_frames = []
        for clip in self.color_clips.values():
            color_frames.append(clip.render_clip())

        self.rendered_light.update_schedules(move_frames, color_frames)

    def __getstate__(self):
        d = {}
        d["id"] = self.id
        d["size"] = self.size
        d["shape"] = self.shape
        d["clip_id_counter"] = self.clip_id_counter



        d["movement_clips"] = [clip.__getstate__() for clip in self.movement_clips.values()]
        d["color_clips"] = [clip.__getstate__() for clip in self.color_clips.values()]

        return d