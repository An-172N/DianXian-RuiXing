import random as rand

from BRICKS.BASESHAPE import BaseShape

from TOOLS.MOVE import mv


class RectRainer:
    def __init__(th, m_own):
        th.m_own = m_own

        th.cnt = 0
        th.ctr = 0
        th.spwn_ctr = 0

    def spwn_rect(th):
        th.spwn_ctr += 1
        th.ctr += 1

        if (th.spwn_ctr >= 1
            and th.ctr >= 60 and th.cnt <= 48):
            th.cnt += 1
            blt = BaseShape(14, 14, 0,
                            (45, 194, 229), 1, "bomb")

            blt.curr_ang = 0
            blt.spd = -24
            blt.damage = 8

            blt.rect.center = (rand.randint(120, 465), 0)

            th.m_own.blt_grp.add(blt)

            th.spwn_ctr = 0

    def upd_rect(th):
        for blt in th.m_own.blt_grp:
            if blt.type == "bomb":
                mv(blt, blt.spd)

    def rst_bomb(th):
        th.cnt = 0
        th.ctr = 0
        th.spwn_ctr = 0

    def lgc(th):
        th.spwn_rect()
        th.upd_rect()