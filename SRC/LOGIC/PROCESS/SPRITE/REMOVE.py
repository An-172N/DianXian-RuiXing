import random as rand


class Remove:
    def __init__(th, own):
        th.own = own

    def rm_sprs(th, spr_grp):
        [spr.kill() for spr in spr_grp
         if not th.own.eff_range.collidepoint(spr.rect.center)]

    def brc_death(th, brc):
        if brc.hp <= 0:
            if rand.random() <= 0.24:
                th.own.item_mgr.item_spwn(1,
                                          (45, 194, 229),
                                          (brc.rect.centerx, brc.rect.centery))
                
                th.own.item_mgr.item_cnt += 1
                
            th.own.ptcl_mgr.spwn_ptcl(brc,
                                      (255, 255, 255), brc.clr)
            th.own.brg_mgr.spwn_brg(brc)

            brc.kill()