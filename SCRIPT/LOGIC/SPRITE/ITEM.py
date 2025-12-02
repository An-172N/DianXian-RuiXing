import random as rand

import FUNC
import SCRIPT.DICT
import SCRIPT.VARIABLE
from SCRIPT.LOGIC.FRIEND import Base


def comb_ctr():
    SCRIPT.VARIABLE.bw_ctr -= 1

    if SCRIPT.VARIABLE.bw_ctr <= 0:
        if 0 < SCRIPT.VARIABLE.comb <= 15:
            SCRIPT.VARIABLE.sc += 2 ** SCRIPT.VARIABLE.comb

        SCRIPT.VARIABLE.comb = 0
        SCRIPT.VARIABLE.bw_ctr = 150
    else:
        if SCRIPT.VARIABLE.comb >= 16:
            SCRIPT.VARIABLE.sc += 2 ** SCRIPT.VARIABLE.comb
            SCRIPT.VARIABLE.comb = 0


def item_spwn(brc_pos):
    if rand.random() <= 0.125:
        spr = Base((9, 9, 2), SCRIPT.DICT.clr_dict[5], 1, 1)
        spr.spd = -2
        spr.rect.center = brc_pos
        SCRIPT.VARIABLE.item_grp.add(spr)
        SCRIPT.VARIABLE.ttl_spwn_spt += 1
    elif rand.random() <= 0.007:
        spr = Base((9, 9, 2), SCRIPT.DICT.clr_dict[2], 1, 2)
        spr.spd = -2
        spr.rect.center = brc_pos
        SCRIPT.VARIABLE.item_grp.add(spr)
        SCRIPT.VARIABLE.ttl_spwn_spt += 1


def item_coll(src, _):
    SCRIPT.VARIABLE.comb += 1
    SCRIPT.VARIABLE.bw_ctr = 150
    SCRIPT.VARIABLE.ttl_spt += 1
    SCRIPT.VARIABLE.stg_ttl_spt += 1

    if (src.type == 1 and
        SCRIPT.VARIABLE.spt < 32):
        SCRIPT.VARIABLE.spt += 1
    elif src.type == 2:
        SCRIPT.VARIABLE.player += 1
        
    src.kill()


def cal_spt():
    return f"{FUNC.Calculate.divide(SCRIPT.VARIABLE.stg_ttl_spt, SCRIPT.VARIABLE.ttl_spwn_spt, 0) * 100:.2f} %"