import pygame
class Light:

    def __init__(self, display, color, location,ID=None):
        self.screen = display
        self.color = color
        self.location = location
        self.ID = ID

    #Draw the light onto the screen
    def draw(self):
        pass #must override in subclass


    #Moves the light to a position on the screen
    #Draws the object so we can contain it in one Task()
    def move(self,dest):
        self.location = dest

    def set_color(self, color):
        self.color = color

class Circle(Light):

    def __init__(self, screen, color, location, radius, thickness=0):
        super().__init__(screen,color,location)
        self.radius = radius
        self.thickness = thickness

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.location, self.radius, self.thickness)







