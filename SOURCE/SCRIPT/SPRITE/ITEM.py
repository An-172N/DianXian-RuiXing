# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

import PRELOAD


class Item(pygame.sprite.Sprite):
    def __init__(th, type: str, speed: float, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed

        th.is_rotated = False

        th.image = PRELOAD.item_cache[th.type]
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

        if th.rect.centery >= 360:
            th.kill()


def item_spawn(group: pygame.sprite.Group, condition: bool, pos: tuple, speed: float, type: str, timer: int=0) -> int:
    timer += 1

    if condition:
        sprite = Item(type, speed, pos)

        group.add(sprite)

        timer = 0

    return timer