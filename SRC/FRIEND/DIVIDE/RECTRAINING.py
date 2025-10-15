from FUNC import BaseShape
from FUNC import Spawn


class RectRaining:
    def __init__(th, proc):
        th.proc = proc

        th.bomb_cnt = 0
        th.ctr = 0

        th.spr = BaseShape

    def free(th):
        th.ctr += 1

        if (th.ctr >= 60 and
            th.ctr % 1 == 0 and
            th.bomb_cnt < 6):
            for i in range(120, 466, 15):
                Spawn.spwn_spr(th.spr, None,
                               th.proc("get", "main", "blt_grp"),
                               (i, 0), (-24, -24), 6, 0,
                               (15, 15), 0, (45, 194, 229), 1)

            th.bomb_cnt += 1

    def fire(th, dx, dy, ang):
        blt_type = [
            {'x': th.proc("get", "pln", "char").rect.left - dx,
             'y': th.proc("get", "pln", "char").rect.top + dy,
             'ang': ang},
            {'x': th.proc("get", "pln", "char").rect.right + dx,
             'y': th.proc("get", "pln", "char").rect.top + dy,
             'ang': -ang}
        ]

        for blt_info in blt_type:
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "blt_grp"),
                           (blt_info['x'], blt_info['y']), (16, 16), 4, blt_info['ang'],
                           (2, 15), 0, (45, 194, 229), 1)