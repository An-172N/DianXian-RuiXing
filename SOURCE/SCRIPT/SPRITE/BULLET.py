# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice
from math import radians, sin, cos


import pygame


from PRELOAD import bullet_cache, effective
from LOGIC.SPRITE import Base


class Bullet(Base):
    __slots__ = ('effective', 'speed', 'color', 'damage')

    def __init__(th, effective: pygame.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, damage: int, image: pygame.Surface, mask: bool=True, rotate: bool=True):
        super().__init__(form, image, angle, pos, mask, rotate)

        th.effective = effective
        th.speed = speed
        th.color = color
        th.damage = damage

    def update(th) -> None:
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


def circle_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        sprite = Bullet(effective, "bullet", 16, 0, i, spawn_pos, 4, bullet_cache["bullet"], False)

        sprite.update()
        group.add(sprite)


def polygon_brick(group: pygame.sprite.Group, *spawn_pos: tuple) -> None:
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
        sprite = Bullet(effective, "bullet-cross", 16, 0, bullet_info['angle'], bullet_info['pos'], 4, bullet_cache["bullet-cross"], False)

        sprite.update()
        group.add(sprite)


def point_brick(group: pygame.sprite.Group) -> None:
    for _ in range(24):
        sprite_pos = (randint(120, 465), randint(15, 345))
        current_angle = randint(0, 360)
        sprite = Bullet(effective, "bullet", 16, 0, current_angle, sprite_pos, 4, bullet_cache["bullet"], False)

        sprite.update()
        group.add(sprite)