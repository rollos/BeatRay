
class LightFrameModel():
    def __init__(self, radius, type:str,  position = None, color = None ):

        self.position = position
        self.color = color
        self.radius = radius
        self.light_type = type

