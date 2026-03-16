# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any, ParamSpec, Concatenate


P = ParamSpec('P')


def load(
    file: bytes,
    func: Callable[Concatenate[int, str, P], Any],
    *args: Any,
    decode: str = 'ascii'
) -> str:
    content = file.decode(decode)
    lines = content.splitlines()

    for row, line in enumerate(lines):
        func(row, line, *args)

    return content


def follow(
    numbers: tuple[int, int],
    end: int,
    start: int = 1
) -> tuple[int, int]:
    stage, level = numbers

    if level >= end:
        stage += 1
        level = start
    else:
        level += 1

    return stage, level