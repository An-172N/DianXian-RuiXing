import random as rand
import json
import os

from typing import Optional, Any

import FUNC
import SCRIPT.DICT
import VARIABLE
import SCRIPT.RESET

from SCRIPT.LOGIC.FRIEND import Base


def next_lv() -> None:
    VARIABLE.sc += VARIABLE.ttl_s_power * 512
    VARIABLE.sc += VARIABLE.no_hurt * 4096

    SCRIPT.RESET.rst1()

    VARIABLE.no_hurt += 1
    VARIABLE.main_char.rect.center = (292, 331)
    VARIABLE.pln_grp.add(VARIABLE.main_char)
    VARIABLE.pln_grp.add(VARIABLE.d_pt)


def lv_ld() -> None:
    if VARIABLE.ctr <= 60:
        VARIABLE.ctr += 1
    else:
        if VARIABLE.level == 6:
            VARIABLE.char = chs_shhm()
            VARIABLE.char.rect.center = (292, 60)
            VARIABLE.txt = ld_txt(VARIABLE.stage)
            VARIABLE.txt_num = 0
            VARIABLE.talk = True

            VARIABLE.brc_grp.add(VARIABLE.char)
        else:
            for i in FUNC.Process.process_file(
                         os.path.join(VARIABLE.asset_path, f"STG_{VARIABLE.stage}-{VARIABLE.level}.stg"),
                         'ascii',
                         0,
                         ld_stg
                     ):
                i

        VARIABLE.sec_bg = VARIABLE.pic[VARIABLE.stage]
        VARIABLE.sec_bg.set_alpha(159)
        VARIABLE.ctr = 0
        VARIABLE.level_ld = True


def lv_summ() -> None:
    if (len(VARIABLE.brc_grp) == 0 and
        not VARIABLE.talk):
        if VARIABLE.ctr <= 150:
            VARIABLE.ctr += 1
            VARIABLE.summ = True
        else:
            if VARIABLE.stage >= 2 and VARIABLE.level == 6:
                VARIABLE.summ = False
                VARIABLE.sav = True
                VARIABLE.ctr = 0
            else:
                next_lv()
                lv_lgc()

                VARIABLE.summ = False
                VARIABLE.ctr = 0


def lv_proc() -> None:
    if not VARIABLE.level_ld:
        lv_ld()
    else:
        lv_summ()


def lv_lgc() -> None:
    if VARIABLE.level >= 6:
        VARIABLE.stage += 1
        VARIABLE.level = 1
    else:
        VARIABLE.level += 1


def chs_shhm() -> Optional[Any]:
    return SCRIPT.DICT.char_dict.get(VARIABLE.stage)()


def shhm_lose() -> None:
    VARIABLE.txt_pt += 1
    VARIABLE.txt_num = 0

    VARIABLE.talk = True


def ld_stg(row, line) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = SCRIPT.DICT.clr_dict[VARIABLE.stage] if rand.random() >= 0.042 else SCRIPT.DICT.clr_dict[6]
            x = 127 + i * 15
            y = 22 + row * 15

            brc = Base((15, 15, 2),
                       c, shape)

            if not hasattr(brc, "hp"):
                brc.hp = 4
            brc.rect.center = (x, y)

            VARIABLE.brc_grp.add(brc)


def ld_txt(stg) -> str:
    file = os.path.join(VARIABLE.asset_path, f"TALK_{stg}.json")

    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)