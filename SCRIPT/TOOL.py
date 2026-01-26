# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import datetime
import re

import pygame


def vector(sprite_pos: tuple, target_pos: tuple, speed: float) -> pygame.Vector2:
    dir = pygame.math.Vector2(target_pos[0] - sprite_pos[0], target_pos[1] - sprite_pos[1])
    current = pygame.math.Vector2(sprite_pos[0], sprite_pos[1])
    target = pygame.math.Vector2(target_pos[0], target_pos[1])

    delta_vec = target_pos - current
    distance = delta_vec.length()

    if distance < speed:
        return target, delta_vec
    else:
        if distance > 0:
            dir.normalize_ip()

        return current + dir * speed, delta_vec
    

def get_datetime() -> tuple:
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H-%M-%S')

    return date, time


def replace_illegal_char(name: str) -> str:
    return re.sub(r'[!<>:"/\\|?*]', '_', name)