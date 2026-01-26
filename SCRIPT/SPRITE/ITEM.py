# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame
import os


class Item(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    item_image = {
        key: pygame.image.load(file).convert_alpha() for key, file in [
            (f"R_IT_{(0, 255, 0)}", os.path.join(asset_path, f'IMAGE\IMG_ITEMGREEN.png')),
            (f"R_IT_{(45, 194, 229)}", os.path.join(asset_path, f'IMAGE\IMG_ITEMBLUE.png')),
            (f"R_IT_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_ITEMWHITE.png'))
        ]
    }

    def __init__(th, type: str, speed: float, color: tuple, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed
        th.color = color

        th.current_angle = 0
        th.is_rotated = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def get_type(th, type: str) -> pygame.Surface:
        item_dict = {
            "power": lambda: Item.item_image[f"R_IT_{th.color}"],
            "flash": lambda: Item.item_image[f"R_IT_{th.color}"],
            "fire": lambda: Item.item_image[f"R_IT_{th.color}"]
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


def item_spawn(group: pygame.sprite.Group, condition: bool, pos: tuple, speed: float, color: tuple, type: str, timer: int=0) -> int:
    timer += 1

    if condition:
        sprite = Item(type, speed, color, pos)

        group.add(sprite)

        timer = 0

    return timer