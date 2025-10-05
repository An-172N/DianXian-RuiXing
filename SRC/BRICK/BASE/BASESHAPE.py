import pygame as pyg
import math

import TOOL


class BaseShape(pyg.sprite.Sprite):
    def __init__(th, wid, hei, bd, clr, shape, type=0):
        super().__init__()
        th.wid = wid
        th.hei = hei
        th.bd = bd
        th.clr = clr
        th.shape = shape
        th.type = type

        th.curr_ang = 0
        th.spd = 0

        th.image = th.get_shape(shape)
        th.rect = th.image.get_rect()

    def get_shape(th, shape):
        if shape == 0:
            return th.polygon()
        elif shape == 1:
            return th.square()
        else:
            return th.circle()

    def polygon(th):
        surface = pyg.Surface((th.wid, th.hei), pyg.SRCALPHA)

        side_length = min(th.wid, th.hei)
        hei_polygon = math.sqrt(3) / 2 * side_length
        center_x = th.wid // 2
        center_y = th.hei // 2
        pt1 = (center_x, center_y - hei_polygon / 2)
        pt2 = (center_x - side_length / 2, center_y + hei_polygon / 2)
        pt3 = (center_x + side_length / 2, center_y + hei_polygon / 2)
        polygon_pts = [pt1, pt2, pt3]

        pyg.draw.polygon(surface,
                         th.clr,
                         polygon_pts,
                         th.bd)

        return surface

    def square(th):
        surface = pyg.Surface((th.wid, th.hei), pyg.SRCALPHA)

        pyg.draw.rect(surface,
                      th.clr,
                      surface.get_rect(),
                      th.bd)

        return surface

    def circle(th):
        surface = pyg.Surface((th.wid, th.hei), pyg.SRCALPHA)

        center_x = th.wid // 2
        center_y = th.hei // 2
        radius = min(th.wid, th.hei) // 2

        pyg.draw.circle(surface,
                        th.clr,
                        (center_x, center_y),
                        radius,
                        th.bd)

        return surface
    
    def update(th):
        TOOL.rot(th)
        TOOL.mv(th, th.spd)