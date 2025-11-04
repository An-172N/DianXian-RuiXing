import random as rand
import json

import pygame as pyg

import DICT
import FUNC
from FRIEND import Base


class StageMgr:
    def __init__(th, own):
        th.own = own

        th.txt_num = 0
        th.txt_pt = 0
        th.ctr = 0
        th.stg = 1
        th.lv = 5

        th.bg = pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()
        th.bg.set_alpha(159)

        th.char = None
        th.txt = None

    def next_lv(th):
        th.own.pln_mgr.sc += th.own.blt_mgr.ttl_spt * 512
        th.own.pln_mgr.sc += th.own.pln_mgr.no_hurt * 4096

        for bra in DICT.rst_dict["rst1"]:
            for evt in DICT.rst_dict["rst1"][bra]:
                DICT.rst_dict["rst1"][bra][evt](th.own)

        th.own.pln_mgr.no_hurt += 1
        th.own.pln_mgr.char.rect.center = (292, 331)
        th.own.pln_grp.add(th.own.pln_mgr.char)

    def lv_ld(th):
        if th.ctr <= 60:
            th.ctr += 1
        else:
            if th.lv == 6:
                th.char = th.chs_shhm()
                th.char.rect.center = (292, 60)
                th.txt = ld_txt(th.stg)
                th.txt_num = 0
                th.own.talk = True

                th.own.brc_grp.add(th.char)
            else:
                ld_stg((th.stg, th.lv),
                       (DICT.clr_dict[th.stg], DICT.clr_dict[6], 0.04),
                       (127, 22),
                       (15, 15, 4),
                       th.own.brc_grp
                )

            th.ctr = 0
            th.own.lv_ld = True

    def lv_summ(th):
        if (len(th.own.brc_grp) == 0 and
            not th.own.talk):
            if th.ctr <= 105:
                th.ctr += 1
                th.own.summ = True
            else:
                th.next_lv()
                th.lv_lgc()

                th.own.summ = False
                th.ctr = 0

    def lv_proc(th):
        if not th.own.lv_ld:
            th.lv_ld()
        else:
            th.lv_summ()
    
    def lv_lgc(th):
        if th.lv >= 6:
            th.stg += 1
            th.lv = 1
            th.bg = pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()
            th.bg.set_alpha(159)
        else:
            th.lv += 1

    def chs_shhm(th):
        return DICT.char_dict.get(th.stg)(th)
    
    def shhm_lose(th):
        th.txt_pt += 1
        th.txt_num = 0

        th.own.talk = True
    

def ld_stg(stg, clr, pos, val, spr_grp):
    file = f"AST/STG_{stg[0]}-{stg[1]}.stg"
    row = 0

    for line in FUNC.Process.process_file(file, 'r', lambda f: f.read()).splitlines():
        for i in range(len(line)):
            if line[i] != 'o':
                shape = int(line[i])
                c = clr[0] if rand.random() >= clr[2] else clr[1]
                x = pos[0] + i * val[0]
                y = pos[1] + row * val[1]

                brc = Base((val[0], val[1], 2),
                            c, shape)

                if not hasattr(brc, "hp"):
                    brc.hp = 4
                brc.rect.center = (x, y)

                spr_grp.add(brc)

        row += 1


def ld_txt(stg):
    file = f"AST/TALK_{stg}.json"

    return json.loads(FUNC.Process.process_file(file, 'r', lambda f: f.read()))