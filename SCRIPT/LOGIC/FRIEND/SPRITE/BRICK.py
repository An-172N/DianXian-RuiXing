# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

from SCRIPT import GLOBAL


class Brick(pygame.sprite.Sprite):
    def __init__(th, type: str, hp: int, color: tuple):
        super().__init__()

        th.type = type
        th.color = color
        th.hp = hp

        th.have_power = False
        th.have_flash = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

    def get_type(th, type: int) -> pygame.Surface:
        brick_dict = {
            0: lambda: GLOBAL.sprite_image[f"T_BR_{th.color}"],
            1: lambda: GLOBAL.sprite_image[f"R_BR_{th.color}"],
            2: lambda: GLOBAL.sprite_image[f"C_BR_{th.color}"]
        }

        return brick_dict.get(type)()
    
    def update(th) -> None:
        pass