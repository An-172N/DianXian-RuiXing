# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import argparse
import json
import random
import os

import pygame

import LOGIC
from SCRIPT import HUMAN, SPRITE, GLOBAL, GUI, KEY, COLLIDE


def option() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument('--stage', type=int, default=1)
    parser.add_argument('--level', type=int, default=0)
    parser.add_argument('--flash', type=int, default=3)
    parser.add_argument('--power', type=int, default=0)

    args = parser.parse_args()

    GLOBAL.stage = int(LOGIC.FUNC.clamp(args.stage, 1, 4))
    GLOBAL.level = int(LOGIC.FUNC.clamp(args.level, 0, 5))
    GLOBAL.flash = int(LOGIC.FUNC.clamp(args.flash, 0, 96))
    GLOBAL.power = int(LOGIC.FUNC.clamp(args.power, 0, 32))
    GLOBAL.second_background = GLOBAL.picture[GLOBAL.stage]
    GLOBAL.second_background.set_alpha(128)


def sprite_loader() -> None:
    if GLOBAL.level == 6:
        GLOBAL.char = chs_shhm()
        with open(os.path.join(GLOBAL.asset_path, f"JSON\TALK_{GLOBAL.stage}.json"), 'r', encoding="utf-8") as f:
            GLOBAL.text = json.load(f)
        GLOBAL.is_talk = True
        GLOBAL.is_blit = False

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        LOGIC.File.read_level(
            os.path.join(GLOBAL.asset_path, f"STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg"),
            SPRITE.Brick.load_brick,
            GLOBAL.color_dict[GLOBAL.stage],
            4,
            0.031,
            (127, 22),
            (15, 15),
            GLOBAL.brick_group
        )

        SPRITE.Brick.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)


def chs_shhm() -> HUMAN.Ono | HUMAN.Hro | HUMAN.Nre | HUMAN.Qdi:
    char_dict = {
        1: HUMAN.Ono,
        2: HUMAN.Hro,
        3: HUMAN.Nre,
        4: HUMAN.Qdi,
    }

    if GLOBAL.stage in [2, 3, 4]:
        return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group, GLOBAL.particle_group, GLOBAL.main_char.rect.center)
    else:
        return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group, GLOBAL.particle_group)


def update(clock: pygame.time.Clock, screen: pygame.Surface, _: None) -> None:
    option()

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if GLOBAL.is_s_divide:
                    GLOBAL.main_char.free()

                GLOBAL.main_char.image = LOGIC.Plane.turn_side(
                    GLOBAL.main_char.original_image.subsurface((0, 0, 12, 26)),
                    GLOBAL.main_char.original_image.subsurface((12, 0, 12, 26)),
                    GLOBAL.is_move_right,
                    GLOBAL.is_move_left
                )
                GLOBAL.main_char.rect.x, GLOBAL.main_char.rect.centery = LOGIC.Plane.move_plane(
                    (GLOBAL.main_char.rect.x, GLOBAL.main_char.rect.centery),
                    (4, 8),
                    (331, 332),
                    GLOBAL.is_move_left,
                    GLOBAL.is_move_right,
                    GLOBAL.is_fast
                )
                keep_position = LOGIC.Plane.keep_position(
                    GLOBAL.window.left,
                    GLOBAL.window.right,
                    GLOBAL.main_char.rect.center
                )
                GLOBAL.main_char.rect.center = keep_position
                GLOBAL.decision_point.rect.center = keep_position

                if hasattr(GLOBAL.char, "target_pos"):
                    GLOBAL.char.target_pos = GLOBAL.main_char.rect.center

                COLLIDE.barrage_collide(GLOBAL.main_char.rect.center)
                GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer = LOGIC.Plane.invinc(
                    GLOBAL.is_s_divide,
                    GLOBAL.is_collide,
                    GLOBAL.is_visitable,
                    GLOBAL.cooldown_timer,
                    180,
                    6,
                    GLOBAL.main_char.reset_bullet
                )
                
                GLOBAL.item_spawn_timer = SPRITE.Item.item_spawn(
                    GLOBAL.item_group,
                    GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0,
                    (random.randint(120, 465), 10),
                    -2,
                    (255, 255, 255),
                    "fire",
                    GLOBAL.item_spawn_timer
                )
                GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score = LOGIC.Item.combo_counter(
                    GLOBAL.combo_timer,
                    GLOBAL.combo,
                    GLOBAL.score,
                    2 ** GLOBAL.combo,
                    120
                )
            
                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()

                COLLIDE.remove_sprite(GLOBAL.bullet_group, GLOBAL.effective)
                COLLIDE.remove_sprite(GLOBAL.barrage_group, GLOBAL.effective)
                COLLIDE.remove_sprite(GLOBAL.item_group, GLOBAL.effective)
                COLLIDE.remove_sprite(GLOBAL.particle_group, GLOBAL.effective)

                COLLIDE.bullet_collide()
                COLLIDE.item_collide()

            if not GLOBAL.is_level_load:
                GLOBAL.wait_level_load_timer, GLOBAL.is_level_load =LOGIC.Stage.level_load(
                    GLOBAL.wait_level_load_timer,
                    GLOBAL.is_level_load,
                    60,
                    sprite_loader
                )
            elif len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                GLOBAL.is_summary = True
                GLOBAL.is_blit = False

        KEY.key_event()

        GUI.window_display(screen)
        GUI.menu_display(screen)
        GUI.font_display(screen, clock)

        pygame.display.flip()
        clock.tick(60)