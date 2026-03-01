# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


def load_level(timer: int, loaded: bool, end: int, load: object, *args: tuple) -> tuple:
    if timer <= end:
        timer += 1
    else:
        load(*args)

        timer = 0
        loaded = True

    return timer, loaded


def level_logic(numbers: tuple, end: int) -> tuple:
    stage, level = numbers

    if level >= end:
        stage += 1
        level = 1
    else:
        level += 1

    return stage, level


def close_summary(numbers: tuple, final: object, proceed: object, *args: tuple):
    return final(*args) if numbers[0][0] >= numbers[1][0] and numbers[0][1] == numbers[1][1] else proceed(*args)