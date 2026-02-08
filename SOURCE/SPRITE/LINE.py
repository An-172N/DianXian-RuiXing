# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from SOURCE.LOGIC import FUNC, Tool


class Line(pygame.sprite.Sprite):
    def __init__(th, size: tuple, damage: int, angle: float, pos: tuple, color: tuple, target_color: tuple):
        super().__init__()

        th.damage = damage
        th.current_angle = angle
        th.color = color
        th.target_color = target_color

        th.type = "line"
        th.timer = 0
        th.is_rotated = False

        th.original_image = Tool.draw_rectangle((size[0], size[1]), 0, th.color).convert_alpha()
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos

    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)

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
                
    sprite = Line((3, distance), 0, current_angle, sprite_pos, color[1], color[2])
    sprite.update()
    
    group.add(sprite)


def line_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    randint = random.randint

    for _ in range(12):
        current_angle = randint(0, 360)

        sprite = Line((2, randint(32, 256)), 6, current_angle, spawn_pos, (45, 194, 229), (128, 0, 128))
        sprite.update()

        group.add(sprite)