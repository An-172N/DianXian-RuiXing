import random

import pygame

import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


def move_plane() -> None:
    if VARIABLE.move_right:
        VARIABLE.main_char.rect.x += 1 if VARIABLE.is_slow else 3
    if VARIABLE.move_left:
        VARIABLE.main_char.rect.x -= 1 if VARIABLE.is_slow else 3

    if VARIABLE.main_char.rect.left < VARIABLE.window.left:
        VARIABLE.main_char.rect.left = VARIABLE.window.left
    elif VARIABLE.main_char.rect.right > VARIABLE.window.right:
        VARIABLE.main_char.rect.right = VARIABLE.window.right

    VARIABLE.d_pt.rect.center = VARIABLE.main_char.rect.center


def turn_side() -> None:
    turn_side_image = VARIABLE.main_char.original_image.subsurface(
        (
            12,
            0,
            12,
            26
        )
    )
    flipped_image = pygame.transform.flip(
        turn_side_image,
        True,
        False
    )

    if VARIABLE.move_right:
        VARIABLE.main_char.image = flipped_image
    elif VARIABLE.move_left:
        VARIABLE.main_char.image = turn_side_image
    else:
        VARIABLE.main_char.image = VARIABLE.main_char.original_image.subsurface(
            (
                0,
                0,
                12,
                26
            )
        )


def collide_barrage(barrage) -> None:
    if (
        not (
            VARIABLE.collide or
            VARIABLE.is_s_divide
        )
    ):
        VARIABLE.collide = True
        life_logic()

    barrage.kill()


def life_logic() -> None:
    rands = random.randint(0, 30)
    for i in range(0 + rands, 360 + rands, 60):
        sprite = Base(
            (8, 8, 0),
            VARIABLE.main_char.color,
            1
        )
        sprite.speed = random.randint(8, 12)
        sprite.rect.center = VARIABLE.main_char.rect.center
        sprite.current_angle = i
        VARIABLE.particle_group.add(sprite)
        
    VARIABLE.no_hurt = 0
    VARIABLE.player -= 1
    VARIABLE.s_flash += 1

    if VARIABLE.player == 0:
        VARIABLE.save = True


def invinc() -> None:
    if (
        VARIABLE.is_s_divide or
        VARIABLE.collide
    ):
        VARIABLE.cooldown_time += 1

        if VARIABLE.cooldown_time >= 180:
            if VARIABLE.is_s_divide:
                VARIABLE.is_s_divide = False
                VARIABLE.collide = False
                VARIABLE.cooldown_time = 0
                VARIABLE.main_char.bomb.bomb_cnt = 0
                VARIABLE.main_char.bomb.timer = 0
                VARIABLE.total_s_power = 0

            VARIABLE.collide = False
        else:
            VARIABLE.is_visitable = (VARIABLE.cooldown_time // 6) % 2
    else:
        VARIABLE.cooldown_time = 0
        VARIABLE.is_visitable = True