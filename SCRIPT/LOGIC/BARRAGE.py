# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from SCRIPT import SPRITE, FUNC


def circle_barrage(type: int, color: tuple, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    two_point = FUNC.add((target_pos[0], target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
    atan2 = math.atan2(-two_point[0], -two_point[1])
    current_angle = math.degrees(atan2)

    sprite = SPRITE.Barrage(type, 3, color, current_angle, spawn_pos)
    sprite.update()

    group.add(sprite)


def polygon_barrage(type: int, color: tuple, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    for i in range(target_pos[0] - 32, target_pos[0] + 33, 64):
        two_point = FUNC.add((i, target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        current_angle = math.degrees(atan2)
        
        sprite = SPRITE.Barrage(type, 3, color, current_angle, spawn_pos)
        sprite.update()

        group.add(sprite)


def line_barrage(target_pos: tuple, group: pygame.sprite.Group) -> None:
    start_pos = (random.randint(100, 480), 0)
    end_pos = (-target_pos[0], -target_pos[1])

    delta_pos = FUNC.add(end_pos, start_pos)
    distance = math.hypot(delta_pos[0], delta_pos[1])

    sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
    atan2 = math.atan2(-delta_pos[0], -delta_pos[1])
    current_angle = math.degrees(atan2)
                
    sprite = SPRITE.Line((3, distance), 0, 0, current_angle, sprite_pos, (255, 255, 255), (128, 0, 128))
    sprite.update()
    
    group.add(sprite)


def point_barrage(type: int, color: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    for _ in range(3):
        sprite_pos = (random.randint(120, 465), random.randint(15, 225))
        two_point = FUNC.add((target_pos[0], target_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        current_angle = math.degrees(atan2)

        sprite = SPRITE.Barrage(type, 4, color, current_angle, sprite_pos)
        sprite.update()

        group.add(sprite)


def spawn_barrage(stage: int, group: pygame.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, target_pos: tuple) -> None:
    if random.random() <= 0.17 + fib[stage - 1]:
        barrage_dict = {
            1: circle_barrage,
            2: polygon_barrage,
            3: line_barrage,
            4: point_barrage
        }

        if stage in [1, 2]:
            return barrage_dict.get(stage)(type, color, spawn_pos, target_pos, group)
        elif stage == 3:
            return barrage_dict.get(stage)(target_pos, group)
        else:
            return barrage_dict.get(stage)(type, color, target_pos, group)