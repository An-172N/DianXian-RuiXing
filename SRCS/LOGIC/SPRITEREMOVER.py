import random as rand


class SpriteRemove:
    def __init__(th, own):
        th.own = own

    def rm_sprs(th, spr_grp):
        [spr.kill() for spr in spr_grp
         if not th.own.eff_range.collidepoint(spr.rect.center)]

    def brc_death(th, brc):
        item_mgr = th.own.item_mgr
        ptcl_mgr = th.own.ptcl_mgr
        brg_mgr = th.own.brg_mgr
        w_brc_proc = th.own.w_brc_proc

        if brc.hp <= 0:
            if rand.random() <= 0.24:
                item_mgr.item_spwn(brc.rect.x, brc.rect.y,
                                   1,
                                   (45, 194, 229))

            if brc.clr == (255, 255, 255):
                if brc.shape == 0:
                    w_brc_proc.polygon_brc(brc)
                elif brc.shape == 1:
                    pass
                else:
                    w_brc_proc.circle_brc(brc)

            ptcl_mgr.spwn_ptcl(brc,
                               (255, 255, 255), brc.clr)
            brg_mgr.spwn_brg(brc)

            brc.kill()