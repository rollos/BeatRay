from Models.LiveModel import *
from Views.LiveView import *
class LiveController():
    def __init__(self, model:LiveModel, view:LiveView):
        self.model = model
        self.view = view

        self.model.set_midi_input(self.view.get_midi_input())