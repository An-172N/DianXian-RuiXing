import random as rand
import json

import FUNC
import SCRIPT.DICT
import SCRIPT.VARIABLE
import SCRIPT.RESET
from SCRIPT.LOGIC.FRIEND import Base


def next_lv():
    SCRIPT.VARIABLE.sc += SCRIPT.VARIABLE.ttl_spt * 512
    SCRIPT.VARIABLE.sc += SCRIPT.VARIABLE.no_hurt * 4096

    SCRIPT.RESET.rst1()

    SCRIPT.VARIABLE.no_hurt += 1
    SCRIPT.VARIABLE.main_char.rect.center = (292, 331)
    SCRIPT.VARIABLE.pln_grp.add(SCRIPT.VARIABLE.main_char)
    SCRIPT.VARIABLE.pln_grp.add(SCRIPT.VARIABLE.d_pt)


def lv_ld():
    if SCRIPT.VARIABLE.ctr <= 60:
        SCRIPT.VARIABLE.ctr += 1
    else:
        if SCRIPT.VARIABLE.level == 6:
            SCRIPT.VARIABLE.char = chs_shhm()
            SCRIPT.VARIABLE.char.rect.center = (292, 60)
            SCRIPT.VARIABLE.txt = ld_txt(SCRIPT.VARIABLE.stage)
            SCRIPT.VARIABLE.txt_num = 0
            SCRIPT.VARIABLE.talk = True

            SCRIPT.VARIABLE.brc_grp.add(SCRIPT.VARIABLE.char)
        else:
            for i in FUNC.Process.process_file(
                         f"ASSET/STG_{SCRIPT.VARIABLE.stage}-{SCRIPT.VARIABLE.level}.stg",
                         'ascii',
                         0,
                         ld_stg
                     ):
                i

        SCRIPT.VARIABLE.sec_bg = SCRIPT.VARIABLE.pic[SCRIPT.VARIABLE.stage]
        SCRIPT.VARIABLE.sec_bg.set_alpha(159)
        SCRIPT.VARIABLE.ctr = 0
        SCRIPT.VARIABLE.level_ld = True


def lv_summ():
    if (len(SCRIPT.VARIABLE.brc_grp) == 0 and
        not SCRIPT.VARIABLE.talk):
        if SCRIPT.VARIABLE.ctr <= 150:
            SCRIPT.VARIABLE.ctr += 1
            SCRIPT.VARIABLE.summ = True
        else:
            if SCRIPT.VARIABLE.stage >= 2 and SCRIPT.VARIABLE.level == 6:
                SCRIPT.VARIABLE.summ = False
                SCRIPT.VARIABLE.sav = True
                SCRIPT.VARIABLE.ctr = 0
            else:
                next_lv()
                lv_lgc()

                SCRIPT.VARIABLE.summ = False
                SCRIPT.VARIABLE.ctr = 0


def lv_proc():
    if not SCRIPT.VARIABLE.level_ld:
        lv_ld()
    else:
        lv_summ()


def lv_lgc():
    if SCRIPT.VARIABLE.level >= 6:
        SCRIPT.VARIABLE.stage += 1
        SCRIPT.VARIABLE.level = 1
    else:
        SCRIPT.VARIABLE.level += 1


def chs_shhm():
    return SCRIPT.DICT.char_dict.get(SCRIPT.VARIABLE.stage)()


def shhm_lose():
    SCRIPT.VARIABLE.txt_pt += 1
    SCRIPT.VARIABLE.txt_num = 0

    SCRIPT.VARIABLE.talk = True


def ld_stg(row, line):
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = SCRIPT.DICT.clr_dict[SCRIPT.VARIABLE.stage] if rand.random() >= 0.031 else SCRIPT.DICT.clr_dict[6]
            x = 127 + i * 15
            y = 22 + row * 15

            brc = Base((15, 15, 2),
                       c, shape)

            if not hasattr(brc, "hp"):
                brc.hp = 4
            brc.rect.center = (x, y)

            SCRIPT.VARIABLE.brc_grp.add(brc)


def ld_txt(stg):
    file = f"ASSET/TALK_{stg}.json"

    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)