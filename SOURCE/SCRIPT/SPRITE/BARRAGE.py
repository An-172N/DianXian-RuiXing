# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint
from math import degrees, atan2


import pygame


from PRELOAD import barrage_cache, effective
from LOGIC.TOOL import add
from LOGIC.SPRITE import Barrage


def circle_barrage(type: int, color: list, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    two_point = add((target_pos[0], target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
    atan2_ = atan2(-two_point[0], -two_point[1])
    current_angle = degrees(atan2_)
    sprite = Barrage(effective, type, 3, color[0], current_angle, spawn_pos, barrage_cache[f"{type}_{color[0]}"], rotate=False)

    group.add(sprite)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    for i in range(target_pos[0] - 32, target_pos[0] + 33, 64):
        two_point = add((i, target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
        atan2_ = atan2(-two_point[0], -two_point[1])
        current_angle = degrees(atan2_)
        sprite = Barrage(effective, type, 3, color[0], current_angle, spawn_pos, barrage_cache[f"{type}_{color[0]}"])

        sprite.update()
        group.add(sprite)


def point_barrage(type: int, color: list, target_pos: tuple, group: pygame.sprite.Group) -> None:
    for _ in range(3):
        sprite_pos = (randint(120, 465), randint(15, 225))
        two_point = add((target_pos[0], target_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
        atan2_ = atan2(-two_point[0], -two_point[1])
        current_angle = degrees(atan2_)
        sprite = Barrage(effective, type, 4, color[0], current_angle, sprite_pos, barrage_cache[f"{type}_{color[0]}"], rotate=False)

        group.add(sprite)