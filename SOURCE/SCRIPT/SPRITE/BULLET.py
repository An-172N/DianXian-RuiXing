# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice


import pygame


from PRELOAD import bullet_cache, effective
from LOGIC.SPRITE import Barrage


def circle_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        sprite = Barrage(effective, "bullet", 16, 0, i, spawn_pos, bullet_cache["bullet"], False)
        sprite.damage = getattr(sprite, "damage", 4)

        sprite.update()
        group.add(sprite)


def polygon_brick(group: pygame.sprite.Group, *spawn_pos: tuple) -> None:
    bullet_index = [
        {
            'angle': choice([-30, -210]),
            'pos': spawn_pos[0]
        },
        {
            'angle': choice([30, 210]),
            'pos': spawn_pos[1]
        },
        {
            'angle': choice([90, 270]),
            'pos': spawn_pos[2]
        }
    ]

    for bullet_info in bullet_index:
        sprite = Barrage(effective, "bullet-cross", 16, 0, bullet_info['angle'], bullet_info['pos'], bullet_cache["bullet-cross"], False)
        sprite.damage = getattr(sprite, "damage", 4)

        sprite.update()
        group.add(sprite)


def point_brick(group: pygame.sprite.Group) -> None:
    for _ in range(24):
        sprite_pos = (randint(120, 465), randint(15, 345))
        current_angle = randint(0, 360)
        sprite = Barrage(effective, "bullet", 16, 0, current_angle, sprite_pos, bullet_cache["bullet"], False)
        sprite.damage = getattr(sprite, "damage", 4)

        sprite.update()
        group.add(sprite)