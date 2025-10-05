import BRICK


class RectRaining:
    def __init__(th, own):
        th.own = own

        th.bomb_cnt = 0
        th.ctr = 0

    def free(th):
        th.ctr += 1

        if (th.ctr >= 60 and
            th.ctr % 1 == 0 and
            th.bomb_cnt < 6):
            for i in range(120, 466, 15):
                blt = BRICK.BaseShape(15, 15, 0,
                                      (45, 194, 229), 1)

                blt.rect.center = (i, 0)
                blt.spd = -24
                if not hasattr(blt, "dmg"):
                    blt.dmg = 6

                th.own.own.blt_grp.add(blt)

            th.bomb_cnt += 1

    def fire(th, dx, dy, ang):
        blt_type = [
            {'x': th.own.own.pln_mgr.char.rect.left - dx,
             'y': th.own.own.pln_mgr.char.rect.top + dy,
             'ang': ang},
            {'x': th.own.own.pln_mgr.char.rect.right + dx,
             'y': th.own.own.pln_mgr.char.rect.top + dy,
             'ang': -ang}
        ]

        for blt_info in blt_type:
            blt = BRICK.BaseShape(2, 15, 0,
                                  (45, 194, 229), 1)

            blt.rect.center = (blt_info['x'], blt_info['y'])
            blt.curr_ang = blt_info['ang']
            blt.spd = 16
            if not hasattr(blt, "dmg"):
                blt.dmg = 4

            th.own.own.blt_grp.add(blt)