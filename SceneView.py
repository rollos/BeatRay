from TkGUI import *
from TkGUI.MainApp import *
from Utils import *
from SceneModel import LightModel, ColorClipModel, MovementClipModel


class SceneView():
    def __init__(self, gui: MainApplication):
        self.observers = []
        self.gui = gui

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
         #   try:
            observer.update(VIEWUPDATE, message)
            #except AttributeError:
             #   raise AttributeError("Scene: Observer does not have update() function")

    def set_bpm(self, bpm):
        self.gui.play_controls.bpm_entry.set_entry(bpm)

    def get_bpm(self):
        return self.gui.play_controls.bpm_entry.get_entry()

    def update_play_button_state(self,state):
        self.gui.play_controls.update_play_button(state)

    def get_scene_length(self):
        return self.gui.play_controls.scene_length_entry.get_entry()

    def get_size(self):
        return self.gui.selected_light.get_light_size()


    def get_selected_light(self):
        return self.gui.selected_light.light_selector_box.get_entry()

    def get_light_type(self):
        return self.gui.selected_light.light_type_var.get()

    def get_clip_length(self):
        return self.gui.selected_clip.location_boxes.get_length()

    def get_clip_start(self):
        return self.gui.selected_clip.location_boxes.get_start()

    def get_clip_end(self):
        return self.gui.selected_clip.location_boxes.get_end()



    # COLOR CLIP GETS
    def get_static_color(self):
        return self.gui.selected_clip.static_color_selector.get_color()

    def get_color_1(self):
        return self.gui.selected_clip.color_1_selector.get_color()

    def get_color_2(self):
        return self.gui.selected_clip.color_2_selector.get_color()

    def get_color_1_time(self):
        return self.gui.selected_clip.color_1_time.get_entry()

    def get_color_2_time(self):
        return self.gui.selected_clip.color_2_time.get_entry()


    def get_from_color(self):
        return self.gui.selected_clip.from_color_selector.get_color()

    def get_to_color(self):
        return self.gui.selected_clip.to_color_selector.get_color()

    def get_selected_clip(self):
        return self.gui.selected_light.clip_selector_box.get_entry()


    def get_static_location(self):
        return self.gui.selected_clip.static_location_entry.get_location()

    def get_start_location(self):
        return self.gui.selected_clip.start_location_entry.get_location()

    def get_end_locaton(self):
        return self.gui.selected_clip.end_location_entry.get_location()

    def get_c_center_location(self):
        return self.gui.selected_clip.c_center_location_box.get_location()

    def get_c_radius(self):
        return self.gui.selected_clip.c_radius_box.get_entry()

    def get_c_start_degrees(self):
        return self.gui.selected_clip.c_start_degrees_box.get_entry()

    def get_c_end_degrees(self):
        return self.gui.selected_clip.c_end_degrees_box.get_entry()

    def get_s_center_location(self):
        return self.gui.selected_clip.s_center_location_box.get_location()

    def get_s_start_degrees(self):
        return self.gui.selected_clip.s_start_degrees_box.get_entry()

    def get_s_end_degrees(self):
        return self.gui.selected_clip.s_end_degrees_box.get_entry()

    def get_s_start_radius(self):
        return self.gui.selected_clip.s_start_radius_box.get_entry()

    def get_s_end_radius(self):
        return self.gui.selected_clip.s_end_radius_box.get_entry()



    def display_light(self, light: LightModel):
        self.gui.selected_light.display_light(light)
        self.display_clip(None)

    def display_clip(self, clip):
        if self.gui.selected_clip is not None:
            self.gui.selected_clip.grid_forget()

        if type(clip) is ColorClipModel:
            self.gui.selected_clip = self.gui.color_clip
            self.gui.selected_clip.display_clip(clip)

        elif type(clip) is MovementClipModel:
            self.gui.selected_clip = self.gui.movement_clip
            self.gui.selected_clip.display_clip(clip)

    def get_clip_type(self):
        return self.gui.selected_clip.type_var.get()



