# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

import PRELOAD
from LOGIC import Tool


class Particle(pygame.sprite.Sprite):
    def __init__(th, effective: pygame.Rect, size: tuple, speed: float, angle: float, pos: tuple, color: tuple, type: str='normal'):
        super().__init__()

        th.effective = effective
        th.speed = speed
        th.current_angle = angle
        th.type = type

        th.is_rotated = False

        th.original_image = PRELOAD.particle_cache[f"{size}_{color}"]
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.rect = th.image.get_rect(center=th.rect.center)
            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)
            th.is_rotated = True
        if th.type != 'normal':
            th.speed -= 0.1
            if th.speed < -4:
                th.speed = -4

        rad = math.radians(th.current_angle)
        sin, cos = math.sin(rad), math.cos(rad)
        th.x, th.y = Tool.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


def spawn_particles(group: pygame.sprite.Group, size: tuple, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    randint = random.randint
    choice = random.choice
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])
        sprite = Particle(PRELOAD.effective, (size[0], size[1]), randint(speed[0], speed[1]), i, pos, color)

        group.add(sprite)