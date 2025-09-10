import random as rand

from BRICK.BASE.BASESHAPE import BaseShape

from LOGIC.PROCESS.MOVE import grav


class Item:
    def __init__(th, own):
        th.own = own

        th.spwn_ctr = 0
        th.combo = 0
        th.bw_ctr = 90

    def item_spwn(th, dx, dy, item, clr):
        th.own.item_grp.add(BaseShape(9, 9, 2,
                                      clr, 1, item,
                                      x=dx, y=dy))
        
    def spwn_regular(th):
        th.spwn_ctr += 1

        if th.spwn_ctr >= 75:
            th.item_spwn(rand.randint(120, 457), 0,
                         0,
                         (255, 255, 255))
            th.spwn_ctr = 0

    def combo_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.combo <= 15:
                th.own.sc_mgr.pts()

            th.combo = 0
            th.bw_ctr = 90
        elif th.combo >= 16:
            th.own.sc_mgr.pts()
            th.combo = 0

    def item_upd(th):
        [grav(item, 0.1) for item in th.own.item_grp]