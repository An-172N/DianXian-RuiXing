# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import itertools


def spawn_bullet(power: int, counter: int, fire: object) -> int:
    p = 2 ** (power // 32)
    q = 2 ** (power // 16)
    
    for i, j in itertools.product(range(0, p), range(-q, q + 1, q)):
        fire(0 + i * 10, 0 + i * 12, j)

    counter -= 1

    return counter


def single_bomb(condition: bool, power: int) -> tuple:
    if not condition and power >= 12:
        power -= 12
        condition = True

    return condition, power


def bullet_collide(hp: int, damage: int, score: int) -> tuple:
    hp -= damage
    score += 64

    return hp, score