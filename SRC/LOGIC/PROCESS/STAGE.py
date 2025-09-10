from STAGE.STAGE1.STAGE1 import Stage1


class Stage:
    def __init__(th, own):
        th.own = own

        th.talk_text = 0
        th.stg = 1
        th.lv = 1

        th.pau = False
        th.ru_sure = False
        th.summ = False
        th.talk = False
        th.is_spwn_fri = False

    def get_stg(th): # 关卡字典
        bg_dict = {
            1: Stage1(th)
        }

        return bg_dict.get(th.stg)
    
    def rt_text(th):
        return th.get_stg().text().get(th.talk_text)
    
    def next_lv(th): # 下一关
        if th.lv >= 6:
            th.stg += 1
            th.lv = 1
        else:
            th.lv += 1

        th.own.sl_gen.lv_ld = False
        th.summ = False

        if th.lv == 6:
            th.talk = True
        # 执行完后重置
        th.rst_game()

    def rst_game(th): # 重置游戏
        # 加结算分
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.get_pow()
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.no_hurt()
        # 清除精灵
        th.own.item_grp.empty()
        th.own.pln_grp.empty()
        th.own.blt_grp.empty()
        th.own.ptcl_grp.empty()
        th.own.brg_grp.empty()
        # 重置飞机和bomb    
        th.own.pln_mgr.rst_pln()
        th.own.bomb_mgr.rect_rainer.rst_bomb()
        # 重置参数
        th.own.pln_mgr.is_use_bomb = False
        th.own.invinc.cd_ctr = 0
        th.own.item_mgr.spwn_ctr = 0
        th.own.item_mgr.bw_ctr = 0
        th.own.pln_mgr.ttl_s_pt = 0
        th.own.coll_mgr.ctr = 0
        th.own.blt_mgr.fusillade_ctr = 0

    def pau_evt(th): # 暂停界面反转
        th.pau = not th.pau

    def ru_sure_evt(th): # 确定界面反转
        th.ru_sure = not th.ru_sure

    def spwn_shhm(th):
        get_stg = th.get_stg()

        if not th.is_spwn_fri:
            get_stg.char.rect.centerx = th.own.win.width // 2 + 120
            get_stg.char.rect.y = 60

            th.own.brc_grp.add(get_stg.char)
            
            th.is_spwn_fri = True
    
    def mv_shhm(th):
        if th.lv == 6:
            for char in th.own.brc_grp:
                if char.type == "fri":
                    th.get_stg().move(char)