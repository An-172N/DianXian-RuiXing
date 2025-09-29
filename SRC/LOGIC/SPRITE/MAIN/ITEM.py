import random as rand

from BRICK.BASE.ITEM import Item


class ItemMgr:
    def __init__(th, own):
        th.own = own

        th.spwn_ctr = 0
        th.bw_ctr = 90

        th.item_cnt = 0
        th.coll_item_cnt = 0
        th.comb = 0

    def item_spwn(th, clr, item, pos):
        th.own.item_grp.add(Item(clr,
                                 item,
                                 pos))
        
    def spwn_rglr(th):
        th.spwn_ctr += 1

        if th.spwn_ctr >= 75:
            th.item_spwn((255, 255, 255),
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

    def cnt_item_coll(th):
        per = th.coll_item_cnt / th.item_cnt

        return f"{(per) * 100:.2f} %"