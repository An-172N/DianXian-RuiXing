# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import datetime
import re

import pygame


def vector(present: tuple, target: tuple, speed: float) -> tuple:
    dir = pygame.math.Vector2(target[0] - present[0], target[1] - present[1])
    current = pygame.math.Vector2(present[0], present[1])
    target = pygame.math.Vector2(target[0], target[1])

    delta_vec = target - current
    distance = delta_vec.length()

    if distance < speed:
        return target, delta_vec
    else:
        if distance > 0:
            dir.normalize_ip()

        return current + dir * speed, delta_vec
    

def update_fps(fps: object, timer: int, bit: int, interval: int, clock: pygame.time.Clock) -> tuple:
    current_time = pygame.time.get_ticks()

    if current_time - timer >= interval:
        fps = f"{clock.get_fps():.{bit}f} FPS"
        timer = current_time

    return fps, timer


def draw_rectangle(size: tuple, border: float, color: tuple) -> pygame.Surface:
    surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)

    pygame.draw.rect(surface, color, surface.get_rect(), border)
            
    return surface


def draw_circle(xy_size: tuple, border: float, color: tuple) -> pygame.Surface:
    surface = pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA)

    pygame.draw.ellipse(surface, color, xy_size, border)

    return surface
    

def get_datetime() -> tuple:
    return datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H-%M-%S')


def replace_illegal_char(string: str) -> str:
    return re.sub(r'[!<>:"/\\|?*]', '_', string)


def turncate_string(string: str, length: int) -> str:
    return string if len(string) <= length else string[:length]