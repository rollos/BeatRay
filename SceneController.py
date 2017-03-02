from Utils import *
from SceneModel import *
from SceneView import *

class SceneController():
    def __init__(self, SceneModel: SceneModel, SceneView: SceneView):
        self.scene_model = SceneModel
        self.scene_view = SceneView

        self.scene_model.register_observer(self)

        self.scene_view.register_observer(self)

    def update(self, event_type, message):

        #If we get an update from the model, update the view
        if event_type == MODELUPDATE:
            print("MODELUPDATE:{}".format(message))
            self.update_view(message)

        #If we get an update from the view, update the model
        elif event_type == VIEWUPDATE:
            print("VIEWUPDATE:{}".format(message))
            self.update_model(message)

    #When the view is updated, update the model
    def update_model(self, message):
        if message == "BPM_UPDATE":
            self.scene_model.set_BPM(self.scene_view.get_bpm())
        elif message == "SCENELENGTH_UPDATE":
            self.scene_model.set_scene_length(self.scene_view.get_scene_length())
        elif message == "PLAY_PRESSED":
            self.scene_model.switch_play_state()
        elif message == "STOP_PRESSED":
            self.scene_model.stop_pressed()
        elif message == "NEW_SCENE":
            self.scene_model.new_scene()
        elif message == "LOAD_SCENE":
            self.scene_model.load_scene()
        elif message == "SAVE_SCENE":
            self.scene_model.save_scene()
        elif message == "NEW_LIGHT":
            self.scene_model.new_light()
        elif message == "NEW_MOVEMENT_CLIP":
            self.scene_model.new_movement_clip()
        elif message == "NEW_COLOR_CLIP":
            self.scene_model.new_color_clip()



    # When the model is updated, update the view
    def update_view(self, message):
        if message == "PLAY_STATE_UPDATE":
            self.scene_view.update_play_button_state(self.scene_model.play_state)



    def play_pressed(self):
        self.scene_model.switch_play_state()
