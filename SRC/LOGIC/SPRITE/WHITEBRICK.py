import random as rand

from FUNC import BaseShape
from FUNC import Spawn


class WhiteBrick:
    def __init__(th, proc):
        th.proc = proc

        th.spr = BaseShape

    def circle_brc(th, brc):
        rands = rand.randint(0, 45)

        for i in range(0 + rands, 360 + rands, 45):
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "blt_grp"),
                           brc.rect.center, (16, 16), 4, i,
                           (2, 15), 0, (45, 194, 229), 1, "blt")

    def rect_brc(th, brc):
        blt_index = [
            {'ang': 0,
             'pos': brc.rect.midleft},
            {'ang': 90,
             'pos': brc.rect.midbottom},
            {'ang': 180,
             'pos': brc.rect.midright},
            {'ang': 270,
             'pos': brc.rect.midtop}
        ]
    
        for blt_info in blt_index:
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "blt_grp"),
                           blt_info['pos'], (16, 16), 4, blt_info['ang'],
                           (2, 15), 0, (45, 194, 229), 1, "blt-cros")

    def polygon_brc(th, brc):
        blt_index = [
            {'ang': rand.choice([-30, -210]),
             'pos': brc.rect.midleft,},
            {'ang': rand.choice([30, 210]),
             'pos': brc.rect.midright},
            {'ang': rand.choice([90, 270]),
             'pos': brc.rect.midbottom}
        ]

        for blt_info in blt_index:
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "blt_grp"),
                           blt_info['pos'], (16, 16), 4, blt_info['ang'],
                           (2, 15), 0, (45, 194, 229), 1, "blt-cros")

    def line_brc(th, brc):
        for i in range(-90, 91, 15):
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "blt_grp"),
                           brc.rect.center, (16, 16), 8, i,
                           (2, 15), 0, (45, 194, 229), 1, "blt")

    def point_brc(th):
        for i in range(12):
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "blt_grp"),
                           (rand.randint(120, 465), rand.randint(15, 345)), (16, 16), 4, rand.randint(0, 360),
                           (2, 15), 0, (45, 194, 229), 1, "blt")
            
    def brc_death(th, brc, brc_pos):
        if brc.clr == th.proc("get", "main", "clr")[6]:
            proc_dict = {
                0: th.polygon_brc,
                1: th.rect_brc,
                2: th.circle_brc,
                3: th.point_brc,
                4: th.line_brc
            }

            proc_dict[brc.shape](brc)

        if rand.random() <= 0.32:
            tupl = rand.choice([(0, 1, 1), (-30, 31, 30)])
            for i in range(tupl[0], tupl[1], tupl[2]):
                Spawn.spwn_spr(th.spr, th.proc("get", "pln", "char"),
                               th.proc("get", "main", "brg_grp"),
                               brc_pos, (2, 2), 0, i,
                               (9, 9), 0, brc.clr, brc.shape)