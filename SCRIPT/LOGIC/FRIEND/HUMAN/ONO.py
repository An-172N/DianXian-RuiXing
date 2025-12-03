import random as rand
import math

import pygame as pyg

import SCRIPT.DICT
import SCRIPT.VARIABLE
from ..BASE import Base


class Ono(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 384
        th.clr = SCRIPT.DICT.clr_dict[1]
        th.shape = 2
        th.curr_ang = 0

        th.bomb = AutFroDiffuse(th.clr)

        th.orig_image = pyg.image.load('ASSET\IMG_ONO.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False

        th.tar_x = 292
        th.tar_y = 60
        th.ctr = 0

    def update(th):
        th.ctr += 1

        if th.ctr % 120 == 0:
            th.tar_x = rand.choice([150, 220, 292, 365, 435])

            th.bomb.bomb_cnt = 0
            th.bomb.bullet_cnt = 0
            th.bomb.dl = 0
            th.is_free = not th.is_free

        dir = pyg.math.Vector2(th.tar_x - th.rect.centerx, 0)
        current_pos = pyg.math.Vector2(th.rect.centerx, th.rect.centery)
        target_pos = pyg.math.Vector2(th.tar_x, 60)

        delta_vec = target_pos - current_pos
        distance = delta_vec.length()

        if distance < 4:
            th.rect.center = target_pos
        else:
            if distance > 0:
                dir.normalize_ip()

            new_pos = current_pos + dir * 4
            th.rect.center = new_pos

        if not th.is_free:
            th.bomb.fire(th.rect)
        else:
            th.bomb.free(th.rect)


class AutFroDiffuse:
    def __init__(th, clr):
        th.clr = clr

        th.bomb_cnt = 0
        th.bullet_cnt = 0
        th.ctr = 0
        th.dl = 0

    def free(th, rect):
        th.ctr += 1

        if (th.ctr % 1 == 0 and
            th.bomb_cnt < 12):
            th.dl += 6

            for i in range(0 + th.dl, 360 + th.dl, 120):
                for j in range(0 + th.dl, 360 + th.dl, 90):
                    pos = (rect.centerx
                           + 32 * math.cos(math.radians(i)),
                           rect.centery
                           + 32 * math.sin(math.radians(i)))

                    spr = Base((9, 9, 0), th.clr, 2)
                    spr.spd = 4
                    spr.rect.center = pos
                    spr.curr_ang = j
                    SCRIPT.VARIABLE.brg_grp.add(spr)

            th.bomb_cnt += 1

    def fire(th, rect):
        if th.bullet_cnt < 1:
            pos = rect.center
            for i in range(0, 360, 15):
                spr = Base((9, 9, 0), th.clr, 2)
                spr.spd = 4
                spr.rect.center = pos
                spr.curr_ang = i
                SCRIPT.VARIABLE.brg_grp.add(spr)

            th.bullet_cnt += 1