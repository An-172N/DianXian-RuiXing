import random as rand

import DICT
from FUNC import Spawn
from FUNC import Base


class ItemMgr:
    def __init__(th, own):
        th.own = own

        th.spwn_ctr = 0
        th.bw_ctr = 120
        th.comb = 0

        th.spr = Base

    def comb_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.comb <= 15:
                th.own.pln_mgr.sc += 2 ** th.comb

            th.comb = 0
            th.bw_ctr = 120
        else:
            if th.comb >= 16:
                th.own.pln_mgr.sc += 2 ** th.comb
                th.comb = 0

    def item_spwn(th, brc_pos):
        if rand.random() <= 0.24:
            clr = DICT.clr_dict[5]
            Spawn.spwn_spr(th.spr, None,
                           th.own.item_grp,
                           brc_pos, (-2, -2, 0, 0),
                           (9, 9), 2, clr, 1, 1)
        elif rand.random() <= 0.01:
            clr = DICT.clr_dict[3]
            Spawn.spwn_spr(th.spr, None,
                           th.own.item_grp,
                           brc_pos, (-2, -2, 0, 0),
                           (9, 9), 2, clr, 1, 2)
    
    def item_coll(th, src, _):
        th.comb += 1
        th.bw_ctr = 90
        th.own.blt_mgr.ttl_spt += 1

        if (src.type == 1 and
            th.own.blt_mgr.spt < 48):
            th.own.blt_mgr.spt += 1
        elif src.type == 2:
            th.own.pln_mgr.plyr += 1
            
        src.kill()