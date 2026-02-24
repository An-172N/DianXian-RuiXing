# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, uniform
from math import degrees, atan2


import pygame as pg


from PRELOAD import char_image, effective, color_dict, barrage_cache
from SCRIPT.SPRITE import Barrage
from LOGIC.CALCULATE import add
from LOGIC.DRAW import rectangle
from SCRIPT.HUMAN import Basic


class Qdi(Basic):
    __slots__ = ('power')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((60, 0, 12, 26)), locate, 96, color_dict[4], *group)

        th.power = True

    def free(th):
        if th.timer == 0:
            for _ in range(48):
                angle = randint(0, 360)
                pos = (randint(120, 465), randint(15, 225))

                Barrage.Barrage(effective, 2, 4, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, True, False)

    def final(th):
        if th.timer == 0:
            pos = (randint(120, 465), randint(15, 170))

            for _ in range(10):
                rands = randint(0, 30)

                for i in range(0 + rands, 360 + rands, 30):
                    Barrage.Barrage(effective, 2, randint(2, 5), th.color, i, pos, barrage_cache[(2, th.color)], th.group, True, False)

    def extend(th):
        if th.timer == 0:
            for _ in range(8):
                pos = (randint(120, 465), randint(15, 200))

                for j in range(0, 360, 30):
                    Barrage.Barrage(effective, 2, randint(2, 5), th.color, j, pos, barrage_cache[(2, th.color)], th.group, True, False)

    def fire(th):
        if th.torrent < 6 and th.timer % 2 == 0:
            pos = (randint(120, 465), randint(15, 230))
            two_point = add(th.locate, (-pos[0], -pos[1]))
            angle = degrees(atan2(-two_point[0], -two_point[1]))

            Barrage.Barrage(effective, 2, 3.5, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, True, False)

            th.torrent += 1

    def update(th):
        th.timer += 1

        if th.timer % 150 == 0:
            th.x, th.y = (randint(150, 435), randint(48, 96))
            th.torrent = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = choice([th.fire] * 8 + [th.free] * 2 + [th.extend, th.final])
        if th.timer % 150 >= 125:
            if th.timer % 150 >= 145:
                th.x += choice([-4, 4])
            if th.timer % 125 == 0:
                for _ in range(12):
                    pos = (int(uniform(th.x - 48, th.x + 48)), int(uniform(th.y - 64, th.y + 64)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Barrage.Barrage(effective, 2, 3, color_dict[6], angle, pos, barrage_cache[(2, color_dict[6])], th.particle_group, False, False)

                th.point = Barrage.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()