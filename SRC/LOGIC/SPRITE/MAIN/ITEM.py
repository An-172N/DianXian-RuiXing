import random as rand

import BRICK


class ItemMgr:
    def __init__(th, own):
        th.own = own

        th.spwn_ctr = 0
        th.bw_ctr = 90

        th.comb = 0

    def item_spwn(th, clr, item, pos):
        item = BRICK.BaseShape(9, 9, 2,
                               clr, 1,
                               item)

        item.rect.center = pos
        item.spd = -2

        th.own.item_grp.add(item)
        
    def spwn_rglr(th):
        th.spwn_ctr += 1

        if th.spwn_ctr >= 75:
            th.item_spwn(th.own.clr_dict[6],
                         0,
                         (rand.randint(120, 457), 0))
            th.spwn_ctr = 0

    def comb_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.comb <= 15:
                th.own.sc_mgr.sc_cnt += th.own.sc_mgr.pt()

            th.comb = 0
            th.bw_ctr = 90
        else:
            if th.comb >= 16:
                th.own.sc_mgr.sc_cnt += th.own.sc_mgr.pt()
                th.comb = 0
    
    def item_coll(th, src, _):
        th.comb += 1
        th.bw_ctr = 90

        if not th.own.blt_mgr.is_cnt_fusil:
            th.own.blt_mgr.spwn_blts()
        elif th.own.blt_mgr.fusil_cnt <= 2:
            th.own.blt_mgr.fusil_cnt += 1

        if (src.type == 1 and
            th.own.pln_mgr.s_pt < 48):
            th.own.pln_mgr.s_pt += 1

            th.own.pln_mgr.ttl_s_pt += 1
        elif src.type == 2:
            th.own.pln_mgr.plyr += 1