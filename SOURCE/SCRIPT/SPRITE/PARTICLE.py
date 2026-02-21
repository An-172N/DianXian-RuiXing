# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice


import pygame


from PRELOAD import particle_cache, effective
from SCRIPT.SPRITE import Barrage


def spawn_particles(group: pygame.sprite.Group, size: tuple, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])
        sprite = Barrage.Barrage(effective, None, randint(speed[0], speed[1]), color, i, pos, particle_cache[f"{size}_{color}"], False, False)

        group.add(sprite)