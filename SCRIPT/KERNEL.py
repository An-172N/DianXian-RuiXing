import argparse
import sys
import os

import pygame

import SCRIPT.LOGIC as LOGIC
import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE


class Game:
    def __init__(th, screen, clock):
        pygame.display.set_icon(pygame.image.load(os.path.join(DICT.asset_path, 'IMG_ICON.png')))

        th.screen = screen
        th.clock = clock
        th.font = pygame.font.Font(os.path.join(DICT.asset_path, 'FNT\FNT_GNUUNIFONT.otf'), 15)

        th.plane_mgr = LOGIC.PlaneMgr
        th.stage_mgr = LOGIC.StageMgr
        th.bullet_mgr = LOGIC.BulletMgr
        th.item_mgr = LOGIC.ItemMgr
        th.brick_mgr = LOGIC.BrickMgr
        th.barrage_mgr = LOGIC.BarrageMgr
        th.particle_mgr = LOGIC.ParticleMgr
        th.key_mgr = LOGIC.Key
        th.gui = LOGIC.GUI

        th.option()

    @staticmethod
    def option() -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--stage',
            type=int,
            default=1
        )
        parser.add_argument(
            '--level',
            type=int,
            default=0
        )
        parser.add_argument(
            '--player',
            type=int,
            default=4
        )
        parser.add_argument(
            '--s_power',
            type=int,
            default=0
        )
        args = parser.parse_args()
        VARIABLE.stage = args.stage
        VARIABLE.level = args.level
        VARIABLE.player = args.player
        VARIABLE.s_power = args.s_power

    @staticmethod
    def remove_sprite(sprite_group, effective_range) -> None:
        for sprite in sprite_group:
            if not effective_range.collidepoint(sprite.rect.center):
                sprite.kill()

    def update(th) -> None:
        while True:
            if (
                VARIABLE.run and
                not VARIABLE.save and
                not VARIABLE.pause
            ):
                if (
                    not VARIABLE.summary and
                    not VARIABLE.talk and
                    VARIABLE.level_load
                ):
                    if VARIABLE.is_s_divide:
                        VARIABLE.main_char.bomb.free()

                    th.plane_mgr.turn_side()
                    th.plane_mgr.move_plane()
                    th.plane_mgr.invinc()
                    th.item_mgr.item_spawn_regular()
                    if (
                        VARIABLE.can_shoot
                        and VARIABLE.shoot_counter > 0
                    ):
                        th.bullet_mgr.spawn_bullet()
                        th.particle_mgr.spawn_particles(
                            2,
                            2,
                            VARIABLE.main_char.color,
                            VARIABLE.main_char.rect.center,
                            (6, 12)
                        )
            
                    VARIABLE.bullet_group.update()
                    VARIABLE.barrage_group.update()
                    VARIABLE.item_group.update()
                    VARIABLE.particle_group.update()
                    VARIABLE.brick_group.update()

                    th.remove_sprite(VARIABLE.bullet_group, VARIABLE.effective)
                    th.remove_sprite(VARIABLE.barrage_group, VARIABLE.effective)
                    th.remove_sprite(VARIABLE.item_group, VARIABLE.effective)
                    th.remove_sprite(VARIABLE.particle_group, VARIABLE.window)

                    collide1 = pygame.sprite.spritecollide(
                        VARIABLE.decision_point,
                        VARIABLE.barrage_group,
                        False,
                        pygame.sprite.collide_mask
                    )
                    for barrage in collide1:
                        if (
                            barrage.color != DICT.color_dict[6]
                            and not (
                                VARIABLE.collide or
                                VARIABLE.is_s_divide
                            )
                        ):
                            th.plane_mgr.collide_barrage()
                            th.particle_mgr.spawn_particles(
                                8,
                                9,
                                VARIABLE.main_char.color,
                                VARIABLE.main_char.rect.center,
                                (12, 16)
                            )
                            th.plane_mgr.life_logic()

                            barrage.kill()
                    collide2 = pygame.sprite.groupcollide(
                        VARIABLE.bullet_group,
                        VARIABLE.brick_group,
                        False,
                        False
                    )
                    for bullet, hit_bricks in collide2.items():
                        for brick in hit_bricks:
                            th.bullet_mgr.bullet_collide(bullet, brick)
                            if brick.hp <= 0:
                                if (
                                    bullet.type == "bullet"
                                    and getattr(brick, 'is_die', False)
                                ):
                                    bullet.kill()
                                    break
                                th.brick_mgr.brick_death(brick)
                                th.particle_mgr.spawn_particles(
                                    2,
                                    2,
                                    brick.color,
                                    brick.rect.center,
                                    (6, 12)
                                )
                                if hasattr(brick, "bomb"):
                                    th.stage_mgr.shhm_lose()
                                th.item_mgr.item_spawn(brick)
                                th.brick_mgr.brick_blast(brick)
                                th.barrage_mgr.spawn_barrage(brick)
                                brick.kill()
                            if bullet.type == "bullet":
                                bullet.kill()
                    collide3 = pygame.sprite.spritecollide(
                        VARIABLE.main_char,
                        VARIABLE.item_group,
                        False
                    )
                    for item in collide3:
                        th.item_mgr.item_collide(item)

                th.item_mgr.combo_counter()

                th.stage_mgr.level_process()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if (
                        VARIABLE.run
                        and event.key in DICT.keyup_game_dict
                    ):
                        DICT.keyup_game_dict[event.key]()
                elif event.type == pygame.KEYDOWN:
                    if (
                        not VARIABLE.run
                        and event.key in DICT.keydown_start_dict
                    ):
                        DICT.keydown_start_dict[event.key]()
                    elif VARIABLE.save:
                        if event.key in DICT.keydown_over_dict:
                            DICT.keydown_over_dict[event.key]()
                        else:
                            VARIABLE.name += event.unicode
                    elif (
                        VARIABLE.pause
                        and event.key in DICT.keydown_pause_dict
                    ):
                        DICT.keydown_pause_dict[event.key]()
                    elif (
                        VARIABLE.talk
                        and event.key in DICT.keydown_talk_dict
                    ):
                        DICT.keydown_talk_dict[event.key]()
                    elif (
                        not VARIABLE.summary
                        and VARIABLE.level_load
                        and event.key in DICT.keydown_game_dict
                    ):
                        DICT.keydown_game_dict[event.key]()

            th.screen.fill(DICT.color_dict[7])
            th.screen.blit(VARIABLE.second_background, (120, 15))

            VARIABLE.bullet_group.draw(th.screen)
            if VARIABLE.is_visitable:
                VARIABLE.plane_group.draw(th.screen)
            VARIABLE.brick_group.draw(th.screen)
            VARIABLE.item_group.draw(th.screen)
            VARIABLE.particle_group.draw(th.screen)
            VARIABLE.barrage_group.draw(th.screen)

            if not VARIABLE.run:
                th.gui.start_menu(th.screen, th.font)
            elif VARIABLE.pause:
                th.gui.pause_menu(th.screen, th.font)
            elif not VARIABLE.level_load:
                th.gui.load_menu(th.screen, th.font)
            elif VARIABLE.talk:
                th.gui.talk_menu(th.screen, th.font)
            elif VARIABLE.summary:
                th.gui.summary_menu(th.screen, th.font)
            elif VARIABLE.save:
                th.gui.save_menu(th.screen, th.font)

            th.screen.blit(VARIABLE.background, (0, 0))

            th.gui.show_situ(th.screen, th.font, th.clock)

            pygame.display.flip()

            th.clock.tick(60)