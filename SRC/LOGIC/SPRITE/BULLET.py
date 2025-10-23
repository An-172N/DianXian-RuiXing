import random as rand

import DICT
from FUNC import Spawn
from FUNC import Base


class BulletMgr:
    def __init__(th, own):
        th.own = own

        th.spt = 16
        th.ttl_spt = 0

        th.spr = Base

    def spwn_blt(th):
        p = 2 ** (th.spt // 32)
        q = 2 ** (th.spt // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                th.own.pln_mgr.char.bomb.fire(0 + i * 10, 0 + i * 12,
                                              j)

        char = th.own.pln_mgr.char
        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 45):
            Spawn.spwn_spr(th.spr, None,
                           th.own.ptcl_grp,
                           char.rect.center, (6, 10, 0, i),
                           (2, 2), 0, char.clr, 1)

    def single_bomb(th):
        if (not th.own.pln_mgr.is_sdivide and
            th.spt >= 8):
            th.spt -= 8
            th.own.pln_mgr.is_sdivide = True

    def use_bomb(th):
        if th.own.pln_mgr.is_sdivide:
            th.own.pln_mgr.char.bomb.free()

    def blt_coll(th, src, tar):
        tar.hp -= src.dmg
        th.own.pln_mgr.sc += 64

        if tar.hp <= 0:
            tar_pos = (tar.rect.centerx, tar.rect.centery)

            if hasattr(tar, "bomb"):
                th.own.stg_mgr.shhm_lose()

            rands = rand.randint(0, 45)
            for i in range(0 + rands, 360 + rands, 45):
                Spawn.spwn_spr(th.spr, None,
                               th.own.ptcl_grp,
                               tar_pos, (6, 10, 0, i),
                               (2, 2), 0, tar.clr, 1)
            
            th.own.item_mgr.item_spwn(tar_pos)
            th.brc_death(tar, tar_pos)
            
            tar.kill()

        src.kill()

    def brc_death(th, brc, brc_pos):
        if brc.clr == DICT.clr_dict[6]:
            proc_dict = {
                0: polygon_brc,
                1: rect_brc,
                2: circle_brc,
                3: point_brc,
                4: line_brc
            }

            proc_dict[brc.shape](th.spr, brc,
                                 th.own.blt_grp,
                                 16)

        if rand.random() <= 0.32:
            tupl = rand.choice([(0, 1, 1), (-30, 31, 30)])
            for i in range(tupl[0], tupl[1], tupl[2]):
                Spawn.spwn_spr(th.spr, th.own.pln_mgr.char,
                               th.own.brg_grp,
                               brc_pos, (2, 2, 0, i),
                               (9, 9), 0, brc.clr, brc.shape)
                

def circle_brc(spr, src, spr_grp, spd):
    rands = rand.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        Spawn.spwn_spr(spr, None,
                       spr_grp,
                       src.rect.center, (spd, spd, 4, i),
                       (2, 15), 0, (45, 194, 229), 1, "blt")


def rect_brc(spr, src, spr_grp, spd):
    blt_index = [
        {'ang': 0,
         'pos': src.rect.midleft},
        {'ang': 90,
         'pos': src.rect.midbottom},
        {'ang': 180,
         'pos': src.rect.midright},
        {'ang': 270,
         'pos': src.rect.midtop}
    ]
    
    for blt_info in blt_index:
        Spawn.spwn_spr(spr, None,
                       spr_grp,
                       blt_info['pos'], (spd, spd, 4, blt_info['ang']),
                       (2, 15), 0, (45, 194, 229), 1, "blt-cros")


def polygon_brc(spr, src, spr_grp, spd):
    blt_index = [
        {'ang': rand.choice([-30, -210]),
         'pos': src.rect.midleft,},
        {'ang': rand.choice([30, 210]),
         'pos': src.rect.midright},
        {'ang': rand.choice([90, 270]),
         'pos': src.rect.midbottom}
    ]

    for blt_info in blt_index:
        Spawn.spwn_spr(spr, None,
                       spr_grp,
                       blt_info['pos'], (spd, spd, 4, blt_info['ang']),
                       (2, 15), 0, (45, 194, 229), 1, "blt-cros")


def line_brc(spr, src, spr_grp, spd):
    for i in range(-90, 91, 15):
        Spawn.spwn_spr(spr, None,
                       spr_grp,
                       src.rect.center, (spd, spd, 8, i),
                       (2, 15), 0, (45, 194, 229), 1, "blt")


def point_brc(spr, _, spr_grp, spd):
    pos = (rand.randint(120, 465), rand.randint(15, 345))

    for _ in range(12):
        Spawn.spwn_spr(spr, None,
                       spr_grp,
                       pos, (spd, spd, 4, rand.randint(0, 360)),
                       (2, 15), 0, (45, 194, 229), 1, "blt")