from FunctionScheduler import *
from ObjectMovements import *
from ObjectColors import *
from Display import *
from BPMGetter import *
from Light import *


class Scene:
    def __init__(self, display):
        self.instances = []
        self.length = 0
        self.display = display



    #Add an instance to the list of instances to run
    def add_instance(self, instance):
        assert type(instance) is Object_Instance, "Cannot add non-instances to a scene"
        self.instances.append(instance)

    #Run one frame of motion
    def run_frame(self):
        self.display.clear()    #Clear the screen
        for instance in self.instances: #Run one task in all of the instances
            ran = instance.run_task()

        self.display.main_menu()

        pygame.display.update() #Update the screen

    def fast_run_scene(self, delay=0):
        while len(self.instances) > 0:
            self.run_frame()
            sleep(delay)


    def __iter__(self):
        yield self.instances

#An instance is an object and its schedule
#Schedules will determine the movements for each object in the entire scene,
#And could even hold other schedules with sub-movements
class Object_Instance:
    def __init__(self, light, move_schedule = None, color_schedule = None, id=None ):
        self.light = light
        self.move_schedule = move_schedule
        self.color_schedule = color_schedule
        self.id = id


       # if move_schedule and color_schedule:
           # assert len(move_schedule) == len(color_schedule), "Movement Schedule: {} and Color Schedule: {} must be the same length".format(len(move_schedule), len(color_schedule))

    def finished(self):
        if (self.move_schedule and self.move_schedule.finished()):
            return False
        if(self.color_schedule and  self.color_schedule.finished()):
            return False
        return True



    def run_task(self):
        # if self.finished():
        #     #print("move_schedule: {}, color:{}".format(self.move_schedule.finished(), self.color_schedule.finished()))
        #     return False

        if self.move_schedule:
            self.move_schedule.run_task()

        if self.color_schedule:
            self.color_schedule.run_task()

        self.light.draw()


        return True


    pass

def main():

    dis = Display()
    scene = Scene(dis)

    light = Circle(dis, (255,0,0), dis.get_center(),15,0)

    move_schedule = move_light_spiral(light, dis.get_center(), 200, 720, 128)

    line_sched = move_light_straight(light, move_schedule.get_final_location(), dis.get_center(), 128)

    move_schedule.add_task(line_sched)

    color_schedule = fade_colors(light, (255, 0, 0), (0, 255, 0), 128)

    flash_sched = blink(light, color_schedule.get_final_color(), (255,255,255), 2,2,128)

    color_schedule.add_task(flash_sched)



    scene.add_instance(Object_Instance(light,move_schedule
                                       , color_schedule))

    BPMtrigger(128, scene, 256)
    dis.main_menu()

if __name__ == "__main__":
    main()