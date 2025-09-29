import pygame as pyg

from BRICK.HUMAN.ONO import Ono


class StageMgr:
    def __init__(th, own):
        th.own = own

        th.txt_num = 0
        th.stg = 1
        th.lv = 0

        th.bg = th.chs_bg()
        th.bg.set_alpha(159)

        th.char = None
        th.txt = None

        th.pau = False
        th.summ = False
        th.talk = False
        th.sav = False

    def next_lv(th):
        th.own.rst_mgr.rst_pau()
        th.own.rst_mgr.rst_spr()
        th.own.rst_mgr.rst_pln()
        th.own.rst_mgr.rst_bomb()

        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.get_pow()
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.no_hurt()

        th.own.sl_gen.lv_ld = False
        th.own.pln_mgr.no_hurt_cnt += 1
        th.own.pln_mgr.spwn_pln()
    
    def lv_lgc(th):
        if th.lv >= 6:
            th.stg += 1
            th.lv = 1

            th.bg = th.chs_bg()
        else:
            th.lv += 1

            if th.lv == 6:
                th.char = th.chs_shhm()
                th.txt = th.own.sl_gen.ld_txt()
                th.txt_num = 0
                th.talk = True

                th.spwn_shhm()

    def chs_shhm(th):
        char_dict = {
            1: Ono
        }

        return char_dict.get(th.stg)(th)
    
    def chs_bg(th):
        return pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()

    def spwn_shhm(th):
        th.char.rect.center = (292, 60)
        th.own.brc_grp.add(th.char)
    
    def rt_txt(th):
        return (th.txt["txt"][f"{th.txt_num}"]["human"],
                th.txt["txt"][f"{th.txt_num}"]["info"])