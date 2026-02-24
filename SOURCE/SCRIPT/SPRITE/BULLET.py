# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint
from math import radians, sin, cos


import pygame as pg


from PRELOAD import bullet_cache, effective
from LOGIC.SPRITE import Base


class Bullet(Base):
    __slots__ = ('effective', 'speed', 'color', 'damage')

    def __init__(th, effective: pg.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, damage: int, image: pg.Surface, group: pg.sprite.Group, mask: bool=True, rotate: bool=True):
        super().__init__(form, image, group, angle=angle, pos=pos, mask=mask, rotate=rotate)

        th.effective = effective
        th.speed = speed
        th.color = color
        th.damage = damage

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


def circle_brick(group: pg.sprite.Group, spawn_pos: tuple):
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        Bullet(effective, "bullet", 16, 0, i, spawn_pos, 4, bullet_cache["bullet"], group, False).update()


def polygon_brick(group: pg.sprite.Group, *spawn_pos: tuple):
    bullet_index = [
        {
            'angle': choice([-30, -210]),
            'pos': spawn_pos[0]
        },
        {
            'angle': choice([30, 210]),
            'pos': spawn_pos[1]
        },
        {
            'angle': choice([90, 270]),
            'pos': spawn_pos[2]
        }
    ]

    for bullet_info in bullet_index:
        Bullet(effective, "bullet-cross", 16, 0, bullet_info['angle'], bullet_info['pos'], 4, bullet_cache["bullet-cross"], group, False)


def point_brick(group: pg.sprite.Group):
    for _ in range(24):
        pos = (randint(120, 465), randint(15, 345))
        angle = randint(0, 360)

        Bullet(effective, "bullet", 16, 0, angle, pos, 4, bullet_cache["bullet"], group, False)