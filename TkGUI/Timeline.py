from math import floor

from Models.MovementClipModel import MovementClipModel
from Models.ColorClipModel import ColorClipModel
from Utils.Utils import *
import tkinter as tk

class TimelineContainer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initialize()
        self.scene_length = DEF_SCENE_LENGTH



    def initialize(self):
        self.move_timeline = MovementTimeline(self)
        self.color_timeline = ColorTimeline(self)

        self.move_timeline.pack( fill=tk.BOTH, expand=tk.YES)
        self.color_timeline.pack( fill=tk.BOTH, expand=tk.YES)
        
    def create_clip(self):
        #length of clip in beats
        length=4
        
    def set_length(self, beats):
        self.scene_length = beats
        self.move_timeline.set_length(beats)
        self.color_timeline.set_length(beats)

    def message_view(self, message, value=None):
        self.parent.message_view(message, value)

    def update_scrubbers(self, scrubber_frame):
        self.move_timeline.move_scrubber(scrubber_frame)
        self.color_timeline.move_scrubber(scrubber_frame)





class Timeline(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent, height=200, relief=tk.GROOVE, borderwidth=5)

        self.canvas = tk.Canvas(self, height = 50, background= "GREY")

        coords = (0, 0, 100, 100)

        self.scrubber = Scrubber(self, self.canvas)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.clip_dict = None

        self.length= None

        self.clips = []


        self.canvas.bind("<Configure>", lambda x: self.message_view("WINDOW_RESIZE"))




    def set_length(self, length):
        self.length = length
        if self.clip_dict is not None:
            self.draw_all_clips(self.clip_dict)

    def draw_all_clips(self, clip_dict:dict):
        self.clip_dict = clip_dict
        self.canvas.delete("all")

        self.scrubber.draw_scrub()

        self.canvas.tag_raise(self.scrubber.id)

        if len(clip_dict) > 0:
            for clip in clip_dict.values():
                self.draw_clip(clip)

    def draw_clip(self, clip):
        #Override in child class
        pass

    def get_canvas_width(self):
        return self.canvas.winfo_width()

    def get_canvas_height(self):
        return self.canvas.winfo_height()

    def get_pix_per_frame(self):
        pix_width = self.get_canvas_width()

        #Length in bars


        return pix_width/self.length

    def move_scrubber(self, scrubber_frame):
        scrub_pix = self.get_pix_per_frame() * scrubber_frame

        self.scrubber.set_scrub_time(scrub_pix)


    def message_view(self, message, value=None):
        self.parent.message_view(message, value)





class MovementTimeline(Timeline):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)

        self.clips = []




    def draw_clip(self, clip:MovementClipModel):
        c = Clip(self, self.canvas, clip)
        self.clips.append(c)






class ColorTimeline(Timeline):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(parent)

        self.clips = []

    def draw_clip(self, clip:ColorClipModel):
        c = Clip(self, self.canvas, clip)
        self.clips.append(c)



class Scrubber():
    def __init__(self, parent, canvas:tk.Canvas):
        self.canvas = canvas
        self.parent = parent

        self.coords = (1,0,1,0)
        self.draw_scrub()

        self.id = None
        self.canvas.update()

    def draw_scrub(self):
        self.id = self.canvas.create_line(*self.coords, fill="black", width=1)
        self.canvas.tag_raise(self.id)

    def set_scrub_time(self, scrub_pix):
        self.coords = (scrub_pix+1, 0, scrub_pix+1, 1000)
        self.canvas.tag_raise(self.id)
        self.canvas.coords(self.id, *self.coords)



class Clip():
    def __init__(self,parent, canvas:tk.Canvas, clip):
        self.canvas = canvas
        self.clip = clip
        self.parent = parent

        pix_per_frame = parent.get_pix_per_frame()

        start = clip.clip_start
        end = clip.clip_end


        start_frame = beats_to_tick(start)
        end_frame = beats_to_tick(end)

        self.start_pix = floor(start_frame * pix_per_frame)
        self.end_pix = floor(end_frame * pix_per_frame)
        self.height = parent.get_canvas_height()

        self.drag = NO_DRAG

        self.drag_data = None


        coords = (self.start_pix, 0, self.end_pix, self.height)



        self.rect_clip = self.canvas.create_rectangle(*coords, fill=clip.color)
        self.text = self.canvas.create_text(self.start_pix+5, 5, anchor="nw", font=("Courrier", 20), text=clip.type)


        self.canvas.tag_bind(self.rect_clip, "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind(self.rect_clip, "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind(self.rect_clip, "<B1-Motion>", self.on_token_motion)


    def on_token_press(self, event):
        x = self.convert_to_relative(event.x)




        #If its a click on the start
        if x < 10:
            self.drag = START_DRAG

        #If its a click on the end
        elif self.end_pix - event.x < 10:
            self.drag = END_DRAG

        else:
            self.drag = CLIP_DRAG
            self.drag_data = event.x


    def on_token_release(self,event):



        if self.drag != NO_DRAG:
            self.message_view("CLIP_RESIZED", value=(self.clip.id, self.get_start_end_ticks()))
            self.drag = NO_DRAG

        self.select_clip()

    def on_token_motion(self,event):


        if self.drag == START_DRAG :
            if event.x >= 0 and self.check_min_size():
             self.start_pix = event.x
            else:
                self.start_pix = self.end_pix - self.parent.get_pix_per_frame()


        elif self.drag == END_DRAG:
            if event.x <= self.parent.get_canvas_width() and self.check_min_size():
              self.end_pix = event.x

            else:

                pass
                self.end_pix = self.start_pix + self.parent.get_pix_per_frame()

        elif self.drag == CLIP_DRAG:
            dist = event.x - self.drag_data
            self.drag_data = event.x


            if self.end_pix + dist < self.parent.get_canvas_width() and self.start_pix + dist > 0:
                self.end_pix = self.end_pix + dist
                self.start_pix = self.start_pix + dist


        self.resize()

    def convert_to_relative(self, x_coord):
        return x_coord - self.start_pix

    def convert_to_absolute(self, x_coord):
        return x_coord + self.start_pix


    def check_min_size(self):
        if self.end_pix - self.start_pix > self.parent.get_pix_per_frame():
            return True
        else:
            return False

    def resize(self):
        self.length = self.end_pix - self.start_pix


        self.canvas.coords(self.text, self.start_pix+5, 5)
        self.canvas.coords(self.rect_clip, self.start_pix, 0, self.end_pix, self.parent.get_canvas_height())



    def get_start_end_ticks(self):
        return {"start":self.convert_pix_to_beats(self.start_pix),
                "end":self.convert_pix_to_beats(self.end_pix)}



    def convert_pix_to_beats(self, pix):
        pix_per_tick = self.parent.get_pix_per_frame()

        if pix != 0:
            return  (ticks_to_beat(pix / pix_per_tick))
        else: return 0




    def message_view(self, message, value=None):

        self.parent.message_view(message, value)

    def select_clip(self):
        self.message_view("CLIP_SELECTED", value=self.clip.id)


NO_DRAG = 0
START_DRAG = 1
END_DRAG = 2
CLIP_DRAG = 3

        
        
