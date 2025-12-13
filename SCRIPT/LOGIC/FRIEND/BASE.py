import math

import pygame as pyg

import FUNC
import SCRIPT.DICT as DICT

from SCRIPT.DRAW import ShapeDraw


class Base(pyg.sprite.Sprite):
    POLYGON = 0
    RECT = 1
    CIRCLE = 2
    LINE = 3

    def __init__(th, value, color, shape, type=0):
        super().__init__()
        th.width = value[0]
        th.height = value[1]
        th.border = value[2]
        th.color = color
        th.type = type
        th.shape = shape

        th.base_draw = ShapeDraw(th.width, th.height, th.border, th.color)

        th.current_angle = 0
        th.speed = 0
        th.timer = 0

        th.is_rotated = False

        th.original_image = th.get_shape(shape)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pyg.mask.from_surface(th.image)

    def get_shape(th, shape) -> None:
        shape_dict = {
            th.POLYGON: th.base_draw.polygon,
            th.RECT: th.base_draw.rect,
            th.CIRCLE: th.base_draw.circle,
        }

        return shape_dict[shape]()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pyg.transform.rotate(th.original_image, th.current_angle)
            th.mask = pyg.mask.from_surface(th.image)
            th.is_rotated = True
        th.rect = th.image.get_rect(center=th.rect.center)

        th.x = getattr(th, 'x', th.rect.centerx)
        th.y = getattr(th, 'y', th.rect.centery)
        rad = math.radians(th.current_angle)
        th.x, th.y, _ = FUNC.Calculate.delta_tuple((th.x, th.y, 0), (math.sin(rad) * th.speed, math.cos(rad) * th.speed, 0))
        th.rect.center = (th.x, th.y)

        if th.shape == 1 and th.height > 16:
            th.timer += 1

            if th.timer >= 80:
                th.kill()
            elif th.timer >= 40 and th.color != DICT.color_dict[3]:
                th.color = DICT.color_dict[3]

                th.image.fill(th.color, special_flags=pyg.BLEND_RGBA_MULT)