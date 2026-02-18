# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random


import pygame


import PRELOAD
from SCRIPT import SPRITE


class Kli(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group):
        super().__init__()

        th.group = group
        th.particle_group = particle_group

        th.color = PRELOAD.color_dict[5]

        th.original_image = PRELOAD.char_image
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0

        th.point = None

        th.rect.center = (292, 332)

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 30 >= 10 and th.particle_counter <= 0:
            for i in range(120, 466, 15):
                pos = (i, random.randint(345, 360))
                rands = random.choice([4, 6, 9, 10, 12])

                sprite = SPRITE.Particle.Particle(PRELOAD.effective, (rands, rands), random.uniform(1, 2), 0, pos, PRELOAD.color_dict[6], 'char')

                th.particle_group.add(sprite)

            th.particle_counter += 1

        if th.bullet_timer >= 30 and th.bullet_counter < 6:
            for i in range(120, 466, 15):
                sprite = SPRITE.Bullet.Bullet(PRELOAD.effective, "bomb", -24, 0, 6, (i, 0))
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th, power: int) -> None:
        p = 2 ** (power // 32)
        q = 2 ** (power // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
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
                    sprite = SPRITE.Bullet.Bullet(PRELOAD.effective, "bullet", 16, bullet_info['angle'], 4, (bullet_info['x'], bullet_info['y']))
                    sprite.update()

                    th.group.add(sprite)

    def reset_bullet(th) -> None:
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0