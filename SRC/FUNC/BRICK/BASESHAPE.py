import math

import pygame as pyg

from ..LOGIC import MOVE


class BaseShape(pyg.sprite.Sprite):
    def __init__(th, wh, bd, clr, shape, type=0, pos1=(0, 0), pos2=(0, 0)):
        super().__init__()
        th.wid = wh[0]
        th.hei = wh[1]
        th.bd = bd
        th.clr = clr
        th.shape = shape
        th.type = type
        th.start_pos = pos1
        th.end_pos = pos2

        th.curr_ang = 0
        th.spd = 0

        th.image = th.get_shape(shape)
        th.rect = th.image.get_rect()

    def get_shape(th, shape):
        shape_dict = {
            0: th.polygon,
            1: th.square,
            2: th.circle,
            3: th.circle,
            4: th.line
        }

        return shape_dict[shape]()

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
    
    def line(th):
        x_min = min(th.start_pos[0], th.end_pos[0])
        y_min = min(th.start_pos[1], th.end_pos[1])
        x_max = max(th.start_pos[0], th.end_pos[0])
        y_max = max(th.start_pos[1], th.end_pos[1])

        surface = pyg.Surface((x_max - x_min + th.bd, y_max - y_min + th.bd), pyg.SRCALPHA)

        start = (th.start_pos[0] - x_min, th.start_pos[1] - y_min)
        end = (th.end_pos[0] - x_min, th.end_pos[1] - y_min)
        pyg.draw.line(surface, th.clr, start, end, th.bd)
  
        return surface
    
    def update(th):
        MOVE.rot(th)
        MOVE.mv(th, th.spd)