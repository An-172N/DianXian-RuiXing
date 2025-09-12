import random as rand


class SpriteRemove:
    def __init__(th, own):
        th.own = own

    def rm_sprs(th, spr_grp):
        [spr.kill() for spr in spr_grp
         if not th.own.eff_range.collidepoint(spr.rect.center)]

    def brc_death(th, brc):
        if brc.hp <= 0:
            if rand.random() <= 0.24:
                th.own.item_mgr.item_spwn(brc.rect.x, brc.rect.y,
                                          1,
                                          (45, 194, 229))
                
            if brc.clr == (255, 255, 255):
                if brc.shape == 0:
                    th.own.wb_p.polygon_brc(brc)
                elif brc.shape == 1:
                    pass
                elif brc.shape == 2:
                    th.own.wb_p.circle_brc(brc)
                
            th.own.ptcl_mgr.spwn_ptcl(brc,
                                      (255, 255, 255), brc.clr)
            th.own.brg_mgr.spwn_brg(brc)

            brc.kill()