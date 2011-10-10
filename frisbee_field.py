import pygame
from pygame.locals import *
import sys

FIELD_COLOR  = (0, 255, 0)
LINE_COLOR = (255, 255, 255)

class Frisbee_Field(pygame.Surface):
    def  __init__(self, FIELD_SCALAR=1.0):
        pygame.Surface.__init__(self)
        self.field_width = int(37 * FIELD_SCALAR)
        self.field_length = int(120 * FIELD_SCALAR)
        windowSurface = pygame.display.set_mode((self.field_width, 
                                                  self.field_length), 
                                                0, 32)
        windowSurface.fill(FIELD_COLOR)
        
        end_zone_offset = int(23 * FIELD_SCALAR)
        pygame.draw.line(windowSurface, 
                 LINE_COLOR, 
                 (0, end_zone_offset),
                 (self.field_width, end_zone_offset), 
                 4)
        pygame.draw.line(windowSurface, 
                 LINE_COLOR, 
                 (0, self.field_length - end_zone_offset),
                 (self.field_width, self.field_length - end_zone_offset),
                 4)

        pygame.display.update()

    def render(self, surface):
        pass

if __name__ == '__main__':
    field = Frisbee_Field(5)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
