# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

from LOGIC import Tool


class Item(pygame.sprite.Sprite):
    item_image = {
        f"R_IT_{(0, 255, 0)}": Tool.draw_rectangle((9, 9), 2, (0, 255, 0)).convert_alpha(),
        f"R_IT_{(45, 194, 229)}": Tool.draw_rectangle((9, 9), 2, (45, 194, 229)).convert_alpha(),
        f"R_IT_{(255, 255, 255)}": Tool.draw_rectangle((9, 9), 2, (255, 255, 255)).convert_alpha()
    }

    def __init__(th, type: str, speed: float, color: tuple, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed

        th.current_angle = 0
        th.is_rotated = False

        th.image = th.get_type(type, color)
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def get_type(th, type: str, color: tuple) -> pygame.Surface:
        item_dict = {
            "power": lambda: Item.item_image[f"R_IT_{color}"],
            "flash": lambda: Item.item_image[f"R_IT_{color}"],
            "fire": lambda: Item.item_image[f"R_IT_{color}"]
        }

        return item_dict.get(type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)

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