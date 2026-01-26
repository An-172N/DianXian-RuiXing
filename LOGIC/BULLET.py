# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


def single_bomb(condition: bool, power: int, critical: int) -> tuple:
    if not condition and power >= critical:
        power -= critical
        condition = True

    return condition, power


def bullet_collide(hp: int, damage: int, score: int, add_score: int) -> tuple:
    hp -= damage
    score += add_score

    return hp, score