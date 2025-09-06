import random as rand

from BRICKS.BASESHAPE import BaseShape

from TOOLS.ANGLE import angle
from TOOLS.ROTATE import rot
from TOOLS.MOVE import mv


class BarrageManager:
    def __init__(th, own):
        th.own = own

    def spwn_brg(th, spr):
        if rand.random() <= 0.16:
            if rand.choice([0, 1, 2, 3]) == 0:
                brg = BaseShape(9.5, 9.5, 0,
                                spr.clr, spr.shape)

                brg.rect.center = spr.rect.center

                brg.curr_ang = angle(th.own.pln_mgr.char, brg)
                brg.spd = 2

                th.own.brg_grp.add(brg)
            else:
                for i in range(-30, 31, 30):
                    brg = BaseShape(9.5, 9.5, 0,
                                    spr.clr, spr.shape)

                    brg.rect.center = spr.rect.center

                    brg.curr_ang = angle(th.own.pln_mgr.char, brg) + i
                    brg.spd = 2

                    th.own.brg_grp.add(brg)

    def upd(th):
        for brg in th.own.brg_grp:
            rot(brg)
            mv(brg, brg.spd)