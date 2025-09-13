import random as rand

from BRICK.BASE.BASESHAPE import BaseShape

from LOGIC.PROCESS.MOVE import mv


class RectRainer:
    def __init__(th, m_own):
        th.m_own = m_own

        th.cnt = 0
        th.ctr = 0

    def spwn_rect(th):
        th.ctr += 1

        if (th.ctr >= 60
            and th.ctr % 2 == 0
            and th.cnt <= 4):
            th.cnt += 1

            for i in range(120, 466, 15):
                blt = BaseShape(15, 15, 0,
                                (45, 194, 229), 1, "bomb")

                blt.spd = -24
                blt.damage = 6

                blt.rect.center = (i, 0)

                th.m_own.blt_grp.add(blt)

    def upd_rect(th):
        for blt in th.m_own.blt_grp:
            if blt.type == "bomb":
                mv(blt, blt.spd)

    def rst_bomb(th):
        th.cnt = 0
        th.ctr = 0