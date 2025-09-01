import pygame as pyg
import sys

from BRICKS.KLI import Kli
from BRICKS.BASESHAPE import BaseShape


class PlaneManager:
    def __init__(th, own):
        th.own = own

        th.mv_right = False
        th.mv_left = False
        th.is_visitable = True
        th.coll = False
        th.is_use_bomb = False
        th.is_wait_respwn = False

        th.char = Kli()
        th.dec_pt = BaseShape(4, 4, 0,
                              (112, 112, 112), 1)
        
        th.rst_pln()

    def rst_pln(th):
        th.char.rect.centerx = th.own.win.width // 2 + 120
        th.char.rect.y = 319
        th.own.pln_grp.add(th.char)
        th.own.pln_grp.add(th.dec_pt)

    def set_pln_spd(th, mod):
        th.char.pln_spd_mod = mod
        th.char.pln_spd = th.char.char_spd()

    def upd_pos(th):
        if th.mv_right:
            th.char.rect.x += th.char.pln_spd
        if th.mv_left:
            th.char.rect.x -= th.char.pln_spd

        th.dec_pt.rect.center = th.char.rect.center

        th.keep_pos()

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
                
    def life_lgc(th):
        ptcl_mgr = th.own.ptcl_mgr

        pln_grp = th.own.pln_grp

        if th.own.s_pt < 24:
            th.is_wait_respwn = True
            th.own.players -= 1
            th.own.no_hurt_cnt = 0

            ptcl_mgr.spwn_ptcl(th.char,
                               (255, 255, 255), (45, 194, 229))

            pln_grp.empty()

            if th.own.players == 0:
                sys.exit()
        else:
            th.own.s_pt -= 24
            th.own.no_hurt_cnt = 0

    def respwn(th):
        if th.is_wait_respwn and th.own.cooldown_ctr >= 30:
            th.rst_pln()

            th.is_wait_respwn = False
            th.own.cooldown_ctr = 0