import math

import pygame as pyg

import FUNC
from DRAW import ShapeDraw


class Base(pyg.sprite.Sprite):
    POLYGON = 0
    RECT = 1
    CIRCLE = 2
    LINE = 3

    def __init__(th, val, clr, shape, type=0):
        super().__init__()
        th.wid = val[0]
        th.hei = val[1]
        th.bd = val[2]
        th.clr = clr
        th.type = type
        th.shape = shape

        th.base_draw = ShapeDraw(th.wid, th.hei, th.bd, th.clr)

        th.curr_ang = 0
        th.spd = 0

        th.orig_image = th.get_shape(shape)
        th.image = th.orig_image
        th.rect = th.image.get_rect()

    def get_shape(th, shape):
        shape_dict = {
            th.POLYGON: lambda: th.base_draw.polygon(),
            th.RECT: lambda: th.base_draw.rect(),
            th.CIRCLE: lambda: th.base_draw.circle(),
        }

        return shape_dict[shape]()
    
    def update(th):
        th.image = pyg.transform.rotate(th.orig_image, th.curr_ang)
        th.rect = th.image.get_rect(center=th.rect.center)

        th.x = getattr(th, 'x', th.rect.centerx)
        th.y = getattr(th, 'y', th.rect.centery)
        rad = math.radians(th.curr_ang)
        th.x, th.y = FUNC.Calculate.delta_position((th.x, th.y), (math.sin(rad) * th.spd, math.cos(rad) * th.spd))
        th.rect.center = (int(th.x), int(th.y))