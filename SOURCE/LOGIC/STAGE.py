# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any


def load_level(
    timer: int,
    loaded: bool,
    end: int,
    load: Callable[..., Any],
    *args: Any
) -> tuple[int, bool]:
    if timer <= end:
        timer += 1
    else:
        load(*args)

        timer = 0
        loaded = True

    return timer, loaded


def next_level(
    numbers: tuple[int, int],
    end: int
) -> tuple[int, int]:
    stage, level = numbers

    if level >= end:
        stage += 1
        level = 1
    else:
        level += 1

    return stage, level