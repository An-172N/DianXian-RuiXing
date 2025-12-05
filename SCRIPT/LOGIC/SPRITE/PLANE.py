import random as rand

import pygame as pyg

import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


def mv_pln() -> None:
    if VARIABLE.mv_right:
        VARIABLE.main_char.rect.x += 1 if VARIABLE.is_slow else 3
    if VARIABLE.mv_left:
        VARIABLE.main_char.rect.x -= 1 if VARIABLE.is_slow else 3

    if VARIABLE.main_char.rect.left < VARIABLE.win.left:
        VARIABLE.main_char.rect.left = VARIABLE.win.left
    elif VARIABLE.main_char.rect.right > VARIABLE.win.right:
        VARIABLE.main_char.rect.right = VARIABLE.win.right

    VARIABLE.d_pt.rect.center = VARIABLE.main_char.rect.center


def turn_side() -> None:
    turn_side_image = VARIABLE.main_char.orig_image.subsurface(
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

    if VARIABLE.mv_right:
        VARIABLE.main_char.image = flipped_image
    elif VARIABLE.mv_left:
        VARIABLE.main_char.image = turn_side_image
    else:
        VARIABLE.main_char.image = VARIABLE.main_char.orig_image.subsurface(
            (0,
             0,
             12,
             26
            )
        )


def coll_brg(brg) -> None:
    if (not (VARIABLE.coll or
             VARIABLE.is_sdivide)):
        VARIABLE.coll = True
        life_lgc()

    brg.kill()


def life_lgc() -> None:
    rands = rand.randint(0, 30)
    for i in range(0 + rands, 360 + rands, 60):
        spr = Base((8, 8, 0), VARIABLE.main_char.clr, 1)
        spr.spd = rand.randint(8, 12)
        spr.rect.center = VARIABLE.main_char.rect.center
        spr.curr_ang = i
        VARIABLE.ptcl_grp.add(spr)
        
    VARIABLE.no_hurt = 0
    VARIABLE.player -= 1
    VARIABLE.sflash += 1

    if VARIABLE.player == 0:
        VARIABLE.sav = True


def invinc() -> None:
    if (VARIABLE.is_sdivide or
        VARIABLE.coll):
        VARIABLE.cd_ctr += 1

        if VARIABLE.cd_ctr >= 180:
            if VARIABLE.is_sdivide:
                VARIABLE.is_sdivide = False
                VARIABLE.coll = False
                VARIABLE.cd_ctr = 0
                VARIABLE.main_char.bomb.bomb_cnt = 0
                VARIABLE.main_char.bomb.ctr = 0
                VARIABLE.ttl_s_power = 0

            VARIABLE.coll = False
        else:
            VARIABLE.is_visitable = (VARIABLE.cd_ctr // 6) % 2
    else:
        VARIABLE.cd_ctr = 0
        VARIABLE.is_visitable = True