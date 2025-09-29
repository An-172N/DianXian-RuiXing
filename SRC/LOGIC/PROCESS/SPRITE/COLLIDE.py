import random as rand


class CollideMgr:
    def __init__(th, own):
        th.own = own

    def chk_coll(th, src_grp, tar_grp, coll, code):
        for src in src_grp:
            for tar in tar_grp:
                if coll == 0:
                    if src.rect.colliderect(tar.rect):
                        code(src, tar)
                else:
                    if src.rect.collidepoint(tar.rect.center):
                        code(src, tar)

    def rm_spr(th, spr_grp):
        [spr.kill() for spr in spr_grp
         if not th.own.eff_range.collidepoint(spr.rect.center)]

    def blt_coll(th, src, tar):
        tar.hp -= src.dmg
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.blt_coll()

        if tar.hp <= 0:
            if rand.random() <= 0.24:
                th.own.item_mgr.item_spwn((45, 194, 229), 1,
                                          (tar.rect.centerx, tar.rect.centery))
                
                th.own.item_mgr.item_cnt += 1

            if rand.random() <= 0.32:
                rand.choice([th.own.brg_mgr.one_brg,
                             th.own.brg_mgr.cir_brg])(tar)

            th.own.ptcl_mgr.spwn_ptcl(tar, 2,
                                      (255, 255, 255), tar.clr)

            tar.kill()

        src.kill()

    def item_coll(th, src, _):
        th.own.item_mgr.comb += 1
        th.own.item_mgr.bw_ctr = 90

        if not th.own.blt_mgr.is_cnt_fusil:
            th.own.blt_mgr.spwn_blts()
        else:
            if (th.own.pln_mgr.s_pt > th.own.blt_mgr.fusil_cnt and
                th.own.blt_mgr.fusil_cnt <= 1):
                th.own.blt_mgr.fusil_cnt += 1

        if (src.type == 1 and
            th.own.pln_mgr.s_pt < 48):
            th.own.pln_mgr.s_pt += 1
                        
            th.own.pln_mgr.ttl_s_pt += 1
            th.own.item_mgr.coll_item_cnt += 1

        src.kill()

    def brg_coll(th, _, __):
        if (not (th.own.pln_mgr.coll or
                 th.own.pln_mgr.is_use_sdivide)):
            th.own.pln_mgr.coll = True
            th.own.life_mgr.cd_ctr = 0
            th.own.life_mgr.life_lgc()