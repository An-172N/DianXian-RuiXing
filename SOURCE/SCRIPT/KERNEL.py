# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import json
from random import randint


import pygame


from PRELOAD import picture, window, asset, color_dict, text_cache
from LOGIC.TOOL import clamp
from LOGIC.PLANE import turn_side, move_plane, invinc
from LOGIC.ITEM import item_spawn, combo_counter
from LOGIC.SPRITE import Text
from LOGIC.STAGE import load_level
from LOGIC.FILE import read_level


def update(clock: pygame.time.Clock, screen: pygame.Surface, *args: tuple) -> None:
    from SCRIPT import GUI, KEY, COLLIDE, GLOBAL
    from SCRIPT.SPRITE import Item, Brick
    from SCRIPT.HUMAN import Ono, Hro, Nre, Qdi

    def sprite_loader() -> None:
        if GLOBAL.level == 6:
            GLOBAL.char = choose_human()
            GLOBAL.text = json.loads(asset(rf"ASSET\JSON\TALK_{GLOBAL.stage}.json").decode('utf-8'))
            GLOBAL.is_talk = True

            GLOBAL.brick_group.add(GLOBAL.char)
        else:
            read_level(asset(rf"ASSET\STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg"), Brick.load_brick, color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)
            Brick.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)

        GLOBAL.animate_timer = 0


    def choose_human() -> Ono | Hro | Nre | Qdi:
        char_dict = {
            1: Ono,
            2: Hro,
            3: Nre,
            4: Qdi
        }

        return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group, GLOBAL.particle_group, GLOBAL.main_char.rect.center)

    GLOBAL.stage = clamp(args[0], 0, 4)
    GLOBAL.level = clamp(args[1], 0, 5)
    GLOBAL.flash = clamp(args[2], 1, 96)
    GLOBAL.power = clamp(args[3], 0, 32)
    GLOBAL.second_background = picture[GLOBAL.stage]

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if GLOBAL.is_s_divide:
                    GLOBAL.main_char.free()

                GLOBAL.main_char.image = turn_side(GLOBAL.main_char.original_image.subsurface((0, 0, 12, 26)), GLOBAL.main_char.original_image.subsurface((12, 0, 12, 26)), GLOBAL.is_move_right, GLOBAL.is_move_left)
                GLOBAL.main_char.rect.x = move_plane(GLOBAL.main_char.rect.x, (4, 8), GLOBAL.is_move_left, GLOBAL.is_move_right, GLOBAL.is_fast)
                GLOBAL.main_char.rect.centery = 331 if GLOBAL.is_fast else 332
                keep_x = clamp(GLOBAL.main_char.rect.centerx, window.left, window.right)
                GLOBAL.main_char.rect.centerx = keep_x
                GLOBAL.decision_point.rect.center = (keep_x, GLOBAL.main_char.rect.centery)

                if hasattr(GLOBAL.char, "target_pos"):
                    GLOBAL.char.target_pos = GLOBAL.main_char.rect.center

                COLLIDE.barrage_collide(GLOBAL.main_char.rect.center)
                GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer = invinc(GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer, 180, 6, GLOBAL.main_char.reset_bullet)

                GLOBAL.item_spawn_timer = item_spawn(GLOBAL.item_group, GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0, Item.Item, "fire", -2, (randint(120, 465), 10), timer=GLOBAL.item_spawn_timer)
                if GLOBAL.combo_timer <= 1 and GLOBAL.combo > 0:
                    GLOBAL.text_group.add(Text(GLOBAL.main_char.rect.midtop, (45, 60), 0.5, text_cache[f"{2 ** GLOBAL.combo}_{color_dict[6]}"], text_cache[f"{2 ** GLOBAL.combo}_{color_dict[7]}"]))
                GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score = combo_counter(GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()
                GLOBAL.text_group.update()

                COLLIDE.bullet_collide()
                COLLIDE.item_collide()

            if not GLOBAL.is_level_load:
                GLOBAL.wait_level_load_timer, GLOBAL.is_level_load = load_level(GLOBAL.wait_level_load_timer, GLOBAL.is_level_load, 90, sprite_loader)
            elif len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                GLOBAL.is_summary = True

        KEY.key_event()
        GUI.display(screen, clock)

        clock.tick(60)