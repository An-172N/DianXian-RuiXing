import pygame as pyg

from LOGIC.TOOL import grav


class Item(pyg.sprite.Sprite):
    def __init__(th, clr, type, pos):
        super().__init__()
        th.clr = clr
        th.type = type

        th.image = th.square()
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def square(th):
        surface = pyg.Surface((9, 9), pyg.SRCALPHA)

        pyg.draw.rect(surface,
                      th.clr,
                      surface.get_rect(),
                      2)

        return surface
    
    def update(th):
        grav(th, 2)