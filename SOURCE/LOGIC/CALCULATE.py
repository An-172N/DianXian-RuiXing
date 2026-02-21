# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def round_angle(angle: int, step: int=9) -> int:
    angle %= 360
    if angle >= 180:
        angle -= 180

    rounded = round(angle / step) * step
    if rounded == 180:
        rounded = 0

    return rounded


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