import random as rand

import BRICK


class ItemMgr:
    def __init__(th, proc):
        th.proc = proc

        th.spwn_ctr = 0
        th.bw_ctr = 90

        th.comb = 0

    def item_spwn(th, clr, item, pos):
        item = BRICK.BaseShape(9, 9, 2,
                               clr, 1,
                               item)

        item.rect.center = pos
        item.spd = -2

        th.proc("get", "main", "item_grp").add(item)
        
    def spwn_rglr(th):
        th.spwn_ctr += 1

        if th.spwn_ctr >= 75:
            th.item_spwn(th.proc("get", "main", "clr")[6],
                         0,
                         (rand.randint(120, 457), 0))
            th.spwn_ctr = 0

    def comb_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.comb <= 15:
                th.proc("add", "pln", "sc",
                        2 ** th.proc("get", "item", "comb"))

            th.comb = 0
            th.bw_ctr = 90
        else:
            if th.comb >= 16:
                th.proc("add", "pln", "sc",
                        2 ** th.proc("get", "item", "comb"))
                th.comb = 0
    
    def item_coll(th, src, _):
        th.comb += 1
        th.bw_ctr = 90

        if not th.proc("get", "blt", "is_fusil"):
            th.proc("func", "blt", "blt")()
        elif th.proc("get", "blt", "fusil_cnt") <= 2:
            th.proc("add", "blt", "fusil_cnt",
                    1)

        if (src.type == 1 and
            th.proc("get", "pln", "spt") < 48):
            th.proc("add", "pln", "ttl_spt",
                    1)
            th.proc("add", "pln", "spt",
                    1)
        elif src.type == 2:
            th.proc("add", "pln", "plyr",
                    1)