class Collide:
    def __init__(th, own):
        th.own = own

    def chk_blt_coll(th):
        for blt in th.own.blt_grp:
            for brc in th.own.brc_grp:
                if blt.rect.colliderect(brc.rect):
                    brc.hp -= blt.dmg

                    th.own.sc_mgr.blt_coll()
                    th.own.rm_mgr.brc_death(brc)

                    if blt.type in ("blt", "bomb"):
                        blt.kill()

    def chk_item_coll(th):
        for item in th.own.item_grp:
            if th.own.pln_mgr.char.rect.colliderect(item.rect):
                th.own.item_mgr.comb += 1
                th.own.item_mgr.bw_ctr = 90

                if not th.own.blt_mgr.is_cnt_fusil:
                    th.own.blt_mgr.spwn_blts()
                else:
                    if (th.own.pln_mgr.s_pt > th.own.blt_mgr.fusil_cnt * 2 + 1
                        and th.own.blt_mgr.fusil_cnt <= 1):
                        th.own.blt_mgr.fusil_cnt += 1

                if item.type == 1:
                    if th.own.pln_mgr.s_pt < 80:
                        th.own.pln_mgr.s_pt += 1
                        
                    th.own.pln_mgr.ttl_s_pt += 1

                item.kill()

    def chk_brg_coll(th):
        for brg in th.own.brg_grp:
            if (brg.rect.collidepoint(th.own.pln_mgr.dec_pt.rect.center)
                and not (th.own.pln_mgr.coll or
                         th.own.pln_mgr.is_use_sdivide or
                         th.own.pln_mgr.is_wait_respwn)):
                th.own.pln_mgr.coll = True
                th.own.invinc.cd_ctr = 0
                th.own.pln_mgr.life_lgc()