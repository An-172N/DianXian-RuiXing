import itertools

import SCRIPT.VARIABLE as VARIABLE


def spawn_bullet() -> None:
    p = 2 ** (VARIABLE.s_power // 32)
    q = 2 ** (VARIABLE.s_power // 16)

    for i, j in itertools.product(
        range(0, p),
        range(-q, q + 1, q)
    ):
        VARIABLE.main_char.bomb.fire(
            0 + i * 10,
            0 + i * 12,
            j
        )

    VARIABLE.shoot_counter -= 1


def single_bomb() -> None:
    if (
        not VARIABLE.is_s_divide
        and VARIABLE.s_power >= 12
    ):
        VARIABLE.s_power -= 12
        VARIABLE.is_s_divide = True


def bullet_collide(source, target) -> None:
    target.hp -= source.damage
    VARIABLE.score += 64