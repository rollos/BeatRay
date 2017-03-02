from FunctionScheduler import *

from PygameStuff.ObjectMovements import *


class ObjInstData():
    def __init__(self, light):
        self.light = light
        self.type = None
        self.args = None
        self.tick_length = 0

    def select_type(self, kwargs):
        self.type = kwargs["type"]
        self.tick_length = kwargs["tick_length"]
        if type is not None:
            self.args = kwargs

    def render_to_schedule(self):
        ##Must be overwritten
        pass

class MoveData(ObjInstData):
    def __init__(self,light):
        super().__init__(light)

    def render_to_schedule(self):
        if self.type is None:
            s = Schedule()
            for x in range(self.tick_length):
                s.add_task(Task(do_nothing()))

        elif self.type == "Line":
            start = self.args["start"]
            dest = self.args["dest"]

            s=move_light_straight(self.light,start,dest, self.tick_length)

        elif self.type == "Circle":
            center_of_rotation = self.args["center_of_rotation"]
            degrees_of_rotation = self.args["degrees_of_rotation"]

            s = move_light_circle(self.light,center_of_rotation, degrees_of_rotation,self.tick_length)

        elif self.type == "Spiral":
            end_radius = self.args["end_radius"]
            center_of_rotation = self.args["center_of_rotation"]
            degrees_of_rotation = self.args["degrees_of_rotation"]

            s = move_light_spiral(self.light, center_of_rotation, end_radius, degrees_of_rotation, self.tick_length)

        else:
            raise Exception("Unknown type when trying to render movement schedule")


        return s








class ColorData(ObjInstData):
    pass