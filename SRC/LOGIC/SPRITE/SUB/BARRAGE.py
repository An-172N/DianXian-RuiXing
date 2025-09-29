from BRICK.BASE.TWOBASE import TwoBase

from LOGIC.TOOL import ang


class BarrageMgr:
    def __init__(th, own):
        th.own = own

    def one_brg(th, spr):
        brg = TwoBase(9, 9, 0,
                      spr.clr, spr.shape,
                      "brc-brg")

        brg.rect.center = spr.rect.center
        brg.curr_ang = ang(th.own.pln_mgr.char, brg)

        th.own.brg_grp.add(brg)

    def cir_brg(th, spr):
        for i in range(-30, 31, 30):
            brg = TwoBase(9, 9, 0,
                          spr.clr, spr.shape,
                          "brc-brg")

            brg.rect.center = spr.rect.center
            brg.curr_ang = ang(th.own.pln_mgr.char, brg) + i

            th.own.brg_grp.add(brg)