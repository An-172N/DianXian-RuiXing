class ResetMgr:
    def __init__(th, own):
        th.own = own

    def rst_spr(th):
        th.own.item_grp.empty()
        th.own.brc_grp.empty()
        th.own.pln_grp.empty()
        th.own.blt_grp.empty()
        th.own.ptcl_grp.empty()
        th.own.brg_grp.empty()

    def rst_pln(th):
        th.own.pln_mgr.cd_ctr = 0
        th.own.pln_mgr.ttl_s_pt = 0
        th.own.pln_mgr.is_spwn = False
        th.own.pln_mgr.is_use_sdivide = False
        th.own.pln_mgr.coll = False

    def rst_bomb(th):
        th.own.blt_mgr.fusil_cnt = 0
        th.own.blt_mgr.bomb.bomb_cnt = 0
        th.own.blt_mgr.bomb.ctr = 0

    def rst_pau(th):
        th.own.pau = False
        th.own.summ = False
        th.own.talk = False
        th.own.sav = False
        th.own.lv_ld = False

    def rst_game(th):
        th.rst_spr()
        th.rst_pln()
        th.rst_bomb()
        th.rst_pau()

        th.own.stg_mgr.stg = 1
        th.own.stg_mgr.lv = 0
        th.own.stg_mgr.char = None

        th.own.pln_mgr.s_pt = 48
        th.own.pln_mgr.no_hurt_cnt = 0
        th.own.pln_mgr.plyr = 7
        
        th.own.sc_mgr.sc_cnt = 0

        th.own.item_mgr.spwn_ctr = 0
        th.own.item_mgr.bw_ctr = 0

        th.own.run = False