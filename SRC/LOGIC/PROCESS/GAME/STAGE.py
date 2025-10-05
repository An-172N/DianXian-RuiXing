import pygame as pyg

import BRICK


class StageMgr:
    def __init__(th, own):
        th.own = own

        th.txt_num = 0
        th.txt_pt = 1
        th.ctr = 0
        th.stg = 1
        th.lv = 5

        th.bg = th.chs_bg()
        th.bg.set_alpha(159)

        th.char = None
        th.txt = None

    def next_lv(th):
        th.own.rst_mgr.rst_pau()
        th.own.rst_mgr.rst_spr()
        th.own.rst_mgr.rst_pln()
        th.own.rst_mgr.rst_bomb()

        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.get_pow()
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.no_hurt()

        th.own.pln_mgr.no_hurt_cnt += 1
        th.own.pln_mgr.spwn_pln()

    def lv_proc(th):
        if not th.own.lv_ld:
            if th.ctr <= 45:
                th.ctr += 1
            else:
                if th.lv == 6:
                    th.char = th.chs_shhm()
                    th.txt = th.own.sl_gen.ld_txt()
                    th.txt_num = 0
                    th.own.talk = True

                    th.spwn_shhm()
                else:
                    th.own.sl_gen.ld_stg()

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
        char_dict = {
            1: BRICK.Ono
        }

        return char_dict.get(th.stg)(th.own)
    
    def shhm_lose(th):
        th.txt_pt += 1
        th.txt_num = 0

        th.own.talk = True
    
    def chs_bg(th):
        return pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()

    def spwn_shhm(th):
        th.char.rect.center = (292, 60)
        th.own.brc_grp.add(th.char)
    
    def rt_txt(th):
        return (th.txt[f"{th.txt_pt}"][f"{th.txt_num}"]["human"],
                th.txt[f"{th.txt_pt}"][f"{th.txt_num}"]["info"],
                th.txt[f"{th.txt_pt}"][f"{th.txt_num}"]["talk"])