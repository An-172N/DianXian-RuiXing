# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def move_plane(pos: tuple, speed: tuple, swing: tuple, left: bool, right: bool, variable: bool) -> tuple:
    x, y = pos

    if left:
        x -= speed[1] if variable else speed[0]
    if right:
        x += speed[1] if variable else speed[0]

    y = swing[0] if variable else swing[1]

    return x, y


def keep_position(left: float, right: float, pos: float) -> tuple:
    x = pos[0]

    if x < left:
        x = left
    elif x > right:
        x = right

    return x, pos[1]


def turn_side(original_image: pygame.Surface, turn_image: pygame.Surface, flip: bool, turn: bool) -> pygame.Surface:
    turn_image = turn_image
    flip_image = pygame.transform.flip(turn_image, True, False)

    if flip:
        return flip_image
    elif turn:
        return turn_image
    else:
        return original_image


def invinc(use_bomb: bool, collided: bool, visitable: bool, timer: int, end: int, interval: int, reset: object) -> tuple:
    if use_bomb or collided:
        timer += 1

        if timer >= end:
            if use_bomb:
                use_bomb = False
                timer = 0

                reset()

            collided = False
        else:
            visitable = (timer // interval) % 2
    else:
        timer = 0
        visitable = True

    return use_bomb, collided, visitable, timer


def single_bomb(use: bool, power: int, critical: int) -> tuple:
    if not use and power >= critical:
        power -= critical
        use = True

    return use, power