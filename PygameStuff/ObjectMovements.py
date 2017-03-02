from math import *

from PygameStuff.FunctionScheduler import *


# Move the object in a straight line
# From the current location of the object to the pixels designated by destX, destY
# move_ticks will set the velocity
# Returns a Schedule with the correct move at each tick
def move_light_straight(light, start, dest, move_ticks):
    s = MovementSchedule()

    x, y = start
    # Calculate the distance between the current position and the final position on each axis
    # The sign of the number indicates the direction.
    x_distance = dest[0] - x
    y_distance = dest[1] - y

    # The distance per tick
    tick_dist_x = x_distance / move_ticks
    tick_dist_y = y_distance / move_ticks

    # Add a new task to move the object for every tick
    for i in range(move_ticks+1):

        next_task = Task(light.move, (ceil(x), ceil(y)))  # Create a task that calls light.move(x,y)
        s.add_task(next_task)  # Add it to the schedule
        x = x + tick_dist_x
        y += tick_dist_y

    return s


# Move an object in a circle around a center of rotation
# The radius of the path is the distance between the object and the center point when the function is called
# Degrees of rotation determines the distance around the circle the
def move_light_circle(light, center_of_rotation, degrees_of_rotation, move_ticks):
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
def move_light_spiral(light, center_of_rotation, end_radius, degrees_of_rotation, move_ticks):
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