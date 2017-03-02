from Display import *
from FunctionScheduler import *
from ObjectColors import *
from ObjectMovements import *

from BPMTools import *
from PygameStuff.Light import *


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
    def __init__(self, light, move_schedule, color_schedule, id=None ):
        self.light = light
        self.move_schedule_data = move_schedule
        self.color_schedule_data = color_schedule
        self.move_schedule = move_schedule
        self.color_schedule = color_schedule
        self.rendered=False
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

    def render_schedules(self):
        self.move_schedule = render_schedule_datas(self.move_schedule_data)
        self.color_schedule = render_schedule_datas(self.color_schedule)
        self.rendered = True







    pass


#Render a list of schedule data into a single schedule object
def render_schedule_datas(self, schedule_data):
    s = Schedule()
    for d in schedule_data:
        s.add_schedule(d.render_to_schedule())

    return s

def main():

    dis = Display()
    scene = Scene(dis)

    light1 = Circle(dis.screen, (255,0,0), (50,50),15,0)
    light2 = Circle(dis.screen, (255, 0, 0), (100, 105), 15, 0)
    light3 = Circle(dis.screen, (255, 0, 0), (210,105 ), 15, 0)
    light = Circle(dis.screen, (255, 0, 0), (100, 0), 15, 0)

    move_schedule1 = move_light_circle(light, dis.get_center(), 720, 128)
    move_schedule2 = move_light_circle(light1, dis.get_center(), 720, 128)
    move_schedule3 = move_light_circle(light2, dis.get_center(), 720, 128)
    move_schedule4 = move_light_circle(light3, dis.get_center(), 720, 128)


    color_schedule = fade_colors(light, (255, 0, 0), (0, 255, 0), 128)

    flash_sched = blink(light, color_schedule.get_final_color(), (255,255,255), 2,2,128)

    color_schedule.add_task(flash_sched)



    scene.add_instance(Object_Instance(light,move_schedule1
                                       , color_schedule))

    scene.add_instance(Object_Instance(light1, move_schedule2
                                       , color_schedule))

    scene.add_instance(Object_Instance(light2, move_schedule3
                                       , color_schedule))

    scene.add_instance(Object_Instance(light3, move_schedule4
                                       , color_schedule))

    BPMtrigger(128, scene, 256)
    dis.main_menu()

if __name__ == "__main__":
    main()