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

                    if blt.type in (0, 1):
                        blt.kill()

    def chk_item_coll(th):
        for item in th.own.item_grp:
            if th.own.pln_mgr.char.rect.colliderect(item.rect):
                th.own.item_mgr.combo += 1
                th.own.item_mgr.bw_ctr = 90

                if item.type == 1:
                    if th.own.s_pt <= 96:
                        th.own.s_pt += 1
                        
                    th.own.ttl_s_pt += 1
                else:
                    pass

                item.kill()

    def chk_brg_coll(th):
        for brg in th.own.brg_grp:
            if (brg.rect.collidepoint(th.own.pln_mgr.dec_pt.rect.center)
                and not (th.own.pln_mgr.coll or
                         th.own.pln_mgr.is_use_bomb or
                         th.own.pln_mgr.is_wait_respwn)):
                th.own.pln_mgr.coll = True
                th.own.cooldown_ctr = 0
                th.own.pln_mgr.life_lgc()