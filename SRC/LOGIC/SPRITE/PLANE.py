import random as rand

import pygame as pyg

from FRIEND import Kli
from FUNC import Spawn
from FUNC import BaseShape


class PlaneMgr:
    def __init__(th, proc):
        th.proc = proc

        th.plyr = 4
        th.spt = 16
        th.ttl_spt = 0
        th.no_hurt = 0
        th.sc = 0
        th.cd_ctr = 0

        th.mv_right = False
        th.mv_left = False
        th.is_slow = False
        th.is_visitable = True
        th.is_sdivide = False
        th.coll = False

        th.char = Kli(th.proc)

    def spwn_pln(th):
        Spawn.shhm_spwn(th.char, th.proc("get", "main", "pln_grp"),
                        (292, 331))
    
    def mv_pln(th):
        if th.mv_right:
            th.char.rect.x += 1 if th.is_slow else 4
        if th.mv_left:
            th.char.rect.x -= 1 if th.is_slow else 4

        if th.char.rect.left < th.proc("get", "main", "win").left:
            th.char.rect.left = th.proc("get", "main", "win").left
        elif th.char.rect.right > th.proc("get", "main", "win").right:
            th.char.rect.right = th.proc("get", "main", "win").right
    
    def turn_side(th):
        turn_side_image = th.char.orig_image.subsurface((12, 0,
                                                         12, 26))
        flipped_image = pyg.transform.flip(turn_side_image,
                                           True, False)

        if th.mv_right:
            th.char.image = flipped_image
        elif th.mv_left:
            th.char.image = turn_side_image
        else:
            th.char.image = th.char.orig_image.subsurface((0, 0,
                                                           12, 26))
            
    def coll_brg(th, src, _):
        if (not (th.coll or
                 th.is_sdivide)):
            th.coll = True
            th.life_lgc()

        src.kill()

    def life_lgc(th):
        ptcl = BaseShape
        rands = rand.randint(0, 30)
        for i in range(0 + rands, 360 + rands, 45):
            Spawn.spwn_spr(ptcl, None,
                           th.proc("get", "main", "ptcl_grp"),
                           th.char.rect.center, (8, 12), 0, i,
                           (8, 8), 0, th.char.clr, 1)
        
        th.no_hurt = 0
        th.plyr -= 1

        if th.plyr == 0:
            th.proc("sw", "main", "sav",
                    True)

    def invinc(th):
        if (th.is_sdivide or
            th.coll):
            th.cd_ctr += 1

            if th.cd_ctr >= 240:
                if th.is_sdivide:
                    th.is_sdivide = False
                    for evt in th.proc("rst1", "blt"):
                        th.proc("rst1", "blt", evt)

                th.coll = False
            else:
                th.is_visitable = (th.cd_ctr // 6) % 2
        else:
            th.cd_ctr = 0
            th.is_visitable = True