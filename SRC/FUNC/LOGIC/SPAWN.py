import random as rand

from ..LOGIC import MOVE


def spwn_spr(spr, tar, spr_grp, pos, spd, dmg, ang, *args):
    curr_spr = spr(*args)

    curr_spr.rect.center = pos
    if tar:
        curr_spr.curr_ang = MOVE.ang(tar, curr_spr) + ang
    else:
        curr_spr.curr_ang = ang
    curr_spr.spd = rand.randint(spd[0], spd[1])
    if not hasattr(curr_spr, "dmg"):
        curr_spr.dmg = dmg

    spr_grp.add(curr_spr)


def shhm_spwn(spr, spr_grp, pos):
    spr.rect.center = pos
    spr_grp.add(spr)