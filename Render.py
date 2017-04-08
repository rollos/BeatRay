from ClipModels import MovementClipModel
from ObjectMovements import *
import tkinter as tk
from LightFrame import *





class RenderedLight:
    def __init__(self, light, canvas:tk.Canvas):
        self.light = light
        self.canvas = canvas

        self.light_id = None

        self.frames = {}

        self.current_position = (100, 100)

        self.render_clips()

        self.draw_light()

    def draw_light(self):
        if self.light.shape == "Circle":
            self.light_id = self.canvas.create_circle(*self.current_position,
                                                      self.light.size,
                                                      fill="black")

    def resize_light(self, size):
        x, y = self.current_position
        self.canvas.coords(self.light_id, x - size, y - size, x + size, y + size)

    def color_light(self,color):
        if type(color) is tuple:
            self.canvas.itemconfig(self.light_id, fill=convert_to_color(*color))
        elif type(color) is str:
            self.canvas.itemconfig(self.light_id, fill=color)
        else:
            raise ValueError

    def render_clips(self):
        movement_clips = [render_clip(clip) for clip in self.light.movement_clips]
        color_clips = [render_clip(clip) for clip in self.light.color_clips]

        self.frames = full_render(movement_clips, color_clips)

    def move_light_to_scrubber(self, scrubber_val):
        try:
            frame = self.frames[scrubber_val]
            x, y = frame.position
            radius = frame.radius

            self.current_position = (x,y)

            self.move_light(x, y, radius)
            self.color_light(frame.color)
        except:
            self.canvas.tag_lower(self.light_id)
            self.color_light("black")




    def move_light(self, x,y,size):
        self.canvas.coords(self.light_id, x - size, y - size, x + size, y + size)

    def update_schedules(self, move_frames, color_frames):
        self.frames = {}

        for clip_frames in move_frames:
            for frame in clip_frames:
                self.frames[frame] = clip_frames[frame]

        for clip_frames in color_frames:
            for frame in clip_frames:
                if frame in self.frames:
                    self.frames[frame].color = clip_frames[frame].color
                else:
                    self.frames[frame] = clip_frames[frame]


      #  self.fill_empty_frames()

        pass

    def fill_empty_frames(self):
        most_recent_frame = None
        frame_end = bars_to_ticks(self.light.parent_scene.scene_length)
        for x in range(0, frame_end):
            try:
                most_recent_frame = self.frames[x]
            except KeyError:
                if x ==0:
                    raise BaseException("Must have something at the beginning of the scene to anchor the light")
                else:
                    self.frames[x] = most_recent_frame



def render_clip(clip):
    if type(clip) is MovementClipModel:
        return move_render_to_frames(clip)


def full_render(movement_clips, color_clips):
    pass