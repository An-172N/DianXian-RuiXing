# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import math

import pygame

from SCRIPT import FUNC


class Particle(pygame.sprite.Sprite):
    def __init__(th, size: tuple, speed: float, angle: float, color: tuple):
        super().__init__()

        th.width = size[0]
        th.height = size[1]
        th.speed = speed
        th.color = color
        th.current_angle = angle

        th.is_rotated = False

        th.original_image = th.get_surface()
        th.image = th.original_image
        th.rect = th.image.get_rect()

    def get_surface(th) -> pygame.Surface:
        surface = pygame.Surface((th.width, th.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, th.color, surface.get_rect(), 0)
            
        return surface
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x = getattr(th, 'x', th.rect.centerx)
            th.y = getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin = math.sin(rad)
        cos = math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)