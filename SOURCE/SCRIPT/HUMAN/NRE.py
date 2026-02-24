# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, uniform
from math import degrees, atan2


import pygame as pg


from PRELOAD import char_image, effective, color_dict, particle_cache
from SCRIPT.SPRITE import Line, Barrage
from LOGIC.PLANE import vector
from LOGIC.CALCULATE import add, round_angle
from LOGIC.DRAW import rectangle
from SCRIPT.HUMAN import Basic


class Nre(Basic):
    __slots__ = ('power')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((48, 0, 12, 26)), locate, 256, color_dict[3], *group)

        th.power = True

    def free(th):
        if th.torrent < 12:
            start_pos = (randint(120, 465), 15)
            end_pos = (-randint(120, 465), -360)
            delta_pos = add(end_pos, start_pos)
            pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
            angle = round_angle(degrees(atan2(-delta_pos[0], -delta_pos[1])))

            Line.Line((3, 500), 0, angle, pos, color_dict[6], color_dict[3], th.group, True)

            th.torrent += 1

    def extend(th):
        if th.torrent < 8 and th.timer % 3 == 0:
            for j in (1, -1):
                start_pos = (th.interval_locate[0] + th.torrent * j * 24, 15)
                end_pos = (-(th.interval_locate[0] + th.torrent * j * 24), -360)
                delta_pos = add(end_pos, start_pos)
                pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)

                Line.Line((3, 500), 0, 0, pos, color_dict[6], color_dict[3], th.group, True)

            if th.torrent < 1:
                for k in range(8):
                    start_pos = (120, (th.locate[1] - 13) - k * 24)
                    end_pos = (-465, -((th.locate[1] - 13) - k * 24))
                    delta_pos = add(end_pos, start_pos)
                    pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
                    angle = round_angle(degrees(atan2(-delta_pos[0], -delta_pos[1])))

                    Line.Line((3, 500), 0, angle, pos, color_dict[6], color_dict[3], th.group, True)

            th.torrent += 1

    def fire(th):
        if th.timer == 0:
            for i in range(th.locate[0] - 30, th.locate[0] + 31, 20):
                start_pos = (i, 15)
                end_pos = (-i, -360)
                delta_pos = add(end_pos, start_pos)
                pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)

                Line.Line((3, 500), 0, 0, pos, color_dict[6], color_dict[3], th.group, True)

    def update(th):
        th.timer += 1

        if th.timer % 100 == 0:
            th.target_pos = (choice((150, 220, 292, 365, 435)), 60)
            th.torrent = 0
            th.timer = 0
            th.interval_locate = th.locate
            th.can_shoot = True
            th.choice = choice([th.fire] * 5 + [th.free] * 3 + [th.extend] * 2)
        if th.timer % 100 >= 82:
            if th.timer % 82 == 0:
                for _ in range(8):
                    pos = (int(uniform(th.x - 48, th.x + 48)), th.y)
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Barrage.Barrage(effective, None, 3, color_dict[6], angle, pos, particle_cache[((9, 9), color_dict[6])], th.particle_group, False)

            th.point = Barrage.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 6)[0]