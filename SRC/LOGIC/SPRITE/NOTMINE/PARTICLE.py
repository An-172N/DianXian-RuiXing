import random as rand

from BRICK.BASE.BASESHAPE import BaseShape

from TOOL import mv


class Particle:
    def __init__(th, own):
        th.own = own

    def spwn_ptcl(th, sprite, clr1, clr2=None):
        rands = rand.randint(0, 360)
        
        for i in range(0 + rands, 360 + rands, 30):
            if clr2 is None:
                clr = clr1
            else:
                clr = rand.choice([clr1, clr2])

            ptcl = BaseShape(2, 2, 0,
                             clr, 1)
            ptcl.rect.center = sprite.rect.center

            ptcl.curr_ang = i
            ptcl.spd = rand.randint(4, 8)

            th.own.ptcl_grp.add(ptcl)

    def upd(th):
        [mv(ptcl, ptcl.spd) for ptcl in th.own.ptcl_grp]