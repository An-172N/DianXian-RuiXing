import random as rand

import pygame as pyg

import SCRIPT.VARIABLE

from SCRIPT.LOGIC.FRIEND import Base


def mv_pln() -> None:
    if SCRIPT.VARIABLE.mv_right:
        SCRIPT.VARIABLE.main_char.rect.x += 1 if SCRIPT.VARIABLE.is_slow else 3
    if SCRIPT.VARIABLE.mv_left:
        SCRIPT.VARIABLE.main_char.rect.x -= 1 if SCRIPT.VARIABLE.is_slow else 3

    if SCRIPT.VARIABLE.main_char.rect.left < SCRIPT.VARIABLE.win.left:
        SCRIPT.VARIABLE.main_char.rect.left = SCRIPT.VARIABLE.win.left
    elif SCRIPT.VARIABLE.main_char.rect.right > SCRIPT.VARIABLE.win.right:
        SCRIPT.VARIABLE.main_char.rect.right = SCRIPT.VARIABLE.win.right

    SCRIPT.VARIABLE.d_pt.rect.center = SCRIPT.VARIABLE.main_char.rect.center


def turn_side() -> None:
    turn_side_image = SCRIPT.VARIABLE.main_char.orig_image.subsurface(
        (12,
         0,
         12,
         26
        )
    )
    flipped_image = pyg.transform.flip(
        turn_side_image,
        True,
        False
    )

    if SCRIPT.VARIABLE.mv_right:
        SCRIPT.VARIABLE.main_char.image = flipped_image
    elif SCRIPT.VARIABLE.mv_left:
        SCRIPT.VARIABLE.main_char.image = turn_side_image
    else:
        SCRIPT.VARIABLE.main_char.image = SCRIPT.VARIABLE.main_char.orig_image.subsurface(
            (0,
             0,
             12,
             26
            )
        )


def coll_brg(src) -> None:
    if (not (SCRIPT.VARIABLE.coll or
             SCRIPT.VARIABLE.is_sdivide)):
        SCRIPT.VARIABLE.coll = True
        life_lgc()

    src.kill()


def life_lgc() -> None:
    rands = rand.randint(0, 30)
    for i in range(0 + rands, 360 + rands, 45):
        spr = Base((8, 8, 0), SCRIPT.VARIABLE.main_char.clr, 1)
        spr.spd = rand.randint(8, 12)
        spr.rect.center = SCRIPT.VARIABLE.main_char.rect.center
        spr.curr_ang = i
        SCRIPT.VARIABLE.ptcl_grp.add(spr)
        
    SCRIPT.VARIABLE.no_hurt = 0
    SCRIPT.VARIABLE.player -= 1
    SCRIPT.VARIABLE.sflash += 1

    if SCRIPT.VARIABLE.player == 0:
        SCRIPT.VARIABLE.sav = True


def invinc() -> None:
    if (SCRIPT.VARIABLE.is_sdivide or
        SCRIPT.VARIABLE.coll):
        SCRIPT.VARIABLE.cd_ctr += 1

        if SCRIPT.VARIABLE.cd_ctr >= 180:
            if SCRIPT.VARIABLE.is_sdivide:
                SCRIPT.VARIABLE.is_sdivide = False
                SCRIPT.VARIABLE.coll = False
                SCRIPT.VARIABLE.cd_ctr = 0
                SCRIPT.VARIABLE.main_char.bomb.bomb_cnt = 0
                SCRIPT.VARIABLE.main_char.bomb.ctr = 0
                SCRIPT.VARIABLE.ttl_s_power = 0

            SCRIPT.VARIABLE.coll = False
        else:
            SCRIPT.VARIABLE.is_visitable = (SCRIPT.VARIABLE.cd_ctr // 6) % 2
    else:
        SCRIPT.VARIABLE.cd_ctr = 0
        SCRIPT.VARIABLE.is_visitable = True