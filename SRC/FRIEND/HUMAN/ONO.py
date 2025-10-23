import random as rand
import math

import pygame as pyg

import DICT
from FUNC import Move
from FUNC import Base
from FUNC import Spawn


class Ono(pyg.sprite.Sprite):
    def __init__(th, own):
        super().__init__()
        th.stg_mgr = own

        th.hp = 128
        th.clr = DICT.clr_dict[1]
        th.shape = 2
        th.curr_ang = 0

        th.bomb = AutFroDiffuse(th)

        th.is_free = False

        th.orig_image = pyg.image.load('AST\IMG_ONO.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()

        th.tar_x = 292
        th.tar_y = 60
        th.ctr = 0

    def update(th):
        th.ctr += 1

        if th.ctr % 120 == 0:
            th.tar_x = rand.choice([150, 292, 435])

            th.bomb.bomb_cnt = 0
            th.bomb.dl = 0
            th.is_free = not th.is_free

        Move.vec(th, th.tar_x, 60, 4)

        if not th.is_free:
            th.bomb.fire()
        else:
            th.bomb.free()


class AutFroDiffuse:
    def __init__(th, own):
        th.char = own

        th.bomb_cnt = 0
        th.ctr = 0
        th.dl = 0

        th.spr = Base

    def free(th):
        th.ctr += 1

        if (th.ctr % 1 == 0 and
            th.bomb_cnt < 12):
            th.dl += 6

            for i in range(0 + th.dl, 360 + th.dl, 120):
                for j in range(0 + th.dl, 360 + th.dl, 90):
                    pos = (th.char.rect.centerx
                           + 32 * math.cos(math.radians(i)),
                           th.char.rect.centery
                           + 32 * math.sin(math.radians(i)))

                    Spawn.spwn_spr(th.spr, None,
                                   th.char.stg_mgr.own.brg_grp,
                                   pos, (4, 4, 0, j),
                                   (9, 9), 0, th.char.clr, 2)

            th.bomb_cnt += 1

    def fire(th):
        if th.bomb_cnt < 1:
            pos = th.char.rect.center
            for i in range(0, 360, 15):
                Spawn.spwn_spr(th.spr, None,
                               th.char.stg_mgr.own.brg_grp,
                               pos, (4, 4, 0, i),
                               (9, 9), 0, th.char.clr, 2)

            th.bomb_cnt += 1