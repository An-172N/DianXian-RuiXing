import argparse
import sys
import os

import pygame


clock = pygame.time.Clock()
screen = pygame.display.set_mode(
    (480, 360),
    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED,
    vsync=1
)

import SCRIPT.LOGIC as LOGIC
import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE

font = pygame.font.Font(os.path.join(DICT.asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)

pygame.display.set_icon(pygame.image.load(os.path.join(DICT.asset_path, 'IMAGE\IMG_ICON.png')))

plane_mgr = LOGIC.PlaneMgr
stage_mgr = LOGIC.StageMgr
bullet_mgr = LOGIC.BulletMgr
item_mgr = LOGIC.ItemMgr
brick_mgr = LOGIC.BrickMgr
barrage_mgr = LOGIC.BarrageMgr
particle_mgr = LOGIC.ParticleMgr
key_mgr = LOGIC.Key
gui = LOGIC.GUI


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


def remove_sprite(sprite_group, effective_range) -> None:
    for sprite in sprite_group:
        if not effective_range.collidepoint(sprite.rect.center):
            sprite.kill()


def update() -> None:
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
                    VARIABLE.main_char.free()

                plane_mgr.turn_side()
                plane_mgr.move_plane()
                plane_mgr.invinc()
                item_mgr.item_spawn_regular()
                if (
                    VARIABLE.can_shoot
                    and VARIABLE.shoot_counter > 0
                ):
                    bullet_mgr.spawn_bullet()
                    particle_mgr.spawn_particles(
                        2,
                        2,
                        VARIABLE.main_char.rect.center,
                        (4, 8),
                        VARIABLE.main_char.color
                    )
            
                VARIABLE.bullet_group.update()
                VARIABLE.barrage_group.update()
                VARIABLE.item_group.update()
                VARIABLE.particle_group.update()
                VARIABLE.brick_group.update()

                remove_sprite(VARIABLE.bullet_group, VARIABLE.effective)
                remove_sprite(VARIABLE.barrage_group, VARIABLE.effective)
                remove_sprite(VARIABLE.item_group, VARIABLE.effective)
                remove_sprite(VARIABLE.particle_group, VARIABLE.window)

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
                        plane_mgr.collide_barrage()
                        particle_mgr.spawn_particles(
                            8,
                            9,
                            VARIABLE.main_char.rect.center,
                            (10, 16),
                            VARIABLE.main_char.color,
                            DICT.color_dict[6]
                        )
                        plane_mgr.life_logic()

                        barrage.kill()
                collide2 = pygame.sprite.groupcollide(
                    VARIABLE.bullet_group,
                    VARIABLE.brick_group,
                    False,
                    False
                )
                for bullet, hit_bricks in collide2.items():
                    for brick in hit_bricks:
                        bullet_mgr.bullet_collide(bullet, brick)
                        if brick.hp <= 0:
                            if (
                                bullet.type in ("bullet", "line", "bomb")
                                and getattr(brick, 'is_die', False)
                            ):
                                bullet.kill()
                                break
                            brick_mgr.brick_death(brick)
                            particle_mgr.spawn_particles(
                                2,
                                2,
                                brick.rect.center,
                                (4, 8),
                                brick.color,
                                DICT.color_dict[6]
                            )
                            if hasattr(brick, "free"):
                                stage_mgr.shhm_lose()
                            item_mgr.item_spawn(brick)
                            brick_mgr.brick_blast(brick)
                            barrage_mgr.spawn_barrage(brick)
                            brick.kill()
                        if bullet.type == "bullet":
                            bullet.kill()
                collide3 = pygame.sprite.spritecollide(
                    VARIABLE.main_char,
                    VARIABLE.item_group,
                    False
                )
                for item in collide3:
                    item_mgr.item_collide(item)

            item_mgr.combo_counter()

            stage_mgr.level_process()

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
                        VARIABLE.is_blited = False
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

        screen.fill(DICT.color_dict[7])
        screen.blit(VARIABLE.second_background, (120, 15))

        VARIABLE.bullet_group.draw(screen)
        if VARIABLE.is_visitable:
            VARIABLE.plane_group.draw(screen)
        VARIABLE.brick_group.draw(screen)
        VARIABLE.item_group.draw(screen)
        VARIABLE.particle_group.draw(screen)
        VARIABLE.barrage_group.draw(screen)

        if not VARIABLE.run:
            gui.start_menu(screen, font)
        elif VARIABLE.pause:
            gui.pause_menu(screen, font)
        elif not VARIABLE.level_load:
            gui.load_menu(screen, font)
        elif VARIABLE.talk:
            gui.talk_menu(screen, font)
        elif VARIABLE.summary:
            gui.summary_menu(screen, font)
        elif VARIABLE.save:
            gui.save_menu(screen, font)

        screen.blit(VARIABLE.background, (0, 0))

        gui.show_situ(screen, font, clock)

        pygame.display.flip()

        clock.tick(60)


option()
update()