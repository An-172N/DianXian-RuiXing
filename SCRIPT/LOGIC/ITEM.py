# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

from SCRIPT import SPRITE, FUNC


def combo_counter(timer: int, combo: int, score: int) -> tuple:
    timer -= 1

    if timer <= 0:
        if combo > 0:
            score += 2 ** combo

        combo = 0
        timer = 120

    return timer, combo, score


def item_collide(timer: int, fire: int, variable1: int, variable2: int, type: str, combo: int) -> tuple:
    timer = 120
    fire = int(FUNC.clamp(fire + 1, 0, 6))

    if type == "power":
        variable1 = int(FUNC.clamp(variable1 + 1, 0, 32))
        combo += 1
    elif type == "flash":
        variable2 += 1
        combo += 1

    return timer, fire, combo, variable1, variable2


def item_spawn(group: pygame.sprite.Group, condition: bool, pos: tuple, speed: float, color: tuple, type: str, timer: int=0) -> None:
    timer += 1

    if condition:
        sprite = SPRITE.Item(type, speed, color, pos)

        group.add(sprite)

        timer = 0

    return timer