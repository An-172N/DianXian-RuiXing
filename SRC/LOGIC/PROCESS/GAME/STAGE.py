from STAGE.STAGE1.STAGE1 import Stage1


class Stage:
    stg_dict = {
        1: Stage1
    }

    def __init__(th, own):
        th.own = own

        th.talk_txt = 0
        th.stg = 1
        th.lv = 5

        th.curr_stg = th.stg_dict.get(th.stg)(th)

        th.pau = False
        th.ru_sure = False
        th.summ = False
        th.talk = False
        th.is_spwn_fri = False
    
    def next_lv(th): # 下一关
        if th.lv >= 6:
            th.stg += 1
            th.lv = 1

            th.curr_stg = th.stg_dict.get(th.stg)(th)
        else:
            th.lv += 1

        th.own.rst_mgr.rst_pau()
        th.own.sl_gen.lv_ld = False

        if th.lv == 6:
            th.talk = True

        th.own.rst_mgr.add_sc()

        th.own.rst_mgr.rst_spr()
        th.own.rst_mgr.rst_pln()
        th.own.rst_mgr.rst_bomb()
        th.own.rst_mgr.rst_ctr()

    def rt_txt(th):
        return th.curr_stg.txt().get(th.talk_txt)

    def spwn_shhm(th):
        th.curr_stg.char.rect.center = (292, 60)

        th.own.brc_grp.add(th.curr_stg.char)

        th.is_spwn_fri = True
    
    def mv_shhm(th):
        if th.lv == 6:
            th.curr_stg.mv_char()