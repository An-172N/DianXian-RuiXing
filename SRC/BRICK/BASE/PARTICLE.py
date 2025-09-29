import pygame as pyg

from LOGIC.TOOL import mv


class Particle(pyg.sprite.Sprite):
    def __init__(th, wid, clr):
        super().__init__()
        th.wid = wid
        th.clr = clr

        th.curr_ang = 0
        th.spd = 0

        th.image = th.square()
        th.rect = th.image.get_rect()

    def square(th):
        surface = pyg.Surface((th.wid, th.wid), pyg.SRCALPHA)

        pyg.draw.rect(surface,
                      th.clr,
                      surface.get_rect(),
                      0)

        return surface
    
    def update(th):
        mv(th, th.spd)