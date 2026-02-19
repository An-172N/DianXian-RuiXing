# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random


import pygame


import PRELOAD
from LOGIC import Plane, Stage, Item


def update(clock: pygame.time.Clock, screen: pygame.Surface, *args: tuple) -> None:
    from SCRIPT import GUI, KEY, COLLIDE, SPRITE, PUBLIC, GLOBAL

    GLOBAL.stage, GLOBAL.level, GLOBAL.flash, GLOBAL.power = args
    GLOBAL.second_background = PRELOAD.picture[GLOBAL.stage]

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if GLOBAL.is_s_divide:
                    GLOBAL.main_char.free()

                GLOBAL.main_char.image = Plane.turn_side(GLOBAL.main_char.original_image.subsurface((0, 0, 12, 26)), GLOBAL.main_char.original_image.subsurface((12, 0, 12, 26)), GLOBAL.is_move_right, GLOBAL.is_move_left)
                GLOBAL.main_char.rect.x, GLOBAL.main_char.rect.centery = Plane.move_plane((GLOBAL.main_char.rect.x, GLOBAL.main_char.rect.centery), (4, 8), (331, 332), GLOBAL.is_move_left, GLOBAL.is_move_right, GLOBAL.is_fast)
                keep_position = Plane.keep_position(PRELOAD.window.left, PRELOAD.window.right, GLOBAL.main_char.rect.center)
                GLOBAL.main_char.rect.center = keep_position
                GLOBAL.decision_point.rect.center = keep_position

                if hasattr(GLOBAL.char, "target_pos"):
                    GLOBAL.char.target_pos = GLOBAL.main_char.rect.center

                COLLIDE.barrage_collide(GLOBAL.main_char.rect.center)
                GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer = Plane.invinc(GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer, 180, 6, GLOBAL.main_char.reset_bullet)

                GLOBAL.item_spawn_timer = SPRITE.Item.item_spawn(GLOBAL.item_group, GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0, (random.randint(120, 465), 10), -2, "fire", GLOBAL.item_spawn_timer)
                if GLOBAL.combo_timer <= 1 and GLOBAL.combo > 0:
                    sprite = SPRITE.Text.Text(2 ** GLOBAL.combo, GLOBAL.main_char.rect.midtop, (128, 128, 128))
                    GLOBAL.text_group.add(sprite)
                GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score = Item.combo_counter(GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()
                GLOBAL.text_group.update()

                COLLIDE.bullet_collide()
                COLLIDE.item_collide()

            if not GLOBAL.is_level_load:
                GLOBAL.wait_level_load_timer, GLOBAL.is_level_load = Stage.load_level(GLOBAL.wait_level_load_timer, GLOBAL.is_level_load, 90, PUBLIC.sprite_loader)
            elif len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                GLOBAL.is_summary = True

        KEY.key_event()

        GUI.display(screen, clock)

        pygame.display.flip()
        clock.tick(60)