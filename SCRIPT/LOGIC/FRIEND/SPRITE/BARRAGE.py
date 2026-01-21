# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import math

import pygame

from SCRIPT import GLOBAL, FUNC


class Barrage(pygame.sprite.Sprite):
    def __init__(th, type: str, speed: float, color: tuple):
        super().__init__()

        th.type = type
        th.speed = speed
        th.color = color

        th.current_angle = 0
        th.is_rotated = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

    def get_type(th, type: int) -> pygame.Surface:
        bullet_dict = {
            0: lambda: GLOBAL.sprite_image[f"T_BA_{th.color}"],
            1: lambda: GLOBAL.sprite_image[f"R_BA_{th.color}"],
            2: lambda: GLOBAL.sprite_image[f"C_BA_{th.color}"]
        }

        return bullet_dict.get(type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x = getattr(th, 'x', th.rect.centerx)
            th.y = getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin = math.sin(rad)
        cos = math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)