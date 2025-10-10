import random as rand

import BRICK


class ParticleMgr:
    def __init__(th, proc):
        th.proc = proc

    def spwn_ptcl(th, sprite, wid, clr1, clr2=None):
        rands = rand.randint(0, 45)
        
        for i in range(0 + rands, 360 + rands, 45):
            clr = clr1 if clr2 == None else rand.choice([clr1, clr2])

            ptcl = BRICK.BaseShape(wid, wid, 0,
                                   clr, 1)
            
            ptcl.rect.center = sprite.rect.center
            ptcl.curr_ang = i
            ptcl.spd = rand.randint(6, 10)

            th.proc("get", "main", "ptcl_grp").add(ptcl)