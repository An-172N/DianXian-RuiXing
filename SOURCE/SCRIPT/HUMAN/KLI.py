# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import uniform, randint, choice


import pygame


from PRELOAD import char_image, color_dict, effective, bullet_cache
from SCRIPT.SPRITE import Item, Bullet
from LOGIC.SPRITE import Base


class Kli(Base):
    __slots__ = ('group', 'particle_group', 'color', 'bullet_counter', 'bullet_timer', 'particle_counter', 'point')

    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group):
        super().__init__(None, char_image.subsurface((0, 0, 12, 26)), pos=(292, 332))

        th.group = group
        th.particle_group = particle_group

        th.color = color_dict[5]

        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0

        th.point = None

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 30 >= 10 and th.particle_counter <= 0:
            for i in range(120, 466, 15):
                pos = (i, randint(345, 360))
                rands = choice([3, 6, 9, 12])
                sprite = Item.Item('char', uniform(1, 2), pos, (rands, rands), color_dict[6])

                th.particle_group.add(sprite)

            th.particle_counter += 1

        if th.bullet_timer >= 30 and th.bullet_counter < 6:
            for i in range(120, 466, 15):
                sprite = Bullet.Bullet(effective, "bomb", -24, th.color, 0, (i, 0), 6, bullet_cache["bomb"], False)

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
                    sprite = Bullet.Bullet(effective, "bullet", 16, th.color, bullet_info['angle'], (bullet_info['x'], bullet_info['y']), 4, bullet_cache["bullet"], False)

                    sprite.update()
                    th.group.add(sprite)

    def reset_bullet(th) -> None:
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0