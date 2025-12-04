import math

import pygame as pyg

import FUNC
import SCRIPT.DICT

from SCRIPT.DRAW import ShapeDraw


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
        th.ctr = 0

        th.orig_image = th.get_shape(shape)
        th.image = th.orig_image
        th.rect = th.image.get_rect()
        th.mask = pyg.mask.from_surface(th.image)

    def get_shape(th, shape) -> None:
        shape_dict = {
            th.POLYGON: lambda: th.base_draw.polygon(),
            th.RECT: lambda: th.base_draw.rect(),
            th.CIRCLE: lambda: th.base_draw.circle(),
        }

        return shape_dict[shape]()
    
    def update(th) -> None:
        th.image = pyg.transform.rotate(th.orig_image, th.curr_ang)
        th.rect = th.image.get_rect(center=th.rect.center)
        th.mask = pyg.mask.from_surface(th.image)

        th.x = getattr(th, 'x', th.rect.centerx)
        th.y = getattr(th, 'y', th.rect.centery)
        rad = math.radians(th.curr_ang)
        th.x, th.y, _ = FUNC.Calculate.delta_tuple((th.x, th.y, 0), (math.sin(rad) * th.spd, math.cos(rad) * th.spd, 0))
        th.rect.center = (int(th.x), int(th.y))

        if th.shape == 1 and th.hei > 16:
            th.ctr += 1

            if th.ctr >= 40:
                th.clr = SCRIPT.DICT.clr_dict[3]
                temp_surface = pyg.Surface(th.image.get_size(), pyg.SRCALPHA)
                temp_surface.fill(th.clr)

                th.image.blit(temp_surface, (0, 0), special_flags=pyg.BLEND_RGBA_MIN)
            if th.ctr >= 80:
                th.kill()