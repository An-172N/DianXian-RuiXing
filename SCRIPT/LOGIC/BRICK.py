# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random

import pygame

from SCRIPT import SPRITE


def brick_death(death_condition: bool) -> bool:
    death_condition = True

    return death_condition


def circle_brick(group: pygame.sprite.Group, *spawn_pos: tuple) -> None:
    rands = random.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        sprite = SPRITE.Bullet("bullet", 16, i, 4, spawn_pos[3])
        sprite.update()

        group.add(sprite)


def polygon_brick(group: pygame.sprite.Group, *spawn_pos: tuple) -> None:
    bullet_index = [
        {
            'angle': random.choice([-30, -210]),
            'pos': spawn_pos[0]
        },
        {
            'angle': random.choice([30, 210]),
            'pos': spawn_pos[1]
        },
        {
            'angle': random.choice([90, 270]),
            'pos': spawn_pos[2]
        }
    ]

    for bullet_info in bullet_index:
        sprite = SPRITE.Bullet("bullet-cross", 16, bullet_info['angle'], 4, bullet_info['pos'])
        sprite.update()

        group.add(sprite)


def line_brick(group: pygame.sprite.Group, color: tuple, target_color: tuple, *spawn_pos: tuple) -> None:
    for _ in range(12):
        current_angle = random.randint(0, 360)

        sprite = SPRITE.Line((2, random.randint(64, 256)), 0, 6, current_angle, spawn_pos[3], color, target_color)
        sprite.update()

        group.add(sprite)


def point_brick(group: pygame.sprite.Group):
    for _ in range(24):
        sprite_pos = (random.randint(120, 465), random.randint(15, 345))
        current_angle = random.randint(0, 360)

        sprite = SPRITE.Bullet("bullet", 16, current_angle, 4, sprite_pos)
        sprite.update()

        group.add(sprite)