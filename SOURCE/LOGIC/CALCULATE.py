# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import math


import pygame


def vector(
    current: tuple[int | float, int | float],
    target: tuple[int | float, int | float],
    delay: int | float
) -> tuple[pygame.Vector2, pygame.Vector2]:
    direction_vec = pygame.math.Vector2(target[0] - current[0], target[1] - current[1])
    current_vec = pygame.math.Vector2(*current)
    target_vec = pygame.math.Vector2(*target)
    delta_vec = target_vec - current_vec
    distance = delta_vec.length()

    if distance < delay:
        return target_vec, delta_vec
    else:
        if distance > 0:
            direction_vec.normalize_ip()

        return current_vec + direction_vec * delay, delta_vec


def approximate(
    value: int | float,
    limit: int = 180,
    step: int = 6
) -> int:
    return 0 if (rounded := round((value % limit) / step) * step) == limit else rounded


def bearing(
    x: float,
    y: float
) -> float:
    return math.degrees(math.atan2(x, y)) % 360


def add(
    *packs: tuple[int | float, ...] | list[int | float] | set[int | float]
) -> tuple[int | float, ...]:
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