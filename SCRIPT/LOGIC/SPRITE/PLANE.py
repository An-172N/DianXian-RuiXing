# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import pygame

from SCRIPT import GLOBAL


def move_plane() -> None:
    main_char_rect = GLOBAL.main_char.rect

    if GLOBAL.is_move_right:
        main_char_rect.x += 8 if GLOBAL.is_fast else 4
    if GLOBAL.is_move_left:
        main_char_rect.x -= 8 if GLOBAL.is_fast else 4


def keep_position() -> None:
    main_char_rect = GLOBAL.main_char.rect
    decision_point_rect = GLOBAL.decision_point.rect

    if main_char_rect.left < GLOBAL.window.left:
        main_char_rect.left = GLOBAL.window.left
    elif main_char_rect.right > GLOBAL.window.right:
        main_char_rect.right = GLOBAL.window.right

    decision_point_rect.center = main_char_rect.center


def turn_side() -> None:
    main_char = GLOBAL.main_char
    turn_side_image = main_char.original_image.subsurface((12, 0, 12, 26))
    flipped_image = pygame.transform.flip(turn_side_image, True, False)

    if GLOBAL.is_move_right:
        main_char.image = flipped_image
    elif GLOBAL.is_move_left:
        main_char.image = turn_side_image
    else:
        main_char.image = main_char.original_image.subsurface((0, 0, 12, 26))


def collide_barrage() -> None:
    GLOBAL.is_collide = True


def life_logic() -> None:
    GLOBAL.no_hurt = 0
    GLOBAL.flash -= 1
    GLOBAL.use_flash += 1

    if GLOBAL.flash == 0:
        GLOBAL.is_save = True
        GLOBAL.is_blit = False


def invinc() -> None:
    main_char = GLOBAL.main_char

    if GLOBAL.is_s_divide or GLOBAL.is_collide:
        GLOBAL.cooldown_timer += 1

        if GLOBAL.cooldown_timer >= 180:
            if GLOBAL.is_s_divide:
                GLOBAL.is_s_divide = False
                GLOBAL.is_collide = False
                GLOBAL.cooldown_timer = 0

                main_char.bullet_counter = 0
                main_char.bullet_timer = 0

            GLOBAL.is_collide = False
        else:
            GLOBAL.is_visitable = (GLOBAL.cooldown_timer // 6) % 2
    else:
        GLOBAL.cooldown_timer = 0
        GLOBAL.is_visitable = True