# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def move_plane(pos: tuple, speed: tuple, up_down: tuple, move_right_condition: bool, move_left_condition: bool, speed_condition: bool) -> tuple:
    x, y = pos
    
    if move_right_condition:
        x += speed[1] if speed_condition else speed[0]
    if move_left_condition:
        x -= speed[1] if speed_condition else speed[0]

    y = up_down[0] if speed_condition else up_down[1]
    
    return x, y


def keep_position(range_left: float, range_right: float, char_pos: float) -> tuple:
    x = char_pos[0]

    if x < range_left:
        x = range_left
    elif x > range_right:
        x = range_right

    return x, char_pos[1]


def turn_side(original_image: pygame.Surface, turn_side_image: pygame.Surface, flip_condition: bool, turn_side_condition: bool) -> pygame.Surface:
    turn_side_image = turn_side_image
    flipped_image = pygame.transform.flip(turn_side_image, True, False)

    if flip_condition:
        return flipped_image
    elif turn_side_condition:
        return turn_side_image
    else:
        return original_image


def invinc(condition1: bool, condition2: bool, is_visitable: bool, timer: int, end: int, interval: int, reset_bullet: object) -> tuple:
    if condition1 or condition2:
        timer += 1

        if timer >= end:
            if condition1:
                condition1 = False
                timer = 0

                reset_bullet()

            condition2 = False
        else:
            is_visitable = (timer // interval) % 2
    else:
        timer = 0
        is_visitable = True

    return condition1, condition2, is_visitable, timer


def single_bomb(condition: bool, power: int, critical: int) -> tuple:
    if not condition and power >= critical:
        power -= critical
        condition = True

    return condition, power