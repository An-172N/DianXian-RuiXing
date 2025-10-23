import pygame as pyg

import DICT
from FUNC import Load
from FUNC import Spawn
from FUNC import Base


class StageMgr:
    def __init__(th, own):
        th.own = own

        th.txt_num = 0
        th.txt_pt = 0
        th.ctr = 0
        th.stg = 1
        th.lv = 5

        th.bg = th.chs_bg()
        th.bg.set_alpha(159)

        th.char = None
        th.txt = None

    def next_lv(th):
        th.own.pln_mgr.sc += th.own.blt_mgr.ttl_spt * 512
        th.own.pln_mgr.sc += th.own.pln_mgr.no_hurt * 4096

        for bra in th.own.proc("rst1"):
            for evt in th.own.proc("rst1", bra):
                th.own.proc("rst1", bra, evt)

        th.own.pln_mgr.no_hurt += 1
        th.own.pln_mgr.spwn_pln()

    def lv_proc(th):
        if not th.own.lv_ld:
            if th.ctr <= 60:
                th.ctr += 1
            else:
                if th.lv == 6:
                    th.char = th.chs_shhm()
                    th.txt = Load.ld_txt(th.stg)
                    th.txt_num = 0
                    th.own.talk = True

                    th.spwn_shhm()
                else:
                    Load.ld_stg((th.stg, th.lv),
                                (DICT.clr_dict[th.stg], DICT.clr_dict[6], 0.04),
                                (2, 4, 6, 30 - th.stg),
                                (127, 22), (15, 15), 4,
                                Base, th.own.brc_grp)

                th.ctr = 0
                th.own.lv_ld = True
        else:
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
    
    def lv_lgc(th):
        if th.lv >= 6:
            th.stg += 1
            th.lv = 1
            th.bg = th.chs_bg()
        else:
            th.lv += 1

    def chs_shhm(th):
        return DICT.char_dict.get(th.stg)(th)
    
    def shhm_lose(th):
        th.txt_pt += 1
        th.txt_num = 0

        th.own.talk = True
    
    def chs_bg(th):
        return pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()

    def spwn_shhm(th):
        Spawn.shhm_spwn(th.char, th.own.brc_grp,
                        (292, 60))