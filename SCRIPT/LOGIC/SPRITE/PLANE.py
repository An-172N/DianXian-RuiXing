# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import pygame

import SCRIPT.GLOBAL as GLOBAL
import SCRIPT.FUNC as FUNC


def move_plane() -> None:
    if GLOBAL.move_right:
        GLOBAL.main_char.rect.x += 1.5 if GLOBAL.is_slow else 3.5
    if GLOBAL.move_left:
        GLOBAL.main_char.rect.x -= 1.5 if GLOBAL.is_slow else 3.5

    if GLOBAL.main_char.rect.left < GLOBAL.window.left:
        GLOBAL.main_char.rect.left = GLOBAL.window.left
    elif GLOBAL.main_char.rect.right > GLOBAL.window.right:
        GLOBAL.main_char.rect.right = GLOBAL.window.right

    GLOBAL.decision_point.rect.center = GLOBAL.main_char.rect.center


def turn_side() -> None:
    turn_side_image = GLOBAL.main_char.original_image.subsurface((12, 0, 12, 26))
    flipped_image = pygame.transform.flip(turn_side_image, True, False)

    if GLOBAL.move_right:
        GLOBAL.main_char.image = flipped_image
    elif GLOBAL.move_left:
        GLOBAL.main_char.image = turn_side_image
    else:
        GLOBAL.main_char.image = GLOBAL.main_char.original_image.subsurface((0, 0, 12, 26))


def collide_barrage() -> None:
    GLOBAL.collide = True


def life_logic() -> None:
    GLOBAL.no_hurt = 0
    GLOBAL.player -= 1
    GLOBAL.s_flash += 1

    if GLOBAL.player == 0:
        GLOBAL.save = True
        GLOBAL.is_blit = False


def invinc() -> None:
    if GLOBAL.is_s_divide or GLOBAL.collide:
        GLOBAL.cooldown_timer += 1

        if GLOBAL.cooldown_timer >= 180:
            if GLOBAL.is_s_divide:
                GLOBAL.is_s_divide = False
                GLOBAL.collide = False
                GLOBAL.cooldown_timer = 0
                GLOBAL.main_char.bullet_counter = 0
                GLOBAL.main_char.bullet_timer = 0
                GLOBAL.total_s_power = 0

            GLOBAL.collide = False
        else:
            GLOBAL.is_visitable = FUNC.digital(GLOBAL.cooldown_timer, 12, 0.5)
    else:
        GLOBAL.cooldown_timer = 0
        GLOBAL.is_visitable = True