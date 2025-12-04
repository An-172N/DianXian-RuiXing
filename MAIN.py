import argparse
import sys
import os

sys.dont_write_bytecode = True

import pygame


pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode(
    (480, 360),
    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED,
    vsync=1
)

import SCRIPT
import VARIABLE

pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain - Ver0.5')
pygame.display.set_icon(pygame.image.load(os.path.join(VARIABLE.asset_path, 'IMG_ICON.png')))

font = pygame.font.Font(os.path.join(VARIABLE.asset_path, 'FNT\FNT_GNUUNIFONT.otf'), 15)
clock = pygame.time.Clock()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--stage',
    type=int,
    default=1
)
parser.add_argument(
    '--level',
    type=int,
    default=0
)
parser.add_argument(
    '--player',
    type=int,
    default=4
)
parser.add_argument(
    '--s_power',
    type=int,
    default=0
)
args = parser.parse_args()
VARIABLE.stage = args.stage
VARIABLE.level = args.level
VARIABLE.player = args.player
VARIABLE.s_power = args.s_power
game = SCRIPT.Game(screen, font, clock)

while True:
    game.update()
    clock.tick(60)