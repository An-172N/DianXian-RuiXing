import pygame as pyg

import BRICK


class PlaneMgr:
    def __init__(th, own):
        th.own = own

        th.plyr = 4
        th.s_pt = 16
        th.ttl_s_pt = 0
        th.no_hurt_cnt = 0
        th.cd_ctr = 0

        th.mv_right = False
        th.mv_left = False
        th.is_slow = False
        th.is_visitable = True
        th.is_use_sdivide = False
        th.coll = False

        th.char = BRICK.Kli(th.own, th)

    def spwn_pln(th):
        th.char.rect.center = (292, 331)
        th.own.pln_grp.add(th.char)
    
    def mv_pln(th):
        if th.mv_right:
            th.char.rect.x += 1 if th.is_slow else 4
        if th.mv_left:
            th.char.rect.x -= 1 if th.is_slow else 4

        if th.char.rect.left < th.own.win.left:
            th.char.rect.left = th.own.win.left
        elif th.char.rect.right > th.own.win.right:
            th.char.rect.right = th.own.win.right
    
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
                 th.is_use_sdivide)):
            th.coll = True
            th.life_lgc()

    def life_lgc(th):
        th.own.ptcl_mgr.spwn_ptcl(th.char, 6,
                                  th.char.clr, th.own.clr_dict[6])
        
        th.no_hurt_cnt = 0
        th.plyr -= 1

        if th.plyr == 0:
            th.own.sav = True

    def invinc(th):
        if (th.is_use_sdivide or
            th.coll):
            th.cd_ctr += 1

            if th.cd_ctr >= 256:
                if th.is_use_sdivide:
                    th.is_use_sdivide = False
                    th.own.rst_mgr.rst_bomb()

                th.coll = False
            else:
                th.is_visitable = (th.cd_ctr // 6) % 2
        else:
            th.cd_ctr = 0
            th.is_visitable = True