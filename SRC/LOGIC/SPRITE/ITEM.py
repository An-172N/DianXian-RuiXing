import random as rand

from FUNC import Spawn
from FUNC import BaseShape


class ItemMgr:
    def __init__(th, proc):
        th.proc = proc

        th.spwn_ctr = 0
        th.bw_ctr = 120
        th.comb = 0

        th.spr = BaseShape

    def comb_ctr(th):
        th.bw_ctr -= 1

        if th.bw_ctr <= 0:
            if 0 < th.comb <= 15:
                th.proc("add", "pln", "sc",
                        2 ** th.comb)

            th.comb = 0
            th.bw_ctr = 120
        else:
            if th.comb >= 16:
                th.proc("add", "pln", "sc",
                        2 ** th.comb)
                th.comb = 0

    def item_spwn(th, brc_pos):
        if rand.random() <= 0.24:
            clr = th.proc("get", "main", "clr")[5]
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "item_grp"),
                           brc_pos, (-2, -2), 0, 0,
                           (9, 9), 2, clr, 1, 1)
        elif rand.random() <= 0.004:
            clr = th.proc("get", "main", "clr")[3]
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "item_grp"),
                           brc_pos, (-2, -2), 0, 0,
                           (9, 9), 2, clr, 1, 2)
    
    def item_coll(th, src, _):
        th.comb += 1
        th.bw_ctr = 90

        if (src.type == 1 and
            th.proc("get", "pln", "spt") < 48):
            th.proc("add", "pln", "ttl_spt",
                    1)
            th.proc("add", "pln", "spt",
                    1)
        elif src.type == 2:
            th.proc("add", "pln", "plyr",
                    1)
            
        src.kill()