# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint
from math import degrees, atan2, radians, sin, cos


import pygame


from PRELOAD import barrage_cache, effective
from LOGIC.CALCULATE import add
from LOGIC.SPRITE import Base


class Barrage(Base):
    __slots__ = ('effective', 'speed', 'color')

    def __init__(th, effective: pygame.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, image: pygame.Surface, mask: bool=True, rotate: bool=True):
        super().__init__(form, image, angle, pos, mask, rotate)

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

    def __init__(th, pos: tuple, kill_time: tuple, speed: float, image: pygame.Surface, target_image: pygame.Surface):
        super().__init__(None, image, pos=pos)
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
    def __init__(th, image: pygame.Surface, pos: tuple=(0, 0), mask: bool=False):
        super().__init__(None, image, pos=pos, mask=mask)


def circle_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pygame.sprite.Group) -> None:
    two_point = add(locate, (-spawn_pos[0], -spawn_pos[1]))
    atan2_ = atan2(-two_point[0], -two_point[1])
    current_angle = degrees(atan2_)
    sprite = Barrage(effective, type, 3, color[0], current_angle, spawn_pos, barrage_cache[f"{type}_{color[0]}"], rotate=False)

    group.add(sprite)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pygame.sprite.Group) -> None:
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        two_point = add((i, locate[1]), (-spawn_pos[0], -spawn_pos[1]))
        atan2_ = atan2(-two_point[0], -two_point[1])
        current_angle = degrees(atan2_)
        sprite = Barrage(effective, type, 3, color[0], current_angle, spawn_pos, barrage_cache[f"{type}_{color[0]}"])

        sprite.update()
        group.add(sprite)


def point_barrage(type: int, color: list, locate: tuple, group: pygame.sprite.Group) -> None:
    for _ in range(3):
        sprite_pos = (randint(120, 465), randint(15, 225))
        two_point = add(locate, (-sprite_pos[0], -sprite_pos[1]))
        atan2_ = atan2(-two_point[0], -two_point[1])
        current_angle = degrees(atan2_)
        sprite = Barrage(effective, type, 4, color[0], current_angle, sprite_pos, barrage_cache[f"{type}_{color[0]}"], rotate=False)

        group.add(sprite)