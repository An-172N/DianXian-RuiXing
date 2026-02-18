# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math


import pygame


import PRELOAD
from LOGIC import Tool


class Barrage(pygame.sprite.Sprite):
    def __init__(th, effective: pygame.Rect, type: str, speed: float, color: tuple, angle: float, pos: tuple, mask: bool=True):
        super().__init__()

        th.effective = effective
        th.type = type
        th.speed = speed
        th.color = color
        th.current_angle = angle

        th.is_rotated = False
        th.is_mask = mask

        th.original_image = PRELOAD.barrage_cache[f"{th.type}_{th.color}"]
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            if th.is_mask:
                th.mask = pygame.mask.from_surface(th.image)
            th.rect = th.image.get_rect(center=th.rect.center)
            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)
            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin, cos = math.sin(rad), math.cos(rad)
        th.x, th.y = Tool.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


def circle_barrage(type: int, color: list, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    two_point = Tool.add((target_pos[0], target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
    atan2 = math.atan2(-two_point[0], -two_point[1])
    current_angle = math.degrees(atan2)
    sprite = Barrage(PRELOAD.effective, type, 3, color[0], current_angle, spawn_pos)

    sprite.update()
    group.add(sprite)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    for i in range(target_pos[0] - 32, target_pos[0] + 33, 64):
        two_point = Tool.add((i, target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        current_angle = math.degrees(atan2)
        sprite = Barrage(PRELOAD.effective, type, 3, color[0], current_angle, spawn_pos)

        sprite.update()
        group.add(sprite)


def point_barrage(type: int, color: list, target_pos: tuple, group: pygame.sprite.Group) -> None:
    randint = random.randint

    for _ in range(3):
        sprite_pos = (randint(120, 465), randint(15, 225))
        two_point = Tool.add((target_pos[0], target_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        current_angle = math.degrees(atan2)
        sprite = Barrage(PRELOAD.effective, type, 4, color[0], current_angle, sprite_pos)

        sprite.update()
        group.add(sprite)