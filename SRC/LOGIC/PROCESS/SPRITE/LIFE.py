class Life:
    def __init__(th, own):
        th.own = own

    def life_lgc(th):
        if th.own.pln_mgr.s_pt >= 16:
            th.own.pln_mgr.s_pt -= 16
        else:
            th.own.pln_mgr.is_wait_respwn = True
            th.own.pln_mgr.plyr -= 1

            th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char,
                                      (255, 255, 255), (45, 194, 229))

            th.own.pln_grp.empty()

            if th.own.pln_mgr.plyr == 0:
                th.own.sav_mgr.is_sav = True
            
        th.own.pln_mgr.no_hurt_cnt = 0
        th.own.item_mgr.bw_ctr = 0

    def respwn(th):
        if (th.own.pln_mgr.is_wait_respwn and
            th.own.invinc.cd_ctr >= 30):
            th.own.pln_mgr.rst_pln()

            th.own.pln_mgr.is_wait_respwn = False
            th.own.invinc.cd_ctr = 0