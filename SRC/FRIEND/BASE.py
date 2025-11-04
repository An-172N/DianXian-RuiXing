import math

import pygame as pyg

from FUNC import Calculate
import DRAW


class Base(pyg.sprite.Sprite):
    POLYGON = 0
    RECT = 1
    CIRCLE = 2
    LINE = 3

    def __init__(th, val, clr, shape, type=0, start=(0, 0), end=(0, 0)):
        super().__init__()
        th.wid = val[0]
        th.hei = val[1]
        th.bd = val[2]
        th.clr = clr
        th.type = type
        th.shape = shape
        th.start_pos = start
        th.end_pos = end

        th.curr_ang = 0
        th.spd = 0

        th.orig_image = th.get_shape(shape)
        th.image = th.orig_image
        th.rect = th.image.get_rect()

    def get_shape(th, shape):
        shape_dict = {
            th.POLYGON: lambda: DRAW.polygon(th.wid, th.hei, th.bd, th.clr),
            th.RECT: lambda: DRAW.rect(th.wid, th.hei, th.bd, th.clr),
            th.CIRCLE: lambda: DRAW.circle(th.wid, th.hei, th.bd, th.clr),
            th.LINE: lambda: DRAW.line(th.start_pos, th.end_pos, th.bd, th.clr)
        }

        return shape_dict[shape]()
    
    def update(th):
        th.image = pyg.transform.rotate(th.orig_image, th.curr_ang)
        th.rect = th.image.get_rect(center=th.rect.center)

        th.x = getattr(th, 'x', th.rect.centerx)
        th.y = getattr(th, 'y', th.rect.centery)
        rad = math.radians(th.curr_ang)
        th.x, th.y = Calculate.coordinate_difference((th.x, th.y), (math.sin(rad) * th.spd, math.cos(rad) * th.spd))
        th.rect.center = (int(th.x), int(th.y))