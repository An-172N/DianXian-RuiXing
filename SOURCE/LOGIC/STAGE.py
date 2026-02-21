# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


def score_summary(power: int, unflash: int, combo: int, collection: tuple) -> int:
    return power * collection[0] + unflash * collection[1] + collection[2] ** combo


def close_summary(numbers: tuple, score: int, bonus: int, end: object, next: object) -> tuple:
    end() if numbers[0][0] >= numbers[1][0] and numbers[0][1] == numbers[1][1] else next()

    return False, score + bonus


def load_level(timer: int, loaded: bool, end: int, load: object) -> tuple:
    if timer <= end:
        timer += 1
    else:
        load()

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