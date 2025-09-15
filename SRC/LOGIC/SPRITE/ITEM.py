import random as rand

from BRICK.BASE.BASESHAPE import BaseShape

from LOGIC.PROCESS.MOVE import grav


class Item:
    def __init__(th, own):
        th.own = own

        th.spwn_ctr = 0
        th.comb = 0
        th.bw_ctr = 90

    def item_spwn(th, item, clr, pos=(0, 0)):
        th.own.item_grp.add(BaseShape(9, 9, 2,
                                      clr, 1, item,
                                      pos))
        
    def spwn_regular(th):
        th.spwn_ctr += 1

        if th.spwn_ctr >= 75:
            th.item_spwn(0,
                         (255, 255, 255),
                         (rand.randint(120, 457), 0))
            th.spwn_ctr = 0

    def comb_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.comb <= 15:
                th.own.sc_mgr.pts()

            th.comb = 0
            th.bw_ctr = 90
        elif th.comb >= 16:
            th.own.sc_mgr.pts()
            th.comb = 0

    def item_upd(th):
        [grav(item, 2) for item in th.own.item_grp]