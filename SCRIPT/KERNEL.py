import argparse
import sys
import os

import pygame as pyg

import SCRIPT.LOGIC
import SCRIPT.DICT
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.RESET


class Game:
    def __init__(th, screen):
        pyg.display.set_icon(pyg.image.load(os.path.join(SCRIPT.DICT.asset_path, 'IMG_ICON.png')))

        th.screen = screen
        th.clock = pyg.time.Clock()
        th.font = pyg.font.Font(os.path.join(SCRIPT.DICT.asset_path, 'FNT\FNT_GNUUNIFONT.otf'), 15)

        th.plane_mgr = SCRIPT.LOGIC.PlaneMgr
        th.stage_mgr = SCRIPT.LOGIC.StageMgr
        th.bullet_mgr = SCRIPT.LOGIC.BulletMgr
        th.item_mgr = SCRIPT.LOGIC.ItemMgr
        th.key_mgr = SCRIPT.LOGIC.Key
        th.gui = SCRIPT.LOGIC.GUI

        th.option()

    def option(th) -> None:
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
        [
            sprite.kill()
            for sprite in sprite_group
            if not effective_range.collidepoint(sprite.rect.center)
        ]

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
                    th.bullet_mgr.spawn_bullet()
            
                    VARIABLE.bullet_group.update()
                    VARIABLE.barrage_group.update()
                    VARIABLE.item_group.update()
                    VARIABLE.particle_group.update()
                    VARIABLE.brick_group.update()

                    th.remove_sprite(VARIABLE.bullet_group, VARIABLE.effective)
                    th.remove_sprite(VARIABLE.barrage_group, VARIABLE.effective)
                    th.remove_sprite(VARIABLE.item_group, VARIABLE.effective)
                    th.remove_sprite(VARIABLE.particle_group, VARIABLE.window)

                    collide1 = pyg.sprite.spritecollide(
                        VARIABLE.d_pt,
                        VARIABLE.barrage_group,
                        False,
                        pyg.sprite.collide_mask
                    )
                    for barrage in collide1:
                        if barrage.color != (255, 255, 255):
                            th.plane_mgr.collide_barrage(barrage)
                    collide2 = pyg.sprite.groupcollide(
                        VARIABLE.bullet_group,
                        VARIABLE.brick_group,
                        False,
                        False
                    )
                    for bullet, hit_bricks in collide2.items():
                        for brick in hit_bricks:
                            th.bullet_mgr.bullet_collide(bullet, brick)
                    collide3 = pyg.sprite.spritecollide(
                        VARIABLE.main_char,
                        VARIABLE.item_group,
                        False
                    )
                    for item in collide3:
                        th.item_mgr.item_collide(item)

                th.item_mgr.combo_counter()

                th.stage_mgr.level_process()

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    sys.exit()
                elif event.type == pyg.KEYUP:
                    if (
                        VARIABLE.run
                        and event.key in SCRIPT.DICT.key_dict["up"]["game"]
                    ):
                        SCRIPT.DICT.key_dict["up"]["game"][event.key]()
                elif event.type == pyg.KEYDOWN:
                    if (
                        not VARIABLE.run
                        and event.key in SCRIPT.DICT.key_dict["down"]["start"]
                    ):
                        SCRIPT.DICT.key_dict["down"]["start"][event.key]()
                    elif VARIABLE.save:
                        if event.key in SCRIPT.DICT.key_dict["down"]["over"]:
                            SCRIPT.DICT.key_dict["down"]["over"][event.key]()
                        else:
                            VARIABLE.name += event.unicode
                    elif (
                        VARIABLE.pause
                        and event.key in SCRIPT.DICT.key_dict["down"]["pause"]
                    ):
                        SCRIPT.DICT.key_dict["down"]["pause"][event.key]()
                    elif (
                        VARIABLE.talk
                        and event.key in SCRIPT.DICT.key_dict["down"]["talk"]
                    ):
                        SCRIPT.DICT.key_dict["down"]["talk"][event.key]()
                    elif (
                        not VARIABLE.summary
                        and VARIABLE.level_load
                        and event.key in SCRIPT.DICT.key_dict["down"]["game"]
                    ):
                        SCRIPT.DICT.key_dict["down"]["game"][event.key]()

            if VARIABLE.is_reset:
                SCRIPT.RESET.reset1()
                SCRIPT.RESET.reset2()
                VARIABLE.is_reset = False

            th.screen.fill(SCRIPT.DICT.color_dict[7])
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

            pyg.display.flip()

            th.clock.tick(60)