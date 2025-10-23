import random as rand

from ..LOGIC import MOVE


def spwn_spr(spr, tar, spr_grp, pos, val, *args):
    curr_spr = spr(*args)

    curr_spr.rect.center = pos
    if tar:
        curr_spr.curr_ang = MOVE.ang(tar, curr_spr) + val[3]
    else:
        curr_spr.curr_ang = val[3]
    curr_spr.spd = rand.randint(val[0], val[1])
    if not hasattr(curr_spr, "dmg"):
        curr_spr.dmg = val[2]

    spr_grp.add(curr_spr)


def shhm_spwn(spr, spr_grp, pos):
    spr.rect.center = pos
    spr_grp.add(spr)