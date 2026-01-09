# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import itertools

import SCRIPT.GLOBAL as GLOBAL


def spawn_bullet() -> None:
    p = 2 ** (GLOBAL.s_power // 32)
    q = 2 ** (GLOBAL.s_power // 16)

    for i, j in itertools.product(range(0, p), range(-q, q + 1, q)):
        GLOBAL.main_char.fire(0 + i * 10, 0 + i * 12, j)

    GLOBAL.shoot_counter -= 1


def single_bomb() -> None:
    if not GLOBAL.is_s_divide and GLOBAL.s_power >= 12:
        GLOBAL.s_power -= 12
        GLOBAL.is_s_divide = True


def bullet_collide(source, target) -> None:
    target.hp -= source.damage
    GLOBAL.score += 64