# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

import PRELOAD
from LOGIC import Tool


class Bullet(pygame.sprite.Sprite):
    def __init__(th, effective: pygame.Rect, type: str, speed: float, angle: float, damage: int, pos: tuple):
        super().__init__()

        th.effective = effective
        th.type = type
        th.speed = speed
        th.current_angle = angle
        th.damage = damage

        th.is_rotated = False

        th.original_image = PRELOAD.bullet_cache[th.type]
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.rect = th.image.get_rect(center=th.rect.center)
            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)
            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin, cos = math.sin(rad), math.cos(rad)
        th.x, th.y = Tool.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


def circle_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    rands = random.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        sprite = Bullet(PRELOAD.effective, "bullet", 16, i, 4, spawn_pos)

        sprite.update()
        group.add(sprite)


def polygon_brick(group: pygame.sprite.Group, *spawn_pos: tuple) -> None:
    choice = random.choice
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
        sprite = Bullet(PRELOAD.effective, "bullet-cross", 16, bullet_info['angle'], 4, bullet_info['pos'])

        sprite.update()
        group.add(sprite)


def point_brick(group: pygame.sprite.Group) -> None:
    randint = random.randint

    for _ in range(24):
        sprite_pos = (randint(120, 465), randint(15, 345))
        current_angle = randint(0, 360)
        sprite = Bullet(PRELOAD.effective, "bullet", 16, current_angle, 4, sprite_pos)

        sprite.update()
        group.add(sprite)