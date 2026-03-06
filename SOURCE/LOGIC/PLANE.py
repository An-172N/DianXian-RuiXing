# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any


import pygame


def move(
    variable: int | float,
    speed: tuple[int | float, int | float],
    forward: bool,
    backward: bool,
    change: bool
) -> float:
    if forward:
        variable -= speed[1] if change else speed[0]
    if backward:
        variable += speed[1] if change else speed[0]

    return variable


def turn_side(
    original_image: pygame.Surface,
    turn_image: pygame.Surface,
    flip: bool,
    turn: bool
) -> pygame.Surface:
    if flip:
        return pygame.transform.flip(turn_image, True, False)
    elif turn:
        return turn_image
    else:
        return original_image


def invinc(
    bombed: bool,
    collided: bool,
    visitable: bool,
    timer: int,
    end: int,
    interval: int,
    reset: Callable[..., Any],
    *args: Any
) -> tuple[bool, bool, bool, int]:
    if bombed or collided:
        timer += 1

        if timer >= end:
            if bombed:
                bombed = False
                timer = 0

                reset(*args)

            collided = False
        else:
            visitable = (timer // interval) % 2
    else:
        timer = 0
        visitable = True

    return bombed, collided, visitable, timer


def single_bomb(
    condition: bool,
    power: int,
    critical: int
) -> tuple[bool, int]:
    if not condition and power >= critical:
        condition = True
        power -= critical

    return condition, power


def count_combo(
    timer: int,
    combo: int,
    score: int,
    bonus: int,
    end: int
) -> tuple[int, int, int]:
    timer -= 1

    if timer <= 0:
        if combo > 0:
            score += bonus

        combo = 0
        timer = end

    return timer, combo, score