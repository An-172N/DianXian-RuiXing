# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import os

import pygame

from SCRIPT import SPRITE


class Kli(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    char_image = pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_KLI.png')).convert_alpha()

    def __init__(th, group: pygame.sprite.Group):
        super().__init__()

        th.group = group

        th.color = (45, 194, 229)

        th.original_image = th.char_image
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.bullet_counter = 0
        th.bullet_timer = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer >= 30 and th.bullet_timer % 1 == 0 and th.bullet_counter < 6:
            for i in range(120, 466, 15):
                sprite = SPRITE.Bullet("bomb", -24, 0, 6, (i, 0))
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th, dx: float, dy: float, angle: float) -> None:
        left = th.rect.left
        top = th.rect.top
        right = th.rect.right

        bullet_type = [
            {
                'x': left - dx,
                'y': top + dy,
                'angle': angle
            },
            {
                'x': right + dx,
                'y': top + dy,
                'angle': -angle
            }
        ]

        for bullet_info in bullet_type:
            sprite = SPRITE.Bullet("bullet", 16, bullet_info['angle'], 4, (bullet_info['x'], bullet_info['y']))
            sprite.update()

            th.group.add(sprite)

    def reset_bullet(th) -> None:
        th.bullet_counter = 0
        th.bullet_timer = 0