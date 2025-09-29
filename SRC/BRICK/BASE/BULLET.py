import pygame as pyg

from LOGIC.TOOL import mv
from LOGIC.TOOL import rot


class KliBullet(pyg.sprite.Sprite):
    def __init__(th, wid, hei, type):
        super().__init__()
        th.wid = wid
        th.hei = hei
        th.type = type

        th.curr_ang = 0
        th.dmg = 4 if th.type == "blt" else 6
        th.spd = 16 if th.type == "blt" else -24

        th.image = th.square()
        th.rect = th.image.get_rect()

    def square(th):
        surface = pyg.Surface((th.wid, th.hei), pyg.SRCALPHA)

        pyg.draw.rect(surface,
                      (45, 194, 229),
                      surface.get_rect(),
                      0)

        return surface
    
    def update(th):
        if th.type == "blt":
            rot(th)

        mv(th, th.spd)