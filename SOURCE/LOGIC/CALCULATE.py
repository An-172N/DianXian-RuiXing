# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame


def round_angle(angle: int, limit: int=180, step: int=6) -> int:
    rounded = round((angle % limit) / step) * step

    return 0 if rounded == limit else rounded


def update_fps(fps: object, timer: int, bit: int, interval: int, clock: pygame.time.Clock) -> tuple:
    current_time = pygame.time.get_ticks()

    if current_time - timer >= interval:
        fps = f"{clock.get_fps():.{bit}f} FPS"
        timer = current_time

    return fps, timer


def add(*tuples: tuple) -> tuple:
    return tuple(map(sum, zip(*tuples)))


def fibonacci(former: int, latter: int, frequency: int) -> int:
    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(min(value, max(minimum, maximum)), min(minimum, maximum))