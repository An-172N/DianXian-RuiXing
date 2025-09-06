from STAGE.STAGE1 import Stage1


class StageManager:
    def __init__(th, own):
        th.own = own

        th.pau = False
        th.ru_sure = False
        th.summ = False
        th.talk = False
        th.is_spwn = False

        th.text = 0

    def get_stg(th): # 关卡字典
        bg_dict = {
            1: Stage1(th)
        }

        return bg_dict.get(th.own.stg)
    
    def rt_text(th):
        return th.get_stg().text().get(th.text)
    
    def next_lv(th): # 下一关
        if th.own.lv >= 6:
            th.own.stg += 1
            th.own.lv = 1
        else:
            th.own.lv += 1

        th.own.sl_gen.lv_ld = False
        th.summ = False

        if th.own.lv == 6:
            th.talk = True
        # 执行完后重置
        th.rst_game()

    def rst_game(th): # 重置游戏
        pln_mgr = th.own.pln_mgr
        bomb_mgr = th.own.bomb_mgr
        item_mgr = th.own.item_mgr
        get_sc = th.own.get_sc
        # 加结算分
        th.own.sc_cnt += get_sc.get_pow()
        th.own.sc_cnt += get_sc.no_hurt()
        # 清除精灵
        th.own.item_grp.empty()
        th.own.pln_grp.empty()
        th.own.blt_grp.empty()
        th.own.ptcl_grp.empty()
        th.own.brg_grp.empty()
        # 重置飞机和bomb    
        pln_mgr.rst_pln()
        bomb_mgr.rect_rainer.rst_bomb()
        # 重置参数
        pln_mgr.is_use_bomb = False
        th.own.cooldown_ctr = 0
        item_mgr.spwn_ctr = 0
        item_mgr.bw_ctr = 0
        th.own.ttl_s_pt = 0
        th.own.coll_mgr.ctr = 0

    def pau_evt(th): # 暂停界面反转
        th.pau = not th.pau

    def ru_sure_evt(th): # 确定界面反转
        th.ru_sure = not th.ru_sure

    def spwn_shhm(th):
        get_stg = th.get_stg()

        if not th.is_spwn:
            get_stg.char.rect.centerx = th.own.win.width // 2 + 120
            get_stg.char.rect.y = 60

            th.own.brc_grp.add(get_stg.char)
            
            th.is_spwn = True
    
    def move_shhm(th):
        pass