import BRICK
import TOOL


class BarrageMgr:
    def __init__(th, proc):
        th.proc = proc

    def spwn_brg(th, spr, tupl):
        for i in range(tupl[0], tupl[1], tupl[2]):
            brg = BRICK.BaseShape(9, 9, 0,
                                  spr.clr, spr.shape)

            brg.rect.center = spr.rect.center
            brg.curr_ang = TOOL.ang(th.proc("get", "pln", "char"), brg) + i
            brg.spd = 2

            th.proc("get", "main", "brg_grp").add(brg)