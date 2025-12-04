import argparse
import sys

sys.dont_write_bytecode = True

import pygame


pygame.display.init()
pygame.font.init()

pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain - Ver0.5.1')
pygame.display.set_icon(pygame.image.load('ASSET\IMG_ICON.png'))
screen = pygame.display.set_mode(
    (480, 360),
    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED,
    vsync=1
)
font = pygame.font.Font('ASSET\FNT\FNT_GNUUNIFONT.otf', 15)
clock = pygame.time.Clock()

import SCRIPT

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
SCRIPT.Variable.stage = args.stage
SCRIPT.Variable.level = args.level
SCRIPT.Variable.player = args.player
SCRIPT.Variable.s_power = args.s_power
game = SCRIPT.Game(screen, font, clock)

while True:
    game.update()
    clock.tick(60)