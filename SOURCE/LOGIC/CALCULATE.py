# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import math


import pygame


def round_angle(
    angle: int | float,
    limit: int | float = 180,
    step: int = 6
) -> int:
    rounded = round((angle % limit) / step) * step

    return 0 if rounded == limit else rounded


def update_fps(
    fps: str,
    timer: int,
    bit: int,
    interval: int,
    clock: pygame.time.Clock
) -> tuple:
    current_time = pygame.time.get_ticks()

    if current_time - timer >= interval:
        fps = f"{clock.get_fps():.{bit}f} FPS"
        timer = current_time

    return fps, timer


def bearing(
    x: float,
    y: float
) -> float:
    return math.degrees(math.atan2(x, y))


def add(
    *packs: tuple[int | float, ...] | list[int | float] | set[int | float]
) -> tuple:
    return tuple(map(sum, zip(*packs)))


def clamp(
    value: int | float,
    minimum: int | float,
    maximum: int | float
) -> int | float:
    return max(min(value, max(minimum, maximum)), min(minimum, maximum))


def fibonacci(
    former: int | float,
    latter: int | float,
    frequency: int
) -> int | float:
    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)