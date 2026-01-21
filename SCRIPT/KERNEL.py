# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import argparse
import random

import pygame

from SCRIPT import GLOBAL, FUNC, LOGIC


def option() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument('--stage', type=int, default=1)
    parser.add_argument('--level', type=int, default=0)
    parser.add_argument('--flash', type=int, default=3)
    parser.add_argument('--power', type=int, default=0)

    args = parser.parse_args()

    GLOBAL.stage = int(FUNC.clamp(args.stage, 1, 4))
    GLOBAL.level = int(FUNC.clamp(args.level, 0, 5))
    GLOBAL.flash = int(FUNC.clamp(args.flash, 0, 96))
    GLOBAL.power = int(FUNC.clamp(args.power, 0, 32))
    GLOBAL.second_background = GLOBAL.picture[GLOBAL.stage]
    GLOBAL.second_background.set_alpha(128)


def remove_sprite(sprite_group: pygame.sprite.Group, effective_range: pygame.Rect) -> None:
    for sprite in sprite_group:
        if not effective_range.collidepoint(sprite.rect.center):
            sprite.kill()


def item_collide() -> None:
    if GLOBAL.is_shoot and GLOBAL.shoot_counter > 0:
        LOGIC.BulletMgr.spawn_bullet()
        LOGIC.ParticleMgr.spawn_particles(2, 2, GLOBAL.main_char.rect.center, (4, 8), GLOBAL.main_char.color)

    collide3 = pygame.sprite.spritecollide(GLOBAL.main_char, GLOBAL.item_group, False)

    for item in collide3:
        LOGIC.ItemMgr.item_collide(item)


def barrage_collide(position) -> None:
    collide1 = pygame.sprite.spritecollide(GLOBAL.decision_point, GLOBAL.barrage_group, False, pygame.sprite.collide_mask)

    for barrage in collide1:
        if barrage.color != (255, 255, 255) and not (GLOBAL.is_collide or GLOBAL.is_s_divide):
            LOGIC.PlaneMgr.collide_barrage()
            LOGIC.ParticleMgr.spawn_particles(9, 9, position, (10, 16), GLOBAL.color_dict[5], (255, 255, 255))
            LOGIC.PlaneMgr.life_logic()

            barrage.kill()


def bullet_collide() -> None:
    collide2 = pygame.sprite.groupcollide(GLOBAL.bullet_group, GLOBAL.brick_group, False, False)

    for bullet, hit_bricks in collide2.items():
        for brick in hit_bricks:
            LOGIC.BulletMgr.bullet_collide(bullet, brick)
            if brick.hp <= 0:
                if bullet.type in ("bullet", "line", "bomb") and getattr(brick, 'is_die', False):
                    bullet.kill()
                    break

                LOGIC.BrickMgr.brick_death(brick)
                LOGIC.ParticleMgr.spawn_particles(2, 2, brick.rect.center, (4, 8), brick.color, (255, 255, 255))
                LOGIC.StageMgr.shhm_lose() if hasattr(brick, "free") else LOGIC.BarrageMgr.spawn_barrage(brick)
                LOGIC.ItemMgr.item_spawn(brick.have_power, brick.rect.center, 2.5, GLOBAL.color_dict[5], "power")
                LOGIC.ItemMgr.item_spawn(brick.have_flash, brick.rect.center, 2.5, GLOBAL.color_dict[2], "flash")
                LOGIC.BrickMgr.brick_blast(brick)
                brick.kill()
            if bullet.type in ("bullet", "bomb"):
                bullet.kill()


def update(clock: pygame.time.Clock, screen: pygame.Surface, _: None) -> None:
    option()

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if GLOBAL.is_s_divide:
                    GLOBAL.main_char.free()

                LOGIC.PlaneMgr.turn_side()
                LOGIC.PlaneMgr.move_plane()
                LOGIC.PlaneMgr.keep_position()
                LOGIC.PlaneMgr.invinc()

                GLOBAL.item_spawn_timer = LOGIC.ItemMgr.item_spawn(
                    GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0,
                    (random.randint(120, 465), 10),
                    -2,
                    (255, 255, 255),
                    "fire",
                    GLOBAL.item_spawn_timer
                )
                LOGIC.ItemMgr.combo_counter()
            
                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()

                remove_sprite(GLOBAL.bullet_group, GLOBAL.effective)
                remove_sprite(GLOBAL.barrage_group, GLOBAL.effective)
                remove_sprite(GLOBAL.item_group, GLOBAL.effective)
                remove_sprite(GLOBAL.particle_group, GLOBAL.window)

                barrage_collide(GLOBAL.main_char.rect.center)
                bullet_collide()
                item_collide()

            LOGIC.StageMgr.level_process()

        LOGIC.Key.key_event()

        LOGIC.GUI.window_display(screen)
        LOGIC.GUI.menu_display(screen)
        LOGIC.GUI.font_display(screen, clock)

        pygame.display.flip()
        clock.tick(60)