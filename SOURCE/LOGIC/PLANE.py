# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def move_plane(variable: float, speed: tuple, forward: bool, backward: bool, change: bool) -> float:
    if forward:
        variable -= speed[1] if change else speed[0]
    if backward:
        variable += speed[1] if change else speed[0]

    return variable


def turn_side(original_image: pygame.Surface, turn_image: pygame.Surface, flip: bool, turn: bool) -> pygame.Surface:
    if flip:
        return pygame.transform.flip(turn_image, True, False)
    elif turn:
        return turn_image
    else:
        return original_image


def invinc(use_bomb: bool, collided: bool, visitable: bool, timer: int, end: int, interval: int, reset_char: object) -> tuple:
    if use_bomb or collided:
        timer += 1

        if timer >= end:
            if use_bomb:
                use_bomb = False
                timer = 0

                reset_char()

            collided = False
        else:
            visitable = (timer // interval) % 2
    else:
        timer = 0
        visitable = True

    return use_bomb, collided, visitable, timer


def vector(present: tuple, target: tuple, speed: float) -> tuple:
    dir = pygame.math.Vector2(target[0] - present[0], target[1] - present[1])
    current = pygame.math.Vector2(present[0], present[1])
    target = pygame.math.Vector2(target[0], target[1])

    delta_vec = target - current
    distance = delta_vec.length()

    if distance < speed:
        return target, delta_vec
    else:
        if distance > 0:
            dir.normalize_ip()

        return current + dir * speed, delta_vec


def single_bomb(use: bool, power: int, critical: int) -> tuple:
    if not use and power >= critical:
        return True, power - critical

    return use, power