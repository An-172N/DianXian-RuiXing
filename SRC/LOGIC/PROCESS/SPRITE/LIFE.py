class LifeMgr:
    def __init__(th, own):
        th.own = own

        th.cd_ctr = 0

    def life_lgc(th):
        if th.own.pln_mgr.s_pt >= 8:
            th.own.pln_mgr.s_pt -= 8
        else:
            th.own.pln_mgr.plyr -= 1

            th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char, 6,
                                      (255, 255, 255), (45, 194, 229))

            if th.own.pln_mgr.plyr == 0:
                th.own.stg_mgr.sav = True
            
        th.own.pln_mgr.no_hurt_cnt = 0
        th.own.item_mgr.bw_ctr = 0

    def invinc(th):
        if (th.own.pln_mgr.is_use_sdivide or
            th.own.pln_mgr.coll):
            th.cd_ctr += 1

            if th.cd_ctr >= 256:
                if th.own.pln_mgr.is_use_sdivide:
                    th.own.pln_mgr.is_use_sdivide = False
                    th.own.rst_mgr.rst_bomb()

                th.own.pln_mgr.coll = False
                th.own.pln_mgr.is_visitable = True
                
                th.cd_ctr = 0
            else:
                th.own.pln_mgr.is_visitable = (th.cd_ctr // 6) % 2 == 0
        else:
            th.own.pln_mgr.is_visitable = True