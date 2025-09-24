import pygame as pyg

from BRICK.HUMAN.FRIEND import Friend


class Stage:
    def __init__(th, own):
        th.own = own

        th.txt_num = 0
        th.stg = 1
        th.lv = 1

        th.char = None

        th.bg = th.choose_bg()
        th.bg.set_alpha(175)

        th.txt = {}

        th.pau = False
        th.ru_sure = False
        th.summ = False
        th.talk = False
        th.sav = False
    
    def next_lv(th): # 下一关
        th.own.rst_mgr.rst_pau()
        th.own.rst_mgr.add_sc()
        th.own.rst_mgr.rst_spr()
        th.own.rst_mgr.rst_pln()
        th.own.rst_mgr.rst_bomb()
        th.own.rst_mgr.rst_ctr()

        th.own.sl_gen.lv_ld = False

        if th.lv >= 6:
            th.stg += 1
            th.lv = 1

            th.char = None

            th.bg = th.choose_bg()

            if th.lv == 6:
                th.talk = True
        else:
            th.lv += 1

    def choose_fri(th):
        pln_dict = {
            1: ('Ono', 'AST\IMG_ONO.png', 
                96, (255, 128, 0), 2)
        }

        if th.own.stg_mgr.stg in pln_dict:
            name, pic, hp, clr, shape = pln_dict[th.own.stg_mgr.stg]
            th.char = Friend(name, pic, hp, clr, shape)

    def spwn_shhm(th):
        th.choose_fri()

        th.char.rect.center = (292, 60)

        th.own.brc_grp.add(th.char)
    
    def mv_shhm(th):
        if th.lv == 6:
            pass

    def rt_txt(th):
        return th.txt.get(th.txt_num)

    def choose_bg(th):
        return pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()