# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from LOGIC import FUNC, Rect


class Bullet(pygame.sprite.Sprite):
    bullet_image = {
        "KLI_BULLET": Rect.Rect((2, 15), 0, (45, 194, 229)).image,
        "KLI_BOMB": Rect.Rect((15, 15), 0, (45, 194, 229)).image
    }

    def __init__(th, type: str, speed: float, angle: float, damage: int, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed
        th.current_angle = angle
        th.damage = damage

        th.is_rotated = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def get_type(th, type: str) -> pygame.Surface:
        bullet_dict = {
            "bomb": lambda: Bullet.bullet_image[f"KLI_BOMB"],
            "bullet": lambda: Bullet.bullet_image[f"KLI_BULLET"],
            "bullet-cross": lambda: Bullet.bullet_image[f"KLI_BULLET"],
        }

        return bullet_dict.get(type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x = getattr(th, 'x', th.rect.centerx)
            th.y = getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin = math.sin(rad)
        cos = math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)


def circle_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    rands = random.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        sprite = Bullet("bullet", 16, i, 4, spawn_pos)
        sprite.update()

        group.add(sprite)

    return None


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
        sprite = Bullet("bullet-cross", 16, bullet_info['angle'], 4, bullet_info['pos'])
        sprite.update()

        group.add(sprite)

    return None


def point_brick(group: pygame.sprite.Group) -> None:
    for _ in range(24):
        sprite_pos = (random.randint(120, 465), random.randint(15, 345))
        current_angle = random.randint(0, 360)

        sprite = Bullet("bullet", 16, current_angle, 4, sprite_pos)
        sprite.update()

        group.add(sprite)

    return None