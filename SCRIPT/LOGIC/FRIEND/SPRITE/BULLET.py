# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import math

import pygame

from SCRIPT import GLOBAL, FUNC


class Bullet(pygame.sprite.Sprite):
    def __init__(th, type: str, speed: float, angle: float, damage: int):
        super().__init__()

        th.type = type
        th.speed = speed
        th.current_angle = angle
        th.damage = damage

        th.is_rotated = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()

    def get_type(th, type: str) -> pygame.Surface:
        bullet_dict = {
            "bomb": lambda: GLOBAL.sprite_image[f"KLI_BOMB"],
            "bullet": lambda: GLOBAL.sprite_image[f"KLI_BULLET"],
            "bullet-cross": lambda: GLOBAL.sprite_image[f"KLI_BULLET"],
        }

        return bullet_dict.get(type)()
    
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