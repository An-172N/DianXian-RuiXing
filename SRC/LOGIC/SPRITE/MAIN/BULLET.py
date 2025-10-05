import random as rand

import BRICK


class BulletMgr:
    def __init__(th, own):
        th.own = own

        th.is_cnt_fusil = False

        th.fusil_cnt = 0

        th.bomb = BRICK.RectRaining(th)

    def spwn_blts(th):
        p = 2 ** (th.own.pln_mgr.s_pt // 32)
        q = 2 ** (th.own.pln_mgr.s_pt // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                th.bomb.fire(0 + i * 10, 0 + i * 12,
                             j)
                
        th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char, 2,
                                  th.own.pln_mgr.char.clr)

    def single_bomb(th):
        if (not th.own.pln_mgr.is_use_sdivide and
            th.own.pln_mgr.s_pt >= 8):
            th.own.pln_mgr.s_pt -= 8
            th.own.pln_mgr.is_use_sdivide = True

    def use_bomb(th):
        if th.own.pln_mgr.is_use_sdivide:
            th.bomb.free()

    def use_fusil(th):
        if (th.fusil_cnt > 0 and
            not th.is_cnt_fusil):
            th.spwn_blts()

            th.fusil_cnt -= 1

    def blt_coll(th, src, tar):
        tar.hp -= src.dmg
        th.own.sc_mgr.sc_cnt += th.own.sc_mgr.blt_coll()

        if tar.hp <= 0:
            if hasattr(tar, "bomb"):
                th.own.stg_mgr.shhm_lose()
            elif rand.random() <= 0.24:
                th.own.item_mgr.item_spwn(th.own.clr_dict[5], 1,
                                          (tar.rect.centerx, tar.rect.centery))
            elif rand.random() <= 0.001:
                th.own.item_mgr.item_spwn(th.own.clr_dict[3], 2,
                                          (tar.rect.centerx, tar.rect.centery))
            elif rand.random() <= 0.24:
                th.own.brg_mgr.spwn_brg(tar, rand.choice([(0, 1, 1),
                                                          (-30, 31, 30)]))

            th.own.ptcl_mgr.spwn_ptcl(tar, 2,
                                      tar.clr, th.own.clr_dict[6])
            
            tar.kill()