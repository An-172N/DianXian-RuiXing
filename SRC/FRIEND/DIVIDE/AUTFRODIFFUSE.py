import math

from FUNC import BaseShape
from FUNC import Spawn


class AutFroDiffuse:
    def __init__(th, proc):
        th.proc = proc

        th.bomb_cnt = 0
        th.ctr = 0
        th.dl = 0

        th.spr = BaseShape

    def free(th):
        th.ctr += 1

        if (th.ctr % 1 == 0 and
            th.bomb_cnt < 12):
            th.dl += 6

            for i in range(0 + th.dl, 360 + th.dl, 120):
                for j in range(0 + th.dl, 360 + th.dl, 90):
                    pos = (th.proc("get", "stg", "char").rect.centerx
                           + 32 * math.cos(math.radians(i)),
                           th.proc("get", "stg", "char").rect.centery
                           + 32 * math.sin(math.radians(i)))

                    Spawn.spwn_spr(th.spr, None,
                                   th.proc("get", "main", "brg_grp"),
                                   pos, (4, 4), 0, j,
                                   (9, 9), 0, th.proc("get", "stg", "char").clr, 2)

            th.bomb_cnt += 1

    def fire(th):
        if th.bomb_cnt < 1:
            pos = th.proc("get", "stg", "char").rect.center
            for i in range(0, 360, 15):
                Spawn.spwn_spr(th.spr, None,
                               th.proc("get", "main", "brg_grp"),
                               pos, (4, 4), 0, i,
                               (9, 9), 0, th.proc("get", "stg", "char").clr, 2)

            th.bomb_cnt += 1