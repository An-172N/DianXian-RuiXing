import random as rand

import FUNC
import SCRIPT.DICT
import SCRIPT.VARIABLE

from SCRIPT.LOGIC.FRIEND import Base


def comb_ctr() -> None:
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


def item_spwn(brc_pos) -> None:
    if rand.random() <= 0.125:
        spr = Base((9, 9, 2), SCRIPT.DICT.clr_dict[5], 1, 1)
        spr.spd = -2
        spr.rect.center = brc_pos
        SCRIPT.VARIABLE.item_grp.add(spr)
        SCRIPT.VARIABLE.ttl_spwn_s_power += 1
    elif rand.random() <= 0.007:
        spr = Base((9, 9, 2), SCRIPT.DICT.clr_dict[2], 1, 2)
        spr.spd = -2
        spr.rect.center = brc_pos
        SCRIPT.VARIABLE.item_grp.add(spr)
        SCRIPT.VARIABLE.ttl_spwn_s_power += 1


def item_coll(src, _) -> None:
    SCRIPT.VARIABLE.comb += 1
    SCRIPT.VARIABLE.bw_ctr = 150
    SCRIPT.VARIABLE.ttl_s_power += 1
    SCRIPT.VARIABLE.stg_ttl_s_power += 1

    if (src.type == 1 and
        SCRIPT.VARIABLE.s_power < 32):
        SCRIPT.VARIABLE.s_power += 1
    elif src.type == 2:
        SCRIPT.VARIABLE.player += 1
        
    src.kill()


def cal_s_power() -> str:
    return f"{FUNC.Calculate.divide(SCRIPT.VARIABLE.stg_ttl_s_power, SCRIPT.VARIABLE.ttl_spwn_s_power, 0) * 100:.2f} %"