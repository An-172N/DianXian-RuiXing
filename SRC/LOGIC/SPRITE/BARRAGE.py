import random as rand

from BRICK.BASE.BASESHAPE import BaseShape

from LOGIC.PROCESS.MOVE import ang
from LOGIC.PROCESS.MOVE import rot
from LOGIC.PROCESS.MOVE import mv


class Barrage:
    def __init__(th, own):
        th.own = own

    def spwn_brg(th, spr):
        if rand.random() <= 0.32:
            if rand.choice([0, 1, 2, 3]) == 0:
                brg = BaseShape(9, 9, 0,
                                spr.clr, spr.shape)

                brg.rect.center = spr.rect.center

                brg.curr_ang = ang(th.own.pln_mgr.char, brg)
                brg.spd = 2

                th.own.brg_grp.add(brg)
            else:
                for i in range(-30, 31, 30):
                    brg = BaseShape(9, 9, 0,
                                    spr.clr, spr.shape)

                    brg.rect.center = spr.rect.center

                    brg.curr_ang = ang(th.own.pln_mgr.char, brg) + i
                    brg.spd = 2

                    th.own.brg_grp.add(brg)

    def upd(th):
        for brg in th.own.brg_grp:
            rot(brg)
            mv(brg, brg.spd)