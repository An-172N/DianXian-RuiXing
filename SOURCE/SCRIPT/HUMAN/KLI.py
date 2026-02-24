# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, uniform


import pygame as pg


from PRELOAD import char_image, effective, color_dict, bullet_cache
from SCRIPT.SPRITE import Item, Bullet
from LOGIC.SPRITE import Base


class Kli(Base):
    __slots__ = ('group', 'particle_group', 'color', 'torrent', 'bullet_timer', 'point')

    def __init__(th, *group: pg.sprite.Group):
        super().__init__(None, char_image.subsurface((0, 0, 12, 26)), group[2], pos=(292, 332))

        th.group = group[0]
        th.particle_group = group[1]
        th.color = color_dict[5]
        th.torrent = 0
        th.bullet_timer = 0
        th.point = None

    def free(th):
        th.bullet_timer += 1

        if th.bullet_timer == 10:
            for i in range(120, 466, 15):
                pos = (i, randint(345, 360))
                rands = choice([3, 6, 9, 12])

                Item.Item('char', uniform(1, 2), pos, th.particle_group, size=(rands, rands), color=color_dict[6])

        if th.bullet_timer >= 30 and th.torrent < 6:
            for i in range(120, 466, 15):
                Bullet.Bullet(effective, "bomb", -24, th.color, 0, (i, 0), 6, bullet_cache["bomb"], th.group, mask=False)

            th.torrent += 1

    def fire(th, power: int):
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
                    Bullet.Bullet(effective, "bullet", 16, th.color, bullet_info['angle'], (bullet_info['x'], bullet_info['y']), 4, bullet_cache["bullet"], th.group, mask=False)

    def reset_bullet(th):
        th.torrent = 0
        th.bullet_timer = 0