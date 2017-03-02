
from PygameStuff.FunctionScheduler import *



# Return a schedule that makes an object blink
# between color1 and color2
#
# ticks1 and ticks2 are the amount of ticks to stay on the respective colors
# always starts in color1
def blink(light, color1, color2, ticks1, ticks2, ticks):
    s = ColorSchedule()

    counter = 0

    while (counter < ticks):
        add_color(light, color1, ticks1, s, ticks)
        counter += ticks1

        add_color(light, color2, ticks1, s, ticks)
        counter += ticks2

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


def fade_colors(light, color_from, color_to, ticks):

    to_r, to_g, to_b = color_to
    from_r, from_g, from_b = color_from

    dist_r = (to_r - from_r)/ticks
    dist_g = (to_g - from_g)/ticks
    dist_b =  (to_b - from_b)/ticks

   # print("dist: r:{} g:{} b:{}".format(dist_r, dist_g, dist_b))

    cur_r = from_r
    cur_g = from_g
    cur_b = from_b

    s = ColorSchedule()

    for x in range(ticks+1):
        cur_color = (cur_r, cur_g, cur_b)
        next_task = Task(light.set_color, (cur_color))
       # print(cur_color)
        s.add_task(next_task)

        cur_r += dist_r
        cur_g += dist_g
        cur_b += dist_b

    return s