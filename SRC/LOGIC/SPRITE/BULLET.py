import random as rand
import math

import DICT
import FUNC
from FRIEND import Base


class BulletMgr:
    def __init__(th, own):
        th.own = own

        th.spt = 16
        th.ttl_spt = 0
        th.stg_ttl_spt = 0
        th.ttl_spwn_spt = 0

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
            spr = Base((2, 2, 0), char.clr, 1)
            spr.spd = rand.randint(6, 10)
            spr.rect.center = char.rect.center
            spr.curr_ang = i
            th.own.ptcl_grp.add(spr)

    def single_bomb(th):
        if (not th.own.pln_mgr.is_sdivide and
            th.spt >= 8):
            th.spt -= 8
            th.own.pln_mgr.is_sdivide = True

    def use_bomb(th):
        if th.own.pln_mgr.is_sdivide:
            th.own.pln_mgr.char.bomb.free()

    def blt_coll(th, src, tar):
        if src.type == "blt":
            if getattr(tar, 'is_dying', False):
                src.kill()
                return

        tar.hp -= src.dmg
        th.own.pln_mgr.sc += 64

        if tar.hp <= 0:
            tar.is_dying = True
            tar_pos = (tar.rect.centerx, tar.rect.centery)

            if hasattr(tar, "bomb"):
                th.own.stg_mgr.shhm_lose()

            rands = rand.randint(0, 45)
            for i in range(0 + rands, 360 + rands, 45):
                spr = Base((2, 2, 0), tar.clr, 1)
                spr.spd = rand.randint(6, 10)
                spr.rect.center = tar_pos
                spr.curr_ang = i
                th.own.ptcl_grp.add(spr)
            
            th.own.item_mgr.item_spwn(tar_pos)
            th.brc_death(tar, tar_pos)
            
            tar.kill()

        if src.type == "blt":
            src.kill()

    def brc_death(th, brc, brc_pos):
        if brc.clr == DICT.clr_dict[6]:
            proc_dict = {
                0: polygon_brc,
                1: line_brc,
                2: circle_brc
            }

            proc_dict[brc.shape](Base, brc,
                                 th.own.blt_grp,
                                 16)

        difficulty = FUNC.Calculate.generalized_fibonacci(1, 2, th.own.stg_mgr.stg + 1) / 100
        if rand.random() <= 0.32 + difficulty:
            tupl = rand.choice([(0, 1, 1), (-30, 31, 30)])
            char = th.own.pln_mgr.char
            for i in range(tupl[0], tupl[1], tupl[2]):
                spr = Base((9, 9, 0), brc.clr, brc.shape)
                spr.spd = 2
                spr.rect.center = brc_pos
                two_pt = FUNC.Calculate.delta_position(char.rect.center, spr.rect.center)
                spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1])) + i
                th.own.brg_grp.add(spr)


def circle_brc(spr, src, spr_grp, spd):
    rands = rand.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        curr_spr = spr((2, 15, 0), (45, 194, 229), 1, "blt")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 4
        curr_spr.spd = spd
        curr_spr.rect.center = src.rect.center
        curr_spr.curr_ang = i
        spr_grp.add(curr_spr)


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
        curr_spr = spr((2, 15, 0), (45, 194, 229), 1, "blt-cros")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 4
        curr_spr.spd = spd
        curr_spr.rect.center = blt_info['pos']
        curr_spr.curr_ang = blt_info['ang']
        spr_grp.add(curr_spr)


def line_brc(spr, src, spr_grp, spd):
    for _ in range(12):
        curr_spr = spr((2, rand.randint(15, 75), 0), (45, 194, 229), 1, "blt")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 6
        curr_spr.spd = spd
        curr_spr.rect.center = src.rect.center
        curr_spr.curr_ang = rand.randint(0, 360)
        spr_grp.add(curr_spr)