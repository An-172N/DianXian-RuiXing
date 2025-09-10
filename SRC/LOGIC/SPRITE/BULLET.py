from BRICK.BASE.BASESHAPE import BaseShape

from LOGIC.PROCESS.MOVE import mv
from LOGIC.PROCESS.MOVE import rot


class Bullet:
    def __init__(th, own):
        th.own = own

        th.fusillade_ctr = 0

        th.is_cnt_fusillade = False

    def spwn_blts(th):
        if (not th.own.pln_mgr.is_wait_respwn
            and not th.is_cnt_fusillade):
            th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char,
                                      (45, 194, 229))

            p = 2 ** (th.own.pln_mgr.s_pt // 48)

            for i in range(0, p):
                for j in range(-8, 9, 8):
                    th.k_blt(0 + i * 10, 0 + i * 12,
                             j)
                        
    def fusillade(th):
        if th.fusillade_ctr > 0:
            if th.fusillade_ctr > 3:
                th.is_cnt_fusillade = False
            if not th.is_cnt_fusillade:
                th.spwn_blts()

                th.fusillade_ctr -= 1

    def k_blt(th, dx, dy, ang):
        blt_type = [
            {'pos': (th.own.pln_mgr.char.rect.left - dx, th.own.pln_mgr.char.rect.top + dy),
             'ang': ang},
            {'pos': (th.own.pln_mgr.char.rect.right + dx, th.own.pln_mgr.char.rect.top + dy),
             'ang': -ang}
        ]

        for blt_info in blt_type:
            pos = blt_info['pos']
            ang = blt_info['ang']

            blt = BaseShape(2, 15, 0,
                            (45, 194, 229), 1, "blt")

            blt.rect.center = pos
            blt.curr_ang = ang
            blt.spd = 16
            blt.damage = 4

            th.own.blt_grp.add(blt)

    def upd_blts(th):
        for blt in th.own.blt_grp:
            if blt.type in ("blt", "blt-cros"):
                rot(blt)
                mv(blt, blt.spd)