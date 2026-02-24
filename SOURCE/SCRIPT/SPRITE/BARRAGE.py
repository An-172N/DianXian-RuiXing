# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint
from math import degrees, atan2, radians, sin, cos


import pygame as pg


from PRELOAD import barrage_cache, effective, particle_cache
from LOGIC.CALCULATE import add
from LOGIC.SPRITE import Base


class Barrage(Base):
    __slots__ = ('effective', 'speed', 'color')

    def __init__(th, effective: pg.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, image: pg.Surface, group: pg.sprite.Group, mask: bool=True, rotate: bool=True):
        super().__init__(form, image, group, angle=angle, pos=pos, mask=mask, rotate=rotate)

        th.effective = effective
        th.speed = speed
        th.color = color

    def update(th) -> None:
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


class Text(Base):
    __slots__ = ('target_image', 'kill_time', 'speed', 'timer')

    def __init__(th, pos: tuple, kill_time: tuple, speed: float, image: pg.Surface, target_image: pg.Surface, group: pg.sprite.Group):
        super().__init__(None, image, group, pos=pos)

        th.target_image = target_image
        th.kill_time = kill_time
        th.speed = speed
        th.timer = 0

    def update(th):
        th.timer += 1
        th.y -= th.speed

        if th.timer >= th.kill_time[1]:
            th.kill()
        elif th.timer >= th.kill_time[0] and th.image != th.target_image:
            th.image = th.target_image


class Rect(Base):
    def __init__(th, image: pg.Surface, *group: pg.sprite.Group, pos: tuple=(0, 0), mask: bool=False):
        super().__init__(None, image, *group, pos=pos, mask=mask)


def circle_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group) -> None:
    two_point = add(locate, (-spawn_pos[0], -spawn_pos[1]))
    atan2_ = atan2(-two_point[0], -two_point[1])
    angle = degrees(atan2_)

    Barrage(effective, type, 3, color[0], angle, spawn_pos, barrage_cache[(type, color[0])], group, rotate=False)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group) -> None:
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        two_point = add((i, locate[1]), (-spawn_pos[0], -spawn_pos[1]))
        atan2_ = atan2(-two_point[0], -two_point[1])
        angle = degrees(atan2_)

        Barrage(effective, type, 3, color[0], angle, spawn_pos, barrage_cache[(type, color[0])], group)


def point_barrage(type: int, color: list, locate: tuple, group: pg.sprite.Group) -> None:
    for _ in range(3):
        pos = (randint(120, 465), randint(15, 225))
        two_point = add(locate, (-pos[0], -pos[1]))
        atan2_ = atan2(-two_point[0], -two_point[1])
        angle = degrees(atan2_)

        Barrage(effective, type, 4, color[0], angle, pos, barrage_cache[(type, color[0])], group, rotate=False)


def spawn_particles(group: pg.sprite.Group, size: tuple, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])

        Barrage(effective, None, randint(speed[0], speed[1]), color, i, pos, particle_cache[(size, color)], group, False, False)