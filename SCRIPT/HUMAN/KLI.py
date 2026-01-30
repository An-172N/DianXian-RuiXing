# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import itertools
import math

import pygame

from SCRIPT import SPRITE, char_image
from LOGIC import FUNC, Rect


class Kli(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group):
        super().__init__()

        th.group = group
        th.particle_group = particle_group

        th.color = (45, 194, 229)

        th.original_image = char_image
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0

        th.point = None

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 30 >= 10 and th.particle_counter <= 0:
            for i, j in itertools.product(
                range(th.rect.centerx - 64, th.rect.centerx + 65, 32),
                range(th.rect.centery - 64, th.rect.centery + 65, 32)
            ):
                pos = (i, j)
                two_point = FUNC.add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                atan2 = math.atan2(-two_point[0], -two_point[1])
                current_angle = math.degrees(atan2)

                particle = SPRITE.Particle.Particle((9, 9), 4, current_angle, pos, (255, 255, 255))

                th.particle_group.add(particle)

            th.particle_counter += 1
            th.point = Rect.Rect((2, 2), 0, (0, 0, 0), th.rect.center)

        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)

        if th.bullet_timer >= 30 and th.bullet_timer % 1 == 0 and th.bullet_counter < 6:
            for i in range(120, 466, 15):
                sprite = SPRITE.Bullet.Bullet("bomb", -24, 0, 6, (i, 0))
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th, power: int) -> None:
        p = 2 ** (power // 32)
        q = 2 ** (power // 16)
    
        for i, j in itertools.product(range(0, p), range(-q, q + 1, q)):
            dx = 0 + i * 10
            dy = 0 + i * 12
            bullet_type = [
                {
                    'x': th.rect.left - dx,
                    'y': th.rect.top + dy,
                    'angle': j
                },
                {
                    'x': th.rect.right + dx,
                    'y': th.rect.top + dy,
                    'angle': -j
                }
            ]

            for bullet_info in bullet_type:
                sprite = SPRITE.Bullet.Bullet("bullet", 16, bullet_info['angle'], 4, (bullet_info['x'], bullet_info['y']))
                sprite.update()

                th.group.add(sprite)

    def reset_bullet(th) -> None:
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0