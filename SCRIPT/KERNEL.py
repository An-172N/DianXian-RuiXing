import argparse
import os

import pygame


clock = pygame.time.Clock()
screen = pygame.display.set_mode(
    (480, 360),
    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED,
    vsync=1
)

import SCRIPT.LOGIC as LOGIC
import SCRIPT.TABLE as TABLE
import SCRIPT.VARIABLE as VARIABLE

font = pygame.font.Font(os.path.join(TABLE.asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)

pygame.display.set_icon(pygame.image.load(os.path.join(TABLE.asset_path, 'IMAGE\IMG_ICON.png')))


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


def item_collide() -> None:
    if (
        VARIABLE.can_shoot
        and VARIABLE.shoot_counter > 0
    ):
        LOGIC.BulletMgr.spawn_bullet()
        LOGIC.ParticleMgr.spawn_particles(
            2,
            2,
            VARIABLE.main_char.rect.center,
            (4, 8),
            VARIABLE.main_char.color
        )

    collide3 = pygame.sprite.spritecollide(
         VARIABLE.main_char, TABLE.item_group,
        False
    )
    for item in collide3:
        LOGIC.ItemMgr.item_collide(item)


def barrage_collide() -> None:
    collide1 = pygame.sprite.spritecollide(
        VARIABLE.decision_point,
        TABLE.barrage_group,
        False,
        pygame.sprite.collide_mask
    )
    for barrage in collide1:
        if (
            barrage.color != TABLE.color_dict[6]
            and not (
                VARIABLE.collide or
                VARIABLE.is_s_divide
            )
        ):
            LOGIC.PlaneMgr.collide_barrage()
            LOGIC.ParticleMgr.spawn_particles(
                8,
                9,
                VARIABLE.main_char.rect.center,
                (10, 16),
                VARIABLE.main_char.color,
                TABLE.color_dict[6]
            )
            LOGIC.PlaneMgr.life_logic()

            barrage.kill()


def bullet_collide() -> None:
    collide2 = pygame.sprite.groupcollide(
        TABLE.bullet_group,
        TABLE.brick_group,
        False,
        False
    )
    for bullet, hit_bricks in collide2.items():
        for brick in hit_bricks:
            LOGIC.BulletMgr.bullet_collide(bullet, brick)
            if brick.hp <= 0:
                if (
                    bullet.type in ("bullet", "line", "bomb")
                    and getattr(brick, 'is_die', False)
                ):
                    bullet.kill()
                    break
                LOGIC.BrickMgr.brick_death(brick)
                LOGIC.ParticleMgr.spawn_particles(
                    2, 2,
                    brick.rect.center,
                    (4, 8),
                    brick.color, TABLE.color_dict[6]
                )
                if hasattr(brick, "free"):
                    LOGIC.StageMgr.shhm_lose()
                LOGIC.ItemMgr.item_spawn(brick)
                LOGIC.BrickMgr.brick_blast(brick)
                LOGIC.BarrageMgr.spawn_barrage(brick)
                brick.kill()
            if bullet.type in ("bullet", "bomb"):
                bullet.kill()


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

                LOGIC.PlaneMgr.turn_side()
                LOGIC.PlaneMgr.move_plane()
                LOGIC.PlaneMgr.invinc()

                LOGIC.ItemMgr.item_spawn_regular()
            
                TABLE.bullet_group.update()
                TABLE.barrage_group.update()
                TABLE.item_group.update()
                TABLE.particle_group.update()
                TABLE.brick_group.update()

                remove_sprite(TABLE.bullet_group, VARIABLE.effective)
                remove_sprite(TABLE.barrage_group, VARIABLE.effective)
                remove_sprite(TABLE.item_group, VARIABLE.effective)
                remove_sprite(TABLE.particle_group, VARIABLE.window)

                barrage_collide()
                bullet_collide()
                item_collide()

            LOGIC.ItemMgr.combo_counter()
            LOGIC.StageMgr.level_process()

        LOGIC.Key.key_event()

        LOGIC.GUI.window_display(screen)
        LOGIC.GUI.menu_display(screen, font)
        LOGIC.GUI.font_display(screen, font, clock)

        pygame.display.flip()
        clock.tick(60)


option()
update()