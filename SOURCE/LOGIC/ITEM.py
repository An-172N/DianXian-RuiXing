# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


def combo_counter(timer: int, combo: int, score: int, add_score: int, end: int) -> tuple:
    timer -= 1

    if timer <= 0:
        if combo > 0:
            score += add_score

        combo = 0
        timer = end

    return timer, combo, score


def calculate_item_rate(game_power: int, condition: bool, critical: tuple) -> str:
    return f"{(game_power / (critical[0] if condition else critical[1])) * 100:.2f} %"