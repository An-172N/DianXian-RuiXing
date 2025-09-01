from STAGE.STAGE1 import Stage1


class StageManager:
    def __init__(th, own):
        th.own = own

        th.pau = False
        th.ru_sure = False
        th.summ = False

    def get_stg(th): # 关卡字典
        bg_dict = {
            1: Stage1(th.own.scr)
        }

        return bg_dict.get(th.own.stg)
    
    def next_lv(th): # 下一关
        th.own.lv += 1
        th.own.sl_gen.lv_ld = False
        th.summ = False
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