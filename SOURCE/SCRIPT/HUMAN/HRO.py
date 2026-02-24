# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice
from math import radians, sin, cos, atan2, degrees


import pygame as pg


from PRELOAD import char_image, effective, color_dict, barrage_cache
from SCRIPT.SPRITE import Barrage
from LOGIC.PLANE import vector
from LOGIC.CALCULATE import add
from LOGIC.DRAW import rectangle
from SCRIPT.HUMAN import Basic


class Hro(Basic):
    __slots__ = ('is_choose', 'flash')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((36, 0, 12, 26)), locate, 224, color_dict[2], *group)

        th.is_choose = False
        th.flash = True

    def free(th):
        bullet_type = [
            {
                'dx1': 140,
                'dy1': 140,
                'dx2': 140,
                'dy2': 140
            },
            {
                'dx1': -140,
                'dy1': -140,
                'dx2': 140,
                'dy2': 140
            }
        ]

        if th.torrent < 18:
            for bullet_info in bullet_type:
                start_pos = (292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = (292 - bullet_info['dy1'], 100 + bullet_info['dy2'])
                current_pos, delta_vec = vector(start_pos, end_pos, th.torrent * 25)

                for j in range(45, 136, 90):
                    atan = atan2(-delta_vec.x, -delta_vec.y)
                    angle = degrees(atan) + j + (th.timer * -6)
                    pos = (current_pos.x, current_pos.y)

                    Barrage.Barrage(effective, 0, 4, th.color, angle, pos, barrage_cache[(0, th.color)], th.group)

            th.torrent += 1

    def extend(th):
        speed = 6

        if th.timer == 0:
            for _ in range(6):
                for j in (150, 185, 220, 255, 292, 327, 365, 400, 435):
                    for k in range(1, 4):
                        pos = (j, 60)
                        two_point = add((th.locate[0], th.locate[1] - 96), (-pos[0], -pos[1]))
                        atan2_ = atan2(-two_point[0], -two_point[1])
                        angle = degrees(atan2_) * k

                        Barrage.Barrage(effective, 0, speed, th.color, angle, pos, barrage_cache[(0, th.color)], th.group)

                speed -= 0.6

    def fire(th):
        if th.timer % 6 == 0 and th.torrent < 3:
            pos = (th.x, th.y)

            for i in range(-30, 31, 30):
                two_point = add((th.locate[0], th.locate[1]), (-pos[0], -pos[1]))
                atan2_ = atan2(-two_point[0], -two_point[1])
                angle = degrees(atan2_) + i

                Barrage.Barrage(effective, 0, 4, th.color, angle, pos, barrage_cache[(0, th.color)], th.group)

            th.torrent += 1

    def update(th):
        th.timer += 1

        if th.timer % 110 == 0:
            th.target_pos = (choice((150, 220, 292, 365)), choice((60, 120, 180, 240)))
            th.torrent = 0
            th.timer = 0
            th.is_choose = False
            th.can_shoot = True
        if th.timer % 110 >= 91:
            if not th.is_choose:
                th.choice = choice([th.fire] * 3 + [th.free, th.extend])
                th.is_choose = True
            if th.timer % 91 == 0:
                for i in range(0, 360, 120 if th.choice == th.fire else 90):
                    pos = (th.x + 45 * cos(radians(i)), th.y + 45 * sin(radians(i)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Barrage.Barrage(effective, 0, 3, color_dict[6], angle, pos, barrage_cache[(0, color_dict[6])], th.particle_group, mask=False)

            th.point = Barrage.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot and not th.is_choose:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 5)[0]