from BRICK.BASE.BASESHAPE import BaseShape

from SDIVIDE.KLI.RECTRAINER import RectRainer

from LOGIC.PROCESS.MOVE import mv
from LOGIC.PROCESS.MOVE import rot


class Bullet:
    def __init__(th, own):
        th.own = own

        th.rect_rain = RectRainer(th)

        th.fusil_cnt = 0

        th.is_cnt_fusil = False

    def spwn_blts(th):
        th.own.ptcl_mgr.spwn_ptcl(th.own.pln_mgr.char,
                                  (45, 194, 229))

        p = 2 ** (th.own.pln_mgr.s_pt // 48)

        for i in range(0, p):
            for j in range(-8, 9, 8):
                th.k_blt(0 + i * 10, 0 + i * 12,
                         j)

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
            blt.dmg = 4

            th.own.blt_grp.add(blt)

    def upd_blts(th):
        for blt in th.own.blt_grp:
            if blt.type == "blt":
                rot(blt)
                mv(blt, blt.spd)