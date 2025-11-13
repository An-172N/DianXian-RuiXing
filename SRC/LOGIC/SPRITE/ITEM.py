import random as rand

import DICT
from FRIEND import Base


class ItemMgr:
    def __init__(th, own):
        th.own = own

        th.spwn_ctr = 0
        th.bw_ctr = 150
        th.comb = 0

    def comb_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.comb <= 15:
                th.own.pln_mgr.sc += 2 ** th.comb

            th.comb = 0
            th.bw_ctr = 150
        else:
            if th.comb >= 16:
                th.own.pln_mgr.sc += 2 ** th.comb
                th.comb = 0

    def item_spwn(th, brc_pos):
        if rand.random() <= 0.08:
            spr = Base((9, 9, 2), DICT.clr_dict[5], 1, 1)
            spr.spd = -2
            spr.rect.center = brc_pos
            th.own.item_grp.add(spr)
            th.own.blt_mgr.ttl_spwn_spt += 1
        elif rand.random() <= 0.01:
            spr = Base((9, 9, 2), DICT.clr_dict[2], 1, 2)
            spr.spd = -2
            spr.rect.center = brc_pos
            th.own.item_grp.add(spr)
            th.own.blt_mgr.ttl_spwn_spt += 1
    
    def item_coll(th, src, _):
        th.comb += 1
        th.bw_ctr = 150
        th.own.blt_mgr.ttl_spt += 1
        th.own.blt_mgr.stg_ttl_spt += 1

        if (src.type == 1 and
            th.own.blt_mgr.spt < 32):
            th.own.blt_mgr.spt += 1
        elif src.type == 2:
            th.own.pln_mgr.plyr += 1
            
        src.kill()

    def cal_spt(th):
        try:
            return f"{th.own.blt_mgr.stg_ttl_spt / th.own.blt_mgr.ttl_spwn_spt * 100:.2f} %"
        except ZeroDivisionError:
            return "0.00 %"