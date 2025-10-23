import pygame as pyg

import DICT
from FUNC import Base
from FUNC import Spawn


class Kli(pyg.sprite.Sprite):
    def __init__(th, own):
        super().__init__()
        th.pln_mgr = own

        th.clr = DICT.clr_dict[5]

        th.bomb = RectRaining(th)

        th.orig_image = pyg.image.load('AST\IMG_KLI.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

    def update(th):
        th.pln_mgr.turn_side()
        th.pln_mgr.mv_pln()

        th.pln_mgr.invinc()


class RectRaining:
    def __init__(th, own):
        th.char = own

        th.bomb_cnt = 0
        th.ctr = 0

        th.spr = Base

    def free(th):
        th.ctr += 1

        if (th.ctr >= 60 and
            th.ctr % 1 == 0 and
            th.bomb_cnt < 6):
            for i in range(120, 466, 15):
                Spawn.spwn_spr(th.spr, None,
                               th.char.pln_mgr.own.blt_grp,
                               (i, 0), (-24, -24, 6, 0),
                               (15, 15), 0, (45, 194, 229), 1)

            th.bomb_cnt += 1

    def fire(th, dx, dy, ang):
        blt_type = [
            {'x': th.char.rect.left - dx,
             'y': th.char.rect.top + dy,
             'ang': ang},
            {'x': th.char.rect.right + dx,
             'y': th.char.rect.top + dy,
             'ang': -ang}
        ]

        for blt_info in blt_type:
            Spawn.spwn_spr(th.spr, None,
                           th.char.pln_mgr.own.blt_grp,
                           (blt_info['x'], blt_info['y']), (16, 16, 4, blt_info['ang']),
                           (2, 15), 0, (45, 194, 229), 1)