class Reset:
    def __init__(th, own):
        th.own = own

    def rst_stage(th): # 重置关卡
        # 清除精灵
        th.own.item_grp.empty()
        th.own.brc_grp.empty()
        th.own.pln_grp.empty()
        th.own.blt_grp.empty()
        th.own.ptcl_grp.empty()
        th.own.brg_grp.empty()
        # 重置飞机
        th.own.pln_mgr.rst_pln()
        th.own.stg_mgr.is_spwn_fri = False
        # 重置bomb
        th.own.blt_mgr.rect_rain.rst_bomb()
        # 重置无敌计数器
        th.own.invinc.cd_ctr = 0
        # 重置生成和combo计数器
        th.own.item_mgr.spwn_ctr = 0
        th.own.item_mgr.bw_ctr = 0
        # 本关收集点数清零和无敌状态复原
        th.own.pln_mgr.ttl_s_pt = 0
        th.own.pln_mgr.is_use_sdivide = False
        th.own.pln_mgr.is_wait_respwn = False
        th.own.pln_mgr.coll = False
        # 连发计数归零
        th.own.blt_mgr.fusil_cnt = 0

    def rst_game(th):
        # 先重置关卡
        th.rst_stage()
        # 形点、无伤和闪躲复原
        th.own.pln_mgr.s_pt = 80
        th.own.pln_mgr.no_hurt_cnt = 0
        th.own.pln_mgr.plyr = 7
        th.own.item_mgr.item_cnt = 0
        th.own.item_mgr.coll_item_cnt = 0
        # 分数清零
        th.own.sc_mgr.sc_cnt = 0
        # 菜单状态复原
        th.own.stg_mgr.pau = False
        th.own.stg_mgr.ru_sure = False
        th.own.stg_mgr.summ = False
        th.own.stg_mgr.talk = False
        th.own.sav_mgr.is_sav = False
        # 关卡状态复原
        th.own.sl_gen.lv_ld = False
        th.own.stg_mgr.stg = 1
        th.own.stg_mgr.lv = 5
        th.own.stg_mgr.talk_txt = 0
        th.own.stg_mgr.curr_stg = th.own.stg_mgr.stg_dict.get(th.own.stg_mgr.stg)(th.own.stg_mgr)
        # 运行状态为假
        th.own.run = False

    def add_sc(th): # 加结算分
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.get_pow()
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.no_hurt()