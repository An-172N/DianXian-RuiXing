import pygame as pyg

from BRICK.HUMAN.KLI import Kli


class Plane:
    def __init__(th, own):
        th.own = own

        th.plyr = 1
        th.s_pt = 80
        th.ttl_s_pt = 0
        th.no_hurt_cnt = 0

        th.mv_right = False
        th.mv_left = False
        th.is_visitable = True
        th.coll = False
        th.is_use_sdivide = False
        th.is_wait_respwn = False

        th.char = Kli()
        
        th.rst_pln()

    def rst_pln(th):
        th.char.rect.center = (292, 331)

        th.own.pln_grp.add(th.char)

    def set_pln_spd(th, mod):
        th.char.pln_spd_mod = mod
        th.char.pln_spd = th.char.char_spd()

    def upd_pos(th):
        if th.mv_right:
            th.char.rect.x += th.char.pln_spd
        if th.mv_left:
            th.char.rect.x -= th.char.pln_spd

    def keep_pos(th):
        if th.char.rect.left < th.own.win.left:
            th.char.rect.left = th.own.win.left
        elif th.char.rect.right > th.own.win.right:
            th.char.rect.right = th.own.win.right

    def upd_size(th):
        turn_side_image = th.char.orig_image.subsurface((12, 0,
                                                         12, 26))
        flipped_image = pyg.transform.flip(turn_side_image,
                                           True, False)

        if th.is_visitable:
            if th.mv_right:
                th.char.image = flipped_image
            elif th.mv_left:
                th.char.image = turn_side_image
            else:
                th.char.image = th.char.orig_image.subsurface((0, 0,
                                                               12, 26))