import random as rand

from BRICK.BASE.PARTICLE import Particle


class ParticleMgr:
    def __init__(th, own):
        th.own = own

    def spwn_ptcl(th, sprite, wid, clr1, clr2=None):
        rands = rand.randint(0, 360)
        
        for i in range(0 + rands, 360 + rands, 30):
            clr = clr1 if clr2 is None else rand.choice([clr1, clr2])

            ptcl = Particle(wid, clr)
            
            ptcl.rect.center = sprite.rect.center
            ptcl.curr_ang = i
            ptcl.spd = rand.randint(6, 10)

            th.own.ptcl_grp.add(ptcl)