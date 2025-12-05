import sys

import pygame


sys.dont_write_bytecode = True
pygame.display.init()
pygame.font.init()

pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')
screen = pygame.display.set_mode(
    (480, 360),
    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED,
    vsync=1
)

import SCRIPT
game = SCRIPT.Game(screen)
game.update()