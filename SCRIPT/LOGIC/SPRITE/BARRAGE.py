# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import random
import math

from SCRIPT import GLOBAL, LOGIC, FUNC


def circle_barrage(brick: LOGIC.Brick) -> None:
    char_pos = GLOBAL.main_char.rect.center

    sprite = LOGIC.Barrage(brick.type, 3, brick.color)
    sprite.rect.center = brick.rect.center
    sprite_pos = sprite.rect.center
    two_point = FUNC.add((char_pos[0], char_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
    atan2 = math.atan2(-two_point[0], -two_point[1])
    sprite.current_angle = math.degrees(atan2)
    sprite.update()

    GLOBAL.barrage_group.add(sprite)


def polygon_barrage(brick: LOGIC.Brick) -> None:
    char_pos = GLOBAL.main_char.rect.center
    
    for i in range(char_pos[0] - 32, char_pos[0] + 33, 64):
        sprite = LOGIC.Barrage(brick.type, 3, brick.color)
        sprite.rect.center = brick.rect.center
        sprite_pos = sprite.rect.center
        two_point = FUNC.add((i, char_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        sprite.current_angle = math.degrees(atan2)
        sprite.update()

        GLOBAL.barrage_group.add(sprite)


def line_barrage(_: None) -> None:
    char_pos = GLOBAL.main_char.rect.center
    start_pos = (random.randint(100, 480), 0)
    end_pos = (-char_pos[0], -char_pos[1])

    delta_pos = FUNC.add(end_pos, start_pos)
    distance = math.hypot(delta_pos[0], delta_pos[1])
                
    sprite = LOGIC.Line((3, distance), 0, 0, (255, 255, 255))
    sprite.rect.center = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
    atan2 = math.atan2(-delta_pos[0], -delta_pos[1])
    sprite.current_angle = math.degrees(atan2)
    sprite.update()
    
    GLOBAL.barrage_group.add(sprite)


def point_barrage(brick: LOGIC.Brick) -> None:
    char_pos = GLOBAL.main_char.rect.center

    for _ in range(3):
        sprite = LOGIC.Barrage(brick.type, 4, brick.color)
        sprite.rect.center = (random.randint(120, 465), random.randint(15, 225))
        sprite_pos = sprite.rect.center
        two_point = FUNC.add((char_pos[0], char_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        sprite.current_angle = math.degrees(atan2)
        sprite.update()

        GLOBAL.barrage_group.add(sprite)


def spawn_barrage(brick: LOGIC.Brick) -> None:
    if random.random() <= 0.17 + GLOBAL.fibonacci_list[GLOBAL.stage - 1]:
        barrage_dict = {
            1: circle_barrage,
            2: polygon_barrage,
            3: line_barrage,
            4: point_barrage
        }
        
        barrage_dict[GLOBAL.stage](brick)