from queue import *
from time import sleep



#A Schedule is an ordered list of tasks to run
#
class Schedule:
    task_list = list()

    def __init__(self):
        self.schedule = Queue()
        self.task_list = []

    def __len__(self):
        return len(self.task_list)


    def __str__(self):
        ret_string = ""
        for x in range(len(self.initial_list)):
            ret_string += "Task {}: ".format(x) + str(self.initial_list[x])+"\n"

        return ret_string

    def __iter__(self):
        yield self.task_list

   # Run all of the tasks in the schedule
    # print_tasks flag will print the task that is running to the console, default False
    # delay sleeps for x seconds after each task run
    #

    def fast_run(self, delay=0, print_tasks=False):
        while not self.schedule.empty():
            task = self.schedule.get()
            task.run()
            if print_tasks:
                print("Running: {}".format(task))
            sleep(delay)


            # Run the first task on the queue

    def run_task(self, print_task=False):
        if self.schedule.empty():
            return False

        task = self.schedule.get()
        task.run()
        if print_task:
            print("Running: {}".format(task))

        return True

    def finished(self):
        return self.schedule.empty()

    def add_task(self,task):
        if type(task) == Task:
#        assert type(task) is Task, "Type of inserted object is not a Task"
            self.schedule.put(task)
            self.task_list.append(task)
            return

        self.add_schedule(task)
        return


    def add_schedule(self, schedule):
        for x in range(len(schedule)):
            new_task = Task(schedule.run_task)
            self.add_task(new_task)

class ColorSchedule(Schedule):
    def __init__(self):
        super().__init__()


    def get_final_color(self):
        if self.task_list == []:
            return None

        final_task = self.task_list[len(self.task_list)-1]
        final_color = final_task.args
       # print("Final color: {}".format(final_color))
        return final_color

class MovementSchedule(Schedule):
    def __init__(self):
        super().__init__()

    def get_final_location(self):
        if self.task_list == []:
            return None
        final_task = self.task_list[len(self.task_list)-1]
        final_loc = final_task.args
        return final_loc


#A task is a function and its arguments that is stored so it can be called upon at a specific time
class Task:
    def __init__(self, function, arguments=None):
        assert function, "Function passed is none"
        self.function = function
        self.args = arguments


    def __str__(self):
        if not self.args:
            return "{}()".format(self.function.__name__)
        elif len(self.args) < 2:
            return ("{}({})".format(self.function.__name__, self.args))
        else:
            return ("{}{}".format(self.function.__name__, self.args))

    # Run the function with the given arguments
    def run(self):
        if not self.args:
            self.function()
        elif len(self.args) == 1 or type(self.args) is tuple:
            self.function(self.args)
        else:
            self.function(*self.args)

#A helper fuction that does nothing
def do_nothing():
    pass

def main():
    pass

if __name__ == '__main__':
   main()