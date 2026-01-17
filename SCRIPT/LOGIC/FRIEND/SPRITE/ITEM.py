# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import pygame

from SCRIPT import GLOBAL


class Item(pygame.sprite.Sprite):
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

    def get_type(th, type: str) -> pygame.Surface:
        item_dict = {
            "power": lambda: GLOBAL.sprite_image[f"R_IT_{th.color}"],
            "flash": lambda: GLOBAL.sprite_image[f"R_IT_{th.color}"],
            "fire": lambda: GLOBAL.sprite_image[f"R_IT_{th.color}"]
        }

        return item_dict.get(type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.x = getattr(th, 'x', th.rect.centerx)
            th.y = getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        th.y -= th.speed
        
        if th.type in ["power", "flash"]:
            th.speed -= 0.1

            if th.speed < -2:
                th.speed = -2

        th.rect.center = (th.x, th.y)