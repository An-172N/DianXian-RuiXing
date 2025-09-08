from BRICKS.BASESHAPE import BaseShape

from TOOLS.MOVE import mv
from TOOLS.ROTATE import rot


class BulletManager:
    def __init__(th, own):
        th.own = own

    def spwn_blts(th):
        if not th.own.pln_mgr.is_wait_respwn:
            for item in th.own.item_grp:
                if th.own.pln_mgr.char.rect.colliderect(item.rect):
                    th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char,
                                              (45, 194, 229))

                    th.k_blt(0, 0,
                               0)
                    th.k_blt(10, 12,
                               4)

                    if th.own.s_pt >= 24:
                        th.k_blt(10, 12,
                                   -4)
                    if th.own.s_pt >= 48:
                        th.k_blt(20, 24,
                                   8)
                        th.k_blt(20, 24,
                                   -8)

    def k_blt(th, dx, dy, ang):
        pln_mgr = th.own.pln_mgr

        blt_type = [
            {'pos': (pln_mgr.char.rect.left - dx, pln_mgr.char.rect.top + dy),
             'ang': ang},
            {'pos': (pln_mgr.char.rect.right + dx, pln_mgr.char.rect.top + dy),
             'ang': -ang}
        ]

        for blt_info in blt_type:
            pos = blt_info['pos']
            ang = blt_info['ang']

            blt = BaseShape(2, 15, 0,
                            (45, 194, 229), 1, 0)

            blt.rect.center = pos
            blt.curr_ang = ang
            blt.spd = 16
            blt.damage = 4

            th.own.blt_grp.add(blt)

    def upd_blts(th):
        for blt in th.own.blt_grp:
            if blt.type == 0:
                rot(blt)
                mv(blt, blt.spd)