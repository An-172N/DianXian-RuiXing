# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

from LOGIC import Tool


class Item(pygame.sprite.Sprite):
    item_cache = {
        "flash": Tool.draw_rectangle((9, 9), 2, (0, 255, 0)).convert_alpha(),
        "power": Tool.draw_rectangle((9, 9), 2, (45, 194, 229)).convert_alpha(),
        "fire": Tool.draw_rectangle((9, 9), 2, (255, 255, 255)).convert_alpha()
    }

    def __init__(th, type: str, speed: float, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed

        th.is_rotated = False

        th.image = Item.item_cache[th.type]
        th.rect = th.image.get_rect()

        th.rect.center = pos
    
    def update(th) -> None:
        if not th.is_rotated:
            th.rect = th.image.get_rect(center=th.rect.center)
            
            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        th.y -= th.speed

        if th.type in ["power", "flash"]:
            th.speed -= 0.1

            if th.speed < -2:
                th.speed = -2

        th.rect.center = (th.x, th.y)


def item_spawn(group: pygame.sprite.Group, condition: bool, pos: tuple, speed: float, type: str, timer: int=0) -> int:
    timer += 1

    if condition:
        sprite = Item(type, speed, pos)

        group.add(sprite)

        timer = 0

    return timer