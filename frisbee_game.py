import pygame
from frisbee_field import Frisbee_Field
from frisbee_player import Frisbee_Player
import sys
from pygame.locals import *

TEAM_1_COLOR = (255, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((468, 60))
    pygame.display.set_caption('Frisbee Sim')
    field = Frisbee_Field(5)

    player = Frisbee_Player((10, 10), TEAM_1_COLOR, 10)
    player_2 = Frisbee_Player((40, 10), TEAM_1_COLOR, 10)
    players = pygame.sprite.RenderPlain((player, player_2))
    players.draw(pygame.display.get_surface())
    player.update()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    return 0

if __name__ == '__main__':
    sys.exit(main())
