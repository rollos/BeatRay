import pygame, sys



BACKGROUND_COLOR = (0,0,0)

class Display:
    def __init__(self, width=640, height=480, fullscreen = False):
        pygame.init()
    #    print("W:{} H:{}".format(screen_width, screen_height))
        self.bg_color = BACKGROUND_COLOR
        self.width=width
        self.height=height
        self.screen = pygame.display.set_mode((640, 480))
        if(fullscreen):
            pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen.fill(BACKGROUND_COLOR)

       # self.main_menu()

    def getBackgroundColor(self):
        return BACKGROUND_COLOR

    def clear(self):
        self.screen.fill(self.bg_color)

    def main_menu(self):
       # print("Main Menu")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 113:
                    pygame.quit()
                    sys.exit()

    #Get the center of the current display
    def get_center(self):
        return (self.width/2, self.height/2)


if __name__ == "__main__":
    display = Display(400,400,True)
