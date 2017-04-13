from FrameMakers.ObjectColors import *

from FrameMakers.ObjectMovements import *
from Models.ColorClipModel import ColorClipModel
from Models.MovementClipModel import MovementClipModel


class RenderedLight:
    def __init__(self, light, canvas):

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
        elif self.light.shape == "Strobe":
            self.light_id = self.canvas.create_rectangle(0,0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="black")


        self.canvas.tag_bind(self.light_id, "<ButtonPress-1>", self.on_token_press)


    def redraw_light(self, light):
        if self.light_id is not None:
            self.canvas.delete(self.light_id)

        self.light = light
        self.draw_light()


    def delete_light(self):
        self.canvas.delete(self.light_id)



    def resize_light(self, size):
        x, y = self.current_position
        self.canvas.coords(self.light_id, x - size, y - size, x + size, y + size)

    def color_light(self,color):
        if type(color) is tuple:
            color = convert_to_color(*color)

        if color == convert_to_color(0,0,0):
            self.canvas.tag_lower(self.light_id)

        self.canvas.itemconfig(self.light_id, fill=color, outline=color)



    def render_clips(self):
        movement_clips = [render_clip(clip) for clip in self.light.movement_clips]
        color_clips = [render_clip(clip) for clip in self.light.color_clips]

        self.frames = full_render(movement_clips, color_clips)

    def move_light_to_scrubber(self, scrubber_val):
        try:
            frame = self.frames[scrubber_val]
            x, y = frame.position


            radius = frame.radius


            if frame.light_type == "Circle":

                self.move_light(x, y, radius)




            self.color_light(frame.color)

        except:

            self.color_light("black")




    def move_light(self, x,y,size):
        self.current_position = (x,y)
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

    def on_token_press(self, *args):
        self.light.parent_scene.select_light(self.light.id)

        pass


def render_clip(clip):
    if type(clip) is MovementClipModel:
        return move_render_to_frames(clip)
    if type(clip) is ColorClipModel:
        return color_render_to_frames(clip)


def full_render(movement_clips, color_clips):
    pass