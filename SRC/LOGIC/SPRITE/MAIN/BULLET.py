from BRICK.BASE.BULLET import KliBullet


class BulletMgr:
    def __init__(th, own):
        th.own = own

        th.is_cnt_fusil = False

        th.fusil_cnt = 0
        th.bomb_cnt = 0
        th.ctr = 0

    def spwn_blts(th):
        p = 2 ** (th.own.pln_mgr.s_pt // 32)
        q = 2 ** (th.own.pln_mgr.s_pt // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                th.k_blt(0 + i * 10, 0 + i * 12,
                         j)
                
        th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char,
                                  2, (45, 194, 229))

    def k_blt(th, dx, dy, ang):
        blt_type = [
            {'x': th.own.pln_mgr.char.rect.left - dx,
             'y': th.own.pln_mgr.char.rect.top + dy,
             'ang': ang},
            {'x': th.own.pln_mgr.char.rect.right + dx,
             'y': th.own.pln_mgr.char.rect.top + dy,
             'ang': -ang}
        ]

        for blt_info in blt_type:
            blt = KliBullet(2, 15,
                            "blt")

            blt.rect.center = (blt_info['x'], blt_info['y'])
            blt.curr_ang = blt_info['ang']
            blt.dmg = 4

            th.own.blt_grp.add(blt)

    def single_bomb(th):
        if (not th.own.pln_mgr.is_use_sdivide and
            th.own.pln_mgr.s_pt >= 8):
            th.own.pln_mgr.s_pt -= 8
            th.own.pln_mgr.cd_ctr = 0
            th.own.pln_mgr.is_use_sdivide = True

    def use_bomb(th):
        if th.own.pln_mgr.is_use_sdivide:
            th.ctr += 1

            if (th.ctr >= 60 and
                th.ctr % 2 == 0 and
                th.bomb_cnt < 6):
                for i in range(120, 466, 15):
                    blt = KliBullet(15, 15,
                                    "bomb")

                    blt.rect.center = (i, 0)

                    th.own.blt_grp.add(blt)
            
                th.bomb_cnt += 1

    def use_fusil(th):
        if th.fusil_cnt > 0:
            if not th.is_cnt_fusil:
                th.spwn_blts()

                th.fusil_cnt -= 1
                th.own.pln_mgr.s_pt -= 1
            
            if th.own.pln_mgr.s_pt < th.fusil_cnt + 1:
                th.fusil_cnt = th.own.pln_mgr.s_pt