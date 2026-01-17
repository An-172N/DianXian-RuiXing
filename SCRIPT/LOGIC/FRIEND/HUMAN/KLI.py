# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import pygame

from SCRIPT import GLOBAL, LOGIC


class Kli(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.color = GLOBAL.color_dict[5]

        th.original_image = GLOBAL.char_image["Kli"]
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.bullet_counter = 0
        th.bullet_timer = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer >= 30 and th.bullet_timer % 1 == 0 and th.bullet_counter < 6:
            for i in range(120, 466, 15):
                sprite = LOGIC.Bullet("bomb", -24, 0, 6)
                sprite.rect.center = (i, 0)
                GLOBAL.bullet_group.add(sprite)

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
            sprite = LOGIC.Bullet("bullet", 16, bullet_info['angle'], 4)
            sprite.rect.center = (bullet_info['x'], bullet_info['y'])
            GLOBAL.bullet_group.add(sprite)


class DecisionPoint(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()
        th.original_image = GLOBAL.sprite_image[f"DEC"]
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)