import sgc
from sgc.locals import *
import pygame, sys, math

from pygame.locals import *


def helloworld():
    print("Hello World!")

pygame.display.init()
pygame.font.init()

screen = sgc.surface.Screen((640,480))

clock = pygame.time.Clock()

b = sgc.Combo(label="Movement Type", pos=(100,100), values=("Option1", "Option2", "Option3", "Default"), fade=False)
b.on_click = helloworld
b.add(0)


# event control -- NEEDS WORK?
while True:
    time = clock.tick(30)

    for event in pygame.event.get():
        sgc.event(event)
        if event.type == GUI:
            print(event)
        if event.type == QUIT:
            exit()

    screen.fill((0,0,0))
    sgc.update(time)
    pygame.display.flip()



