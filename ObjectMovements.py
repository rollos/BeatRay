from math import *

import time

from SceneModel import *
from Utils import _create_circle
from Utils import *
from LightFrame import *




def tester():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200, borderwidth=0, highlightthickness=0, bg="black")
    canvas.grid()

    tk.Canvas.create_circle = _create_circle


    frames = make_line_frames(20, 20, "Circle", (0, 0), (100, 100))


    frame_counter = 0

    while True:

        time.sleep(.1)

        canvas.delete("all")
        try:
            frames[frame_counter].draw(canvas)
        except:
            break


        frame_counter += 1
        root.update_idletasks()
        root.update()


def move_render_to_frames(clip):

    frame_length = bars_to_ticks(clip.clip_length)
    light_size = clip.parent_light.size
    type = clip.parent_light.shape
    start_frame = bars_to_ticks(clip.clip_start)


    if clip.type == "None":
        return make_static_frames(frame_length, light_size, type, clip.static_location, start_frame)

    elif clip.type == "Line":
        return make_line_frames(frame_length, light_size, type, start_frame)

    elif clip.type == "Circle":
        return make_circle_frames(clip)
    elif clip.type == "Spiral":
        return make_spiral_frames(clip)

def make_static_frames(frame_length, light_size, type, position, start_frame):
    frames = {}

    start_frame = int(round(start_frame))
    end_frame = start_frame + int(round(frame_length))

    for frame in range(start_frame, end_frame):
        model = LightFrameModel(light_size, type, position=position)
        print(frame)
        frames[frame] = model

    return frames


# Move the object in a straight line
# From the current location of the object to the pixels designated by destX, destY
# move_ticks will set the velocity
# Returns a Schedule with the correct move at each tick
def make_line_frames(frame_length, light_size, type, start, dest):
    frames = {}

    x, y = start
    # Calculate the distance between the current position and the final position on each axis
    # The sign of the number indicates the direction.
    x_distance = dest[0] - x
    y_distance = dest[1] - y

    # The distance per tick
    tick_dist_x = x_distance / frame_length
    tick_dist_y = y_distance / frame_length

    # Add a new task to move the object for every tick
    for i in range(frame_length):

        model = LightFrameModel(light_size, type, position=(x,y))
        frames[i] = model

        x = x + tick_dist_x
        y += tick_dist_y

    return frames




# Move an object in a circle around a center of rotation
# The radius of the path is the distance between the object and the center point when the function is called
# Degrees of rotation determines the distance around the circle the
def make_circle_frames(light, center_of_rotation, degrees_of_rotation, move_ticks):
    # Calculate the radius of the circle
    radius = get_distance(center_of_rotation, light.location)

    # print("COR = {}, r = {}".format(center_of_rotation,radius))
    # Calculate the amount of degrees to move each tick
    tick_dist = radians(degrees_of_rotation / move_ticks)

    #print("Degrees/Tick:{}".format(degrees(tick_dist)))

    theta = get_radians_from_point(center_of_rotation, light.location, radius)

    # print("Initial theta = {}".format(theta))

    s = MovementSchedule()

    for x in range(move_ticks+1):
        theta += tick_dist
        # if x==1:
        #     s.add_task(Task(time.sleep, (2)))
        next_task = Task(light.move, (get_point_circle(center_of_rotation, radius, theta)))
        s.add_task(next_task)

    return s


#Move the light in a spiral around a center of rotation.
#The initial radius is the distance between the center of rotation and the light
#
def make_spiral_frames(light, center_of_rotation, end_radius, degrees_of_rotation, move_ticks):
    # Calculate the radius of the circle
    radius = get_distance(center_of_rotation, light.location)

    # print("COR = {}, r = {}".format(center_of_rotation,radius))
    # Calculate the amount of degrees to move each tick
    rotation_dist = radians(degrees_of_rotation / move_ticks)
    radius_dist =  (end_radius-radius)/move_ticks

    #print("Degrees/Tick:{}".format(degrees(tick_dist)))

    theta = get_radians_from_point(center_of_rotation, light.location, radius)

    # print("Initial theta = {}".format(theta))

    s = MovementSchedule()

    for x in range(move_ticks+1):

        # if x==1:
        #     s.add_task(Task(time.sleep, (2)))
        next_task = Task(light.move, (get_point_circle(center_of_rotation, radius, theta)))
        s.add_task(next_task)

        theta += rotation_dist
        radius += radius_dist

    return s


# Get the distance between two points
def get_distance(point1, point2):
    x_len, y_len = get_dist_xy(point1,point2)

    # Pythagreoum Theroum
    return sqrt(x_len * x_len + y_len * y_len)


# Move an object directly to a destination, instead of moving a certain amount of pixels
def move_object_jump(object, dest):
    x_dist = dest.getX() - object.getCenter().getX()
    y_dist = dest.getY() - object.getCenter().getY()

    object.move(x_dist, y_dist)


# Get the coordinate of a point around a circle, based on theta
# theta must be in radians
def get_point_circle(center, radius, theta):
    x,y = center
    x_dist = radius * cos(theta)
    y_dist = radius * sin(theta)

    return (ceil(x_dist + x), ceil(y_dist + y))


# Calculate the radians from a center point and a point on the circle
# Based around a unit circle
# a point in the positive x direction with no change in y should = 0
def get_radians_from_point(center, point, radius):
    x_dist,y_dist = get_dist_xy(center,point)

    # cos(theta) = x_dist/radius

    return atan2(y_dist, x_dist)

def get_dist_xy(point1, point2):
    x_len = point1[0] - point2[0]
    y_len = point1[1] - point2[1]

    return (x_len,y_len)




if __name__ == "__main__":
    tester()