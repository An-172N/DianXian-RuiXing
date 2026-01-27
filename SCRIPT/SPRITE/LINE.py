# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from LOGIC import FUNC


class Line(pygame.sprite.Sprite):
    def __init__(th, size: tuple, border: int, damage: int, angle: float, pos: tuple, color: tuple, target_color: tuple):
        super().__init__()

        th.width = size[0]
        th.height = size[1]
        th.border = border
        th.damage = damage
        th.current_angle = angle
        th.color = color
        th.target_color = target_color

        th.type = "line"
        th.timer = 0
        th.is_rotated = False

        th.original_image = th.get_surface()
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos

    def get_surface(th) -> pygame.Surface:
        surface = pygame.Surface((th.width, th.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, th.color, surface.get_rect(), th.border)
            
        return surface
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.is_rotated = True

        th.timer += 1

        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color

            th.image.fill(th.color, special_flags=pygame.BLEND_RGBA_MULT)


def line_barrage(color: list, target_pos: tuple, group: pygame.sprite.Group) -> None:
    start_pos = (random.randint(100, 480), 0)
    end_pos = (-target_pos[0], -target_pos[1])

    delta_pos = FUNC.add(end_pos, start_pos)
    distance = math.hypot(delta_pos[0], delta_pos[1])

    sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
    atan2 = math.atan2(-delta_pos[0], -delta_pos[1])
    current_angle = math.degrees(atan2)
                
    sprite = Line((3, distance), 0, 0, current_angle, sprite_pos, color[1], color[2])
    sprite.update()
    
    group.add(sprite)

    return None


def line_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    for _ in range(12):
        current_angle = random.randint(0, 360)

        sprite = Line((2, random.randint(64, 256)), 0, 6, current_angle, spawn_pos, (45, 194, 229), (128, 0, 128))
        sprite.update()

        group.add(sprite)

    return None