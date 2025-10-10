import pygame as pyg

import BRICK


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

        th.char = BRICK.Kli(th.proc)

    def spwn_pln(th):
        th.char.rect.center = (292, 331)
        th.proc("get", "main", "pln_grp").add(th.char)
    
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
            
    def coll_brg(th, _, __):
        if (not (th.coll or
                 th.is_sdivide)):
            th.coll = True
            th.life_lgc()

    def life_lgc(th):
        th.proc("func", "ptcl", "ptcl")(th.char, 6,
                                        th.char.clr, th.proc("get", "main", "clr")[6])
        
        th.no_hurt = 0
        th.plyr -= 1

        if th.plyr == 0:
            th.proc("sw", "main", "sav", True)

    def invinc(th):
        if (th.is_sdivide or
            th.coll):
            th.cd_ctr += 1

            if th.cd_ctr >= 256:
                if th.is_sdivide:
                    th.is_sdivide = False
                    for evt in th.proc("rst1", "blt"):
                        if evt != "fusil_cnt":
                            th.proc("rst1", "blt", evt)

                th.coll = False
            else:
                th.is_visitable = (th.cd_ctr // 6) % 2
        else:
            th.cd_ctr = 0
            th.is_visitable = True