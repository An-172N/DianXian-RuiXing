import random as rand

import FUNC
import SCRIPT.DICT
import VARIABLE

from SCRIPT.LOGIC.FRIEND import Base


def comb_ctr() -> None:
    VARIABLE.bw_ctr -= 1

    if VARIABLE.bw_ctr <= 0:
        if 0 < VARIABLE.comb <= 15:
            VARIABLE.sc += 2 ** VARIABLE.comb

        VARIABLE.comb = 0
        VARIABLE.bw_ctr = 150
    else:
        if VARIABLE.comb >= 16:
            VARIABLE.sc += 2 ** VARIABLE.comb
            VARIABLE.comb = 0


def item_spwn(brc_pos) -> None:
    if rand.random() <= 0.125:
        spr = Base((9, 9, 2), SCRIPT.DICT.clr_dict[5], 1, 1)
        spr.spd = -2
        spr.rect.center = brc_pos
        VARIABLE.item_grp.add(spr)
        VARIABLE.ttl_spwn_s_power += 1
    elif rand.random() <= 0.007:
        spr = Base((9, 9, 2), SCRIPT.DICT.clr_dict[2], 1, 2)
        spr.spd = -2
        spr.rect.center = brc_pos
        VARIABLE.item_grp.add(spr)
        VARIABLE.ttl_spwn_s_power += 1


def item_coll(src, _) -> None:
    VARIABLE.comb += 1
    VARIABLE.bw_ctr = 150
    VARIABLE.ttl_s_power += 1
    VARIABLE.stg_ttl_s_power += 1

    if (src.type == 1 and
        VARIABLE.s_power < 32):
        VARIABLE.s_power += 1
    elif src.type == 2:
        VARIABLE.player += 1
        
    src.kill()


def cal_s_power() -> str:
    return f"{FUNC.Calculate.divide(VARIABLE.stg_ttl_s_power, VARIABLE.ttl_spwn_s_power, 0) * 100:.2f} %"