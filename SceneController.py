from Utils import *
from SceneModel import *
from SceneView import *
import pickle

class SceneController():
    def __init__(self, SceneModel: SceneModel, SceneView: SceneView, root:tk.Tk):
        self.scene_model = SceneModel
        self.scene_view = SceneView

        self.scene_model.register_observer(self)

        self.scene_view.register_observer(self)

        self.scene_model.canvas = self.scene_view.gui.display_window.canvas


        self.scene_view.update_scene_length(self.scene_model.scene_length)

        SceneModel.new_light()

        self.main_loop(root)





    def main_loop(self, root):
        while (True):

            root.update_idletasks()
            root.update()


            if self.scene_model.play_state == PLAY_STATE:
                #Delay the clock so that it matches the current bpm (in midi  so 24 ticks per beat)
                self.scene_model.bpm_delay()

                self.scene_model.advance_scrubber()




    def play_pressed(self):
        self.scene_model.switch_play_state()


    def update(self, event_type, message, value=None):

        #If we get an update from the model, update the view
        if event_type == MODELUPDATE:
            print("Controller received message from MODEL: {}".format(message))
            self.update_view(message, value)

        #If we get an update from the view, update the model
        elif event_type == VIEWUPDATE:
            print("Controller received message from VIEW: {}".format(message))
            self.update_model(message, value)

    #When the view is updated, update the model
    def update_model(self, message,value=None):
        if message == "SAVE_SCENE":
            fn = self.scene_view.get_save_filename()
            if fn is not None:
                f = open(fn, "wb")
                pickle.dump(self.scene_model, f)
                f.close()

        if message == "LOAD_SCENE":
            fn = self.scene_view.get_load_filename()
            if fn is not None:
                f = open(fn, "rb")

                self.scene_model = pickle.load(f)

                self.scene_model.canvas = self.scene_view.gui.display_window.canvas

                self.scene_model.register_observer(self)

                self.scene_model.make_lights_from_state()

                f.close()
            print("loaded")

        if message == "BPM_UPDATE":
            self.scene_model.set_BPM(self.scene_view.get_bpm())
        elif message == "SCENE_LENGTH_UPDATE":
            self.scene_model.set_scene_length(self.scene_view.get_scene_length())
        elif message == "PLAY_PRESSED":
            self.scene_model.switch_play_state()
        elif message == "STOP_PRESSED":
            self.scene_model.stop_pressed()

        elif message == "LIGHT_SELECTED":
            selected_light = self.scene_view.get_selected_light()
            self.scene_model.select_light(selected_light)
        elif message == "CLIP_SELECTED":
            self.scene_model.get_selected_light().select_clip(value)

        elif message == "NEW_LIGHT":
            self.scene_model.new_light()
            self.scene_model.get_selected_light().rendered_light.draw_light(self.scene_view.gui.display_window.canvas)

        elif message == "NEW_MOVEMENT_CLIP":
            self.scene_model.new_movement_clip()
        elif message == "NEW_COLOR_CLIP":
            self.scene_model.new_color_clip()

        elif message == "CLIP_LENGTH_UPDATED":
            self.scene_model.get_selected_clip().clip_length_updated(self.scene_view.get_clip_length())
        elif message == "CLIP_START_UPDATED":
            self.scene_model.get_selected_clip().clip_start_updated(self.scene_view.get_clip_start())
        elif message == "CLIP_END_UPDATED":
            self.scene_model.get_selected_clip().clip_end_updated(self.scene_view.get_clip_end())
        elif message == "CLIP_TYPE_UPDATED":
            self.scene_model.get_selected_clip().clip_type_updated(self.scene_view.get_clip_type())
            self.update_lights_and_sched()

        elif message == "SIZE_UPDATED":
            self.scene_model.size_updated(self.scene_view.get_size())
        elif message == "LIGHT_TYPE_UPDATED":
            self.scene_model.light_type_updated(self.scene_view.get_light_type())


        #COLOR CLIP MESSAGES
        elif message == "STATIC_COLOR_UPDATED":
            self.scene_model.get_selected_clip().static_color_updated(self.scene_view.get_static_color())
            self.update_lights_and_sched()
        elif message == "COLOR_1_UPDATED":
            self.scene_model.get_selected_clip().color_1_updated(self.scene_view.get_color_1())
            self.update_lights_and_sched()
        elif message == "COLOR_2_UPDATED":
            self.scene_model.get_selected_clip().color_2_updated(self.scene_view.get_color_2())
            self.update_lights_and_sched()
        elif message == "COLOR_1_TIME_UPDATED":
            self.scene_model.get_selected_clip().color_1_time_updated(self.scene_view.get_color_1_time())
            self.update_lights_and_sched()
        elif message == "COLOR_2_TIME_UPDATED":
            self.scene_model.get_selected_clip().color_2_time_updated(self.scene_view.get_color_2_time())
            self.update_lights_and_sched()
        elif message == "FROM_COLOR_UPDATED":
            self.scene_model.get_selected_clip().from_color_updated(self.scene_view.get_from_color())
            self.update_lights_and_sched()
        elif message == "TO_COLOR_UPDATED":
            self.scene_model.get_selected_clip().to_color_updated(self.scene_view.get_to_color())
            self.update_lights_and_sched()


        #MOVEMENT CLIP MESSAGES
        elif message == "STATIC_LOCATION_UPDATED":
            self.scene_model.get_selected_clip().static_location_updated(self.scene_view.get_static_location())
            self.update_lights_and_sched()
        elif message == "START_LOCATION_UPDATED":
            self.scene_model.get_selected_clip().start_location_updated(self.scene_view.get_start_location())
            self.update_lights_and_sched()
        elif message == "END_LOCATION_UPDATED":
            self.scene_model.get_selected_clip().end_location_updated(self.scene_view.get_end_locaton())
            self.update_lights_and_sched()
        elif message == "C_CENTER_LOCATION_UPDATED":
            self.scene_model.get_selected_clip().c_center_location_updated(self.scene_view.get_c_center_location())
            self.update_lights_and_sched()
        elif message == "C_RADIUS_UPDATED":
            self.scene_model.get_selected_clip().c_radius_updated(self.scene_view.get_c_radius())
            self.update_lights_and_sched()
        elif message == "C_START_DEGREES_UPDATED":
            self.scene_model.get_selected_clip().c_start_degrees_updated(self.scene_view.get_c_start_degrees())
            self.update_lights_and_sched()
        elif message == "S_CENTER_LOCATION_UPDATED":
            self.scene_model.get_selected_clip().s_center_location_updated(self.scene_view.get_s_center_location())
            self.update_lights_and_sched()
        elif message == "S_START_RADIUS_UPDATED":
            self.scene_model.get_selected_clip().s_start_radius_updated(self.scene_view.get_s_start_radius())
            self.update_lights_and_sched()
        elif message == "S_END_RADIUS_UPDATED":
            self.scene_model.get_selected_clip().s_end_radius_updated(self.scene_view.get_s_end_radius())
            self.update_lights_and_sched()
        elif message == "S_START_DEGREES_UPDATED":
            self.scene_model.get_selected_clip().s_start_degrees_updated(self.scene_view.get_s_start_degrees())
            self.update_lights_and_sched()
        elif message == "S_END_DEGREES_UPDATED":
            self.scene_model.get_selected_clip().s_end_degrees_updated(self.scene_view.get_s_end_degrees())
            self.update_lights_and_sched()

        elif message == "CLIP_RESIZED":
            light = self.scene_model.get_selected_light()
            clip = light.get_clip(value[0])
            clip.clip_resized(value[1])
            self.scene_model.get_selected_light().render_schedules()


        elif message == "WINDOW_RESIZE":
            self.update_timelines()

    def update_lights(self):
        self.scene_model.update_display_lights()

    def update_lights_and_sched(self):

        self.scene_model.render_schedules()
        self.update_lights()


    # When the model is updated, update the view
    def update_view(self, message, *args):
        if message == "PLAY_STATE_UPDATE":
            self.scene_view.update_play_button_state(self.scene_model.play_state)
        elif message == "LIGHT_SELECTED": #If the selected light has been updated in the model, push the newly selected light to the view
            self.scene_view.display_light(self.scene_model[self.scene_model.selected_light_id])
            self.update_timelines()
        elif message == "CLIP_SELECTED": #If a new clip has been selected, push the newly selected clip to the view
            self.scene_view.display_clip(self.scene_model.get_selected_light().get_selected_clip())
            self.update_timelines()
        elif message == "SCENE_LENGTH_UPDATED":
            self.scene_view.set_scene_length(self.scene_model.scene_length)

        elif message == "CLIP_START_UPDATED":
             self.scene_view.set_clip_end(self.scene_model.get_selected_clip().clip_end)
             self.update_timelines()

        elif message == "CLIP_END_UPDATED":
             self.scene_view.set_clip_length(self.scene_model.get_selected_clip().clip_end)
             self.update_timelines()

        elif message == "CLIP_LENGTH_UPDATED":
            self.scene_view.set_clip_end(self.scene_model.get_selected_clip().clip_end)
            self.update_timelines()

        elif message == "CLIP_TYPE_UPDATED":
            self.update_timelines()


        elif message == "SELECTED_CLIP_RESIZED":
            self.scene_view.display_clip(self.scene_model.get_selected_clip())

        elif message == "STATIC_COLOR_UPDATED":
            self.update_timelines()

        elif message == "SCRUB_TIME_UPDATED":
            self.scene_view.update_lights(self.scene_model.lights, self.scene_model.scrub_time)
            self.scene_view.update_scrubber(self.scene_model.scrub_time)

        elif message == "CANVAS_REQUESTED":
            self.scene_model.canvas = self.scene_view.gui.display_window.canvas



    def update_timelines(self):
        self.scene_view.update_timelines(self.scene_model.get_selected_light())



