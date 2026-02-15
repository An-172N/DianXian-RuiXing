# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import argparse
import json
import random

import pygame

import PRELOAD
from LOGIC import Tool, Plane, Stage, Item, File
from SCRIPT import HUMAN, SPRITE, GLOBAL, GUI, KEY, COLLIDE


def option() -> None:
    clamp = Tool.clamp
    parser = argparse.ArgumentParser()

    parser.add_argument('-stage', type=int, default=1)
    parser.add_argument('-level', type=int, default=0)
    parser.add_argument('-flash', type=int, default=3)
    parser.add_argument('-power', type=int, default=0)

    args = parser.parse_args()

    GLOBAL.stage = int(clamp(args.stage, 1, 4))
    GLOBAL.level = int(clamp(args.level, 0, 5))
    GLOBAL.flash = int(clamp(args.flash, 0, 96))
    GLOBAL.power = int(clamp(args.power, 0, 32))
    GLOBAL.second_background = PRELOAD.picture[GLOBAL.stage]


def sprite_loader() -> None:
    if GLOBAL.level == 6:
        GLOBAL.char = choose_human()
        GLOBAL.text = json.loads(PRELOAD.asset(f"ASSET\JSON\TALK_{GLOBAL.stage}.json").decode('utf-8'))
        GLOBAL.is_talk = True
        GLOBAL.is_blit = False

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        File.read_level(PRELOAD.asset(f"ASSET\STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg"), SPRITE.Brick.load_brick, PRELOAD.color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)

        SPRITE.Brick.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)


def choose_human() -> HUMAN.Ono | HUMAN.Hro | HUMAN.Nre | HUMAN.Qdi:
    char_dict = {
        1: HUMAN.Ono,
        2: HUMAN.Hro,
        3: HUMAN.Nre,
        4: HUMAN.Qdi
    }

    return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group, GLOBAL.particle_group, GLOBAL.main_char.rect.center)


def update(clock: pygame.time.Clock, screen: pygame.Surface) -> None:
    option()

    sprite_item = SPRITE.Item
    remove_sprite = COLLIDE.remove_sprite
    window = GLOBAL.window

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                main_char = GLOBAL.main_char
                decision_point = GLOBAL.decision_point

                if GLOBAL.is_s_divide:
                    main_char.free()

                main_char.image = Plane.turn_side(main_char.original_image.subsurface((0, 0, 12, 26)), main_char.original_image.subsurface((12, 0, 12, 26)), GLOBAL.is_move_right, GLOBAL.is_move_left)
                main_char.rect.x, main_char.rect.centery = Plane.move_plane((main_char.rect.x, main_char.rect.centery), (4, 8), (331, 332), GLOBAL.is_move_left, GLOBAL.is_move_right, GLOBAL.is_fast)
                keep_position = Plane.keep_position(window.left, window.right, main_char.rect.center)
                main_char.rect.center = keep_position
                decision_point.rect.center = keep_position

                if hasattr(GLOBAL.char, "target_pos"):
                    GLOBAL.char.target_pos = main_char.rect.center

                COLLIDE.barrage_collide(main_char.rect.center)
                GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer = Plane.invinc(GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer, 180, 6, main_char.reset_bullet)

                GLOBAL.item_spawn_timer = sprite_item.item_spawn(GLOBAL.item_group, GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0, (random.randint(120, 465), 10), -2, "fire", GLOBAL.item_spawn_timer)
                if GLOBAL.combo_timer <= 1 and GLOBAL.combo > 0:
                    sprite = SPRITE.Text.Text(2 ** GLOBAL.combo, main_char.rect.midtop, (128, 128, 128))
                    GLOBAL.text_group.add(sprite)
                GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score = Item.combo_counter(GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()
                GLOBAL.text_group.update()

                remove_sprite(GLOBAL.bullet_group, GLOBAL.effective)
                remove_sprite(GLOBAL.barrage_group, GLOBAL.effective)
                remove_sprite(GLOBAL.item_group, GLOBAL.effective)
                remove_sprite(GLOBAL.particle_group, GLOBAL.effective)

                COLLIDE.bullet_collide()
                COLLIDE.item_collide()

            if not GLOBAL.is_level_load:
                GLOBAL.wait_level_load_timer, GLOBAL.is_level_load = Stage.load_level(GLOBAL.wait_level_load_timer, GLOBAL.is_level_load, 60, sprite_loader)
            elif len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                GLOBAL.is_summary = True
                GLOBAL.is_blit = False

        KEY.key_event()

        GUI.display(screen, clock)

        pygame.display.flip()
        clock.tick(60)