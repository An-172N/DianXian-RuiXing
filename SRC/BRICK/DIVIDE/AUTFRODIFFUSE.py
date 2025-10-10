import math

import BRICK


class AutFroDiffuse:
    def __init__(th, proc):
        th.proc = proc

        th.bomb_cnt = 0
        th.ctr = 0
        th.dl = 0

    def free(th):
        th.ctr += 1

        if (th.ctr % 1 == 0 and
            th.bomb_cnt < 12):
            th.dl += 6

            for i in range(0 + th.dl, 360 + th.dl, 120):
                for j in range(0 + th.dl, 360 + th.dl, 90):
                    blt = BRICK.BaseShape(9, 9, 0,
                                          th.proc("get", "stg", "char").clr, 2)

                    blt.rect.center = (th.proc("get", "stg", "char").rect.centerx
                                       + 32 * math.cos(math.radians(i)),
                                       th.proc("get", "stg", "char").rect.centery
                                       + 32 * math.sin(math.radians(i)))
                    blt.curr_ang = j
                    blt.spd = 4

                    th.proc("get", "main", "brg_grp").add(blt)

            th.bomb_cnt += 1

    def fire(th):
        if th.bomb_cnt < 1:
            for i in range(0, 360, 15):
                blt = BRICK.BaseShape(9, 9, 0,
                                      th.proc("get", "stg", "char").clr, 2)

                blt.rect.center = th.proc("get", "stg", "char").rect.center
                blt.curr_ang = i
                blt.spd = 4

                th.proc("get", "main", "brg_grp").add(blt)

            th.bomb_cnt += 1