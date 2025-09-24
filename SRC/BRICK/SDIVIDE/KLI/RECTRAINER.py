from BRICK.BASE.BASESHAPE import BaseShape

from TOOL import mv


class RectRainer:
    def __init__(th, own):
        th.own = own

        th.ctr = 0
        th.cnt = 0

    def spwn_rect(th):
        th.ctr += 1

        if (th.ctr >= 60 and
            th.ctr % 2 == 0 and
            th.cnt < 6):
            for i in range(120, 466, 15):
                blt = BaseShape(15, 15, 0,
                                (45, 194, 229), 1, "bomb")

                blt.spd = -24
                blt.dmg = 6

                blt.rect.center = (i, 0)

                th.own.own.blt_grp.add(blt)
            
            th.cnt += 1

    def upd_rect(th):
        for blt in th.own.own.blt_grp:
            if blt.type == "bomb":
                mv(blt, blt.spd)

    def rst_bomb(th):
        th.cnt = 0
        th.ctr = 0