# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random

import pygame

from SCRIPT import GLOBAL, LOGIC


def brick_blast(brick: LOGIC.Brick) -> None:
    if brick.color == (255, 255, 255):
        process_dict = {
            1: circle_brick,
            2: polygon_brick,
            3: line_brick,
            4: point_brick
        }

        process_dict[GLOBAL.stage](brick, GLOBAL.bullet_group, 16)


def brick_death(target: LOGIC.Brick):
    target.is_die = True


def circle_brick(source: LOGIC.Brick, sprite_group: pygame.sprite.Group, speed: float) -> None:
    rands = random.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        current_sprite = LOGIC.Bullet("bullet", speed, i, 4)
        current_sprite.rect.center = source.rect.center
        current_sprite.update()

        sprite_group.add(current_sprite)


def polygon_brick(source: LOGIC.Brick, sprite_group: pygame.sprite.Group, speed: float) -> None:
    midleft = source.rect.midleft
    midright = source.rect.midright
    midbottom = source.rect.midbottom

    bullet_index = [
        {
            'angle': random.choice([-30, -210]),
            'pos': midleft
        },
        {
            'angle': random.choice([30, 210]),
            'pos': midright
        },
        {
            'angle': random.choice([90, 270]),
            'pos': midbottom
        }
    ]

    for bullet_info in bullet_index:
        current_sprite = LOGIC.Bullet("bullet-cross", speed, bullet_info['angle'], 4)
        current_sprite.rect.center = bullet_info['pos']
        current_sprite.update()

        sprite_group.add(current_sprite)


def line_brick(source: LOGIC.Brick, sprite_group: pygame.sprite.Group, _: None) -> None:
    for _ in range(12):
        current_sprite = LOGIC.Line((2, random.randint(64, 256)), 0, 6, GLOBAL.color_dict[5])
        current_sprite.rect.center = source.rect.center
        current_sprite.current_angle = random.randint(0, 360)
        current_sprite.update()

        sprite_group.add(current_sprite)


def point_brick(_: None, sprite_group: pygame.sprite.Group, speed: float):
    for _ in range(24):
        current_sprite = LOGIC.Bullet("bullet", speed, random.randint(0, 360), 4)
        current_sprite.rect.center = (random.randint(120, 465), random.randint(15, 345))
        current_sprite.update()

        sprite_group.add(current_sprite)