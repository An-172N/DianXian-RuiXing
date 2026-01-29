# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from LOGIC import FUNC, Rect


class Particle(pygame.sprite.Sprite):
    def __init__(th, size: tuple, speed: float, angle: float, pos: tuple, color: tuple):
        super().__init__()

        th.width, th.height = size
        th.speed = speed
        th.color = color
        th.current_angle = angle

        th.is_rotated = False

        th.original_image = Rect.Rect((th.width, th.height), 0, th.color).image
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)
            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin, cos = math.sin(rad), math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)


def spawn_particles(group: pygame.sprite.Group, size: tuple, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    rands = random.randint(0, 45)
    
    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else random.choice([color1, color2])

        sprite = Particle((size[0], size[1]), random.randint(speed[0], speed[1]), i, pos, color)
        
        group.add(sprite)