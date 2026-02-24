# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint
from math import radians, sin, cos, atan2, degrees


import pygame as pg


from PRELOAD import char_image, effective, color_dict, barrage_cache
from SCRIPT.SPRITE import Barrage
from LOGIC.PLANE import vector
from LOGIC.CALCULATE import add
from LOGIC.DRAW import rectangle
from SCRIPT.HUMAN import Basic


class Ono(Basic):
    __slots__ = ('power')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((24, 0, 12, 26)), locate, 192, color_dict[1], *group)

        th.power = True

    def free(th):
        if th.torrent < 8:
            for i in range(0 + th.timer * 6, 360 + th.timer * 6, 180):
                for j in range(0 + th.timer * 6, 360 + th.timer * 6, 90):
                    pos = (th.x + 32 * cos(radians(i)),th.y + 32 * sin(radians(i)))

                    Barrage.Barrage(effective, 2, 3.5, th.color, j, pos, barrage_cache[(2, th.color)], th.group, True, False)

            th.torrent += 1

    def extend(th):
        speed = 5
        delay = 0

        if th.timer == 0:
            for _ in range(8):
                for j in range(-30, 31, 30):
                    delay += 20

                    for k in (j - 180, j, 180 - delay):
                        two_point = add(th.locate, (-th.x, -th.y))
                        atan2_ = atan2(-two_point[0], -two_point[1])
                        angle = degrees(atan2_) + k

                        Barrage.Barrage(effective, 2, speed, th.color, angle, (th.x, th.y), barrage_cache[(2, th.color)], th.group, True, False)

                speed -= 0.5

    def final(th):
        if th.torrent < 32:
            two_point = add(th.locate, (-th.x, -th.y))
            atan2_ = atan2(-two_point[0], -two_point[1])
            angle = degrees(atan2_) + 180

            for i in (2, 1, -1):
                Barrage.Barrage(effective, 2, 4, th.color, ((th.timer * 12) * i) + angle, (th.x, th.y), barrage_cache[(2, th.color)], th.group, True, False)

            th.torrent += 1

    def fire(th):
        if th.timer == 0:
            for i in range(0, 360, 15):
                Barrage.Barrage(effective, 2, 4, th.color, i, (th.x, th.y), barrage_cache[(2, th.color)], th.group, True, False)

    def update(th):
        th.timer += 1

        if th.timer % 120 == 0:
            rands = randint(0, 360)
            th.target_pos = (292 + 50 * cos(radians(rands)), 110 + 50 * sin(radians(rands)))
            th.torrent = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = choice([th.fire] * 5 + [th.free, th.extend, th.final])
        if th.timer % 120 >= 99:
            if th.timer % 99 == 0: 
                for i in range(0, 360, 30):
                    pos = (th.x + 48 * cos(radians(i)), th.y + 48 * sin(radians(i)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Barrage.Barrage(effective, 2, 3, color_dict[6], angle, pos, barrage_cache[(2, color_dict[6])], th.particle_group, False, False)

            th.point = Barrage.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 4)[0]