import pygame as pyg

import DICT
from ..BASE import Base


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

    def free(th):
        th.ctr += 1

        if (th.ctr >= 60 and
            th.ctr % 1 == 0 and
            th.bomb_cnt < 6):
            for i in range(120, 466, 15):
                spr = Base((15, 15, 0), (45, 194, 229), 1, "blt")
                if not hasattr(spr, "dmg"):
                    spr.dmg = 6
                spr.spd = -24
                spr.rect.center = (i, 0)
                th.char.pln_mgr.own.blt_grp.add(spr)

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
            spr = Base((2, 15, 0), (45, 194, 229), 1, "blt")
            if not hasattr(spr, "dmg"):
                spr.dmg = 4
            spr.spd = 16
            spr.rect.center = (blt_info['x'], blt_info['y'])
            spr.curr_ang = blt_info['ang']
            th.char.pln_mgr.own.blt_grp.add(spr)