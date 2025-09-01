import random as rand

from BRICKS.BASESHAPE import BaseShape


class WhiteBrickProcess:
    def __init__(th, own):
        th.own = own

    def circle_brc(th, brc):
        rands = rand.randint(0, 360)

        for i in range(0 + rands, 360 + rands, 45):
            blt = BaseShape(2, 15, 0,
                            (45, 194, 229), 1, 0)
            
            blt.rect.center = brc.rect.center
            blt.curr_ang = i
            blt.spd = 16
            blt.damage = 4

            th.own.blt_grp.add(blt)

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
            blt = BaseShape(2, 15, 0,
                            (45, 194, 229), 2, 0)

            blt.rect.center = blt_info['pos']
            blt.curr_ang = blt_info['ang']
            blt.spd = 16
            blt.damage = 6

            th.own.blt_grp.add(blt)

    def point_brc(th):
        for i in range(12):
            blt = BaseShape(2, 15, 0,
                            (45, 194, 229), 1, 0)
            
            blt.rect.center = (rand.randint(120, 465), rand.randint(15, 345))
            blt.curr_ang = rand.randint(0, 360)
            blt.spd = 16
            blt.damage = 4

            th.own.blt_grp.add(blt)