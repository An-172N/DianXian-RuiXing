# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

import PRELOAD
from LOGIC import FUNC, Tool


class Barrage(pygame.sprite.Sprite):
    barrage_dict = {
        f"C_BA_{(255, 128, 0)}": Tool.draw_circle((0, 0, 9, 9), 0, (255, 128, 0)).convert_alpha(),
        f"C_BA_{(251, 234, 18)}": Tool.draw_circle((0, 0, 9, 9), 0, (251, 234, 18)).convert_alpha(),
        f"C_BA_{(255, 255, 255)}": Tool.draw_circle((0, 0, 9, 9), 0, (255, 255, 255)).convert_alpha(),
        f"T_BA_{(0, 255, 0)}": PRELOAD.barrage_image.subsurface((0, 0, 9, 8)),
        f"T_BA_{(255, 255, 255)}": PRELOAD.barrage_image.subsurface((9, 0, 9, 8))
    }

    def __init__(th, type: str, speed: float, color: tuple, angle: float, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed
        th.color = color
        th.current_angle = angle

        th.is_rotated = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos

    def get_type(th, type: int) -> pygame.Surface:
        bullet_dict = {
            0: lambda: Barrage.barrage_dict[f"T_BA_{th.color}"],
            2: lambda: Barrage.barrage_dict[f"C_BA_{th.color}"]
        }

        return bullet_dict.get(type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)

            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin, cos = math.sin(rad), math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)


def circle_barrage(type: int, color: list, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    two_point = FUNC.add((target_pos[0], target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
    atan2 = math.atan2(-two_point[0], -two_point[1])
    current_angle = math.degrees(atan2)

    sprite = Barrage(type, 3, color[0], current_angle, spawn_pos)
    sprite.update()

    group.add(sprite)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, target_pos: tuple, group: pygame.sprite.Group) -> None:
    for i in range(target_pos[0] - 32, target_pos[0] + 33, 64):
        two_point = FUNC.add((i, target_pos[1]), (-spawn_pos[0], -spawn_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        current_angle = math.degrees(atan2)
        
        sprite = Barrage(type, 3, color[0], current_angle, spawn_pos)
        sprite.update()

        group.add(sprite)


def point_barrage(type: int, color: list, target_pos: tuple, group: pygame.sprite.Group) -> None:
    randint = random.randint

    for _ in range(3):
        sprite_pos = (randint(120, 465), randint(15, 225))
        two_point = FUNC.add((target_pos[0], target_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
        atan2 = math.atan2(-two_point[0], -two_point[1])
        current_angle = math.degrees(atan2)

        sprite = Barrage(type, 4, color[0], current_angle, sprite_pos)
        sprite.update()

        group.add(sprite)