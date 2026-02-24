# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame


def combo_counter(timer: int, combo: int, score: int, bonus: int, end: int) -> tuple:
    timer -= 1

    if timer <= 0:
        if combo > 0:
            score += bonus

        combo = 0
        timer = end

    return timer, combo, score


def item_spawn(group: pygame.sprite.Group, condition: bool, char: object, *args: tuple, timer: int=0) -> int:
    timer += 1

    if condition:
        group.add(char(*args))

        timer = 0

    return timer