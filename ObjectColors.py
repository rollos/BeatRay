
from PygameStuff.FunctionScheduler import *
from Utils import *
from LightFrame import *

def color_render_to_frames(clip):
    frame_length = beats_to_tick(clip.clip_length)
    light_size = clip.parent_light.size
    shape = clip.parent_light.shape
    start_frame = beats_to_tick(clip.clip_start)

    start_frame = beats_to_tick(int(round(clip.clip_start)))
    end_frame = start_frame + int(round(frame_length))


    if clip.type == "None":
        return make_static_color_frames(start_frame, end_frame, frame_length,
                                        light_size, shape, clip.color)
    elif clip.type == "Blink":
        return  blink(start_frame, end_frame, frame_length,light_size, shape,
                      clip.color_1, clip.color_2,
                      clip.color_1_time, clip.color_2_time)
    elif clip.type == "Fade":
        return fade_colors(start_frame, end_frame, frame_length,light_size, shape,
                           clip.from_color, clip.to_color)

def make_static_color_frames(start_frame, end_frame, frame_length, light_size, shape, color):
    frames = {}


    for frame in range(start_frame, end_frame):
        model = LightFrameModel(light_size, shape, color=color)
      #  print(frame)
        frames[frame] = model

    return frames
# Return a schedule that makes an object blink
# between color1 and color2
#
# ticks1 and ticks2 are the amount of ticks to stay on the respective colors
# always starts in color1
def blink(start_frame, end_frame, frame_length, light_size, shape, color1, color2, ticks1, ticks2):
    s = {}

    frame_counter = start_frame

    while frame_counter < end_frame:
        for x in range(int(round(ticks1))):
            s[frame_counter] = LightFrameModel(light_size, shape, color=color1)
            frame_counter+=1

        for x in range(int(round(ticks2))):

            s[frame_counter] = LightFrameModel(light_size, shape, color=color2)
            frame_counter += 1




    return s



def add_color(light, color, ticks, schedule, length):
    # Add
    for x in range(ticks+1):
        if len(schedule) != length:
            if x == 0:
                print("Setting color: {}".format(color))
                next_task = Task(light.set_color, (color))
                schedule.add_task(next_task)
            else:
                schedule.add_task(Task(do_nothing))


def fade_colors(start_frame, end_frame, frame_length, light_size, shape, color_from, color_to):

    to_r, to_g, to_b = color_to
    from_r, from_g, from_b = color_from

    dist_r = (to_r - from_r)/frame_length
    dist_g = (to_g - from_g)/frame_length
    dist_b =  (to_b - from_b)/frame_length

   # print("dist: r:{} g:{} b:{}".format(dist_r, dist_g, dist_b))

    cur_r = from_r
    cur_g = from_g
    cur_b = from_b

    s = {}

    for frame in range(start_frame, end_frame):
        cur_color = (int(round(cur_r)), int(round(cur_g)), int(round(cur_b)))
        next_task = LightFrameModel(light_size, shape, color = cur_color)
       # print(cur_color)
        s[frame] = next_task

        cur_r += dist_r
        cur_g += dist_g
        cur_b += dist_b

    return s