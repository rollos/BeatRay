from Scene import *
from Light import *
from pygame import *

class SceneBuilder():

    def __init__(self,display):
        self.display = display
        self.scene = Scene(display)
        self.id_counter = 0

    def add_light(self):
        light = Light(self.display, color=(0,0,0))
        obj = Object_Instance(light=light, id=self.id_counter)
        self.scene.add_instance(obj)
        self.id_counter += 1

    def add_movement(self, light_id,
                     type=None):
        obj_inst = self.get_light_with_id(light_id)
        s = MovementSchedule()


        if obj_inst.movement_schedule is None:
            obj_inst.movement_schedule = s
        else:
            obj_inst.movement_schedule.add_schedule(s)






    def get_light_with_id(self, id):
        for obj in self.scene:
            if obj.id == id:
                return obj

