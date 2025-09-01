class CollideManager:
    def __init__(th, own):
        th.own = own

    def chk_blt_coll(th):
        for blt in th.own.blt_grp:
            for brc in th.own.brc_grp:
                if blt.rect.colliderect(brc.rect):
                    brc.hp -= blt.damage

                    th.own.get_sc.blt_coll()
                    th.own.rm_mgr.brc_death(brc)
                    blt.kill()

    def chk_item_coll(th):
        pln_mgr = th.own.pln_mgr
        item_mgr = th.own.item_mgr

        for item in th.own.item_grp:
            if pln_mgr.char.rect.colliderect(item.rect):
                item_mgr.combo += 1
                item_mgr.bw_ctr = 90

                if item.type == 1:
                    if th.own.s_pt <= 96:
                        th.own.s_pt += 1
                        
                    th.own.ttl_s_pt += 1
                else:
                    pass

                item.kill()

    def chk_brg_coll(th):
        pln_mgr = th.own.pln_mgr

        for brg in th.own.brg_grp:
            if (brg.rect.collidepoint(pln_mgr.dec_pt.rect.center)
                and not (pln_mgr.coll or
                         pln_mgr.is_use_bomb or
                         pln_mgr.is_wait_respwn)):
                pln_mgr.coll = True
                th.own.cooldown_ctr = 0
                pln_mgr.life_lgc()