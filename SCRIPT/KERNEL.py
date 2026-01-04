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
import SCRIPT.GLOBAL as GLOBAL

font = pygame.font.Font(os.path.join(GLOBAL.asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)

pygame.display.set_icon(pygame.image.load(os.path.join(GLOBAL.asset_path, 'IMAGE\IMG_ICON.png')))


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
    GLOBAL.stage = args.stage
    GLOBAL.level = args.level
    GLOBAL.player = args.player
    GLOBAL.s_power = args.s_power


def remove_sprite(sprite_group, effective_range) -> None:
    for sprite in sprite_group:
        if not effective_range.collidepoint(sprite.rect.center):
            sprite.kill()


def item_collide() -> None:
    if (
        GLOBAL.can_shoot
        and GLOBAL.shoot_counter > 0
    ):
        LOGIC.BulletMgr.spawn_bullet()
        LOGIC.ParticleMgr.spawn_particles(
            2,
            2,
            GLOBAL.main_char.rect.center,
            (4, 8),
            GLOBAL.main_char.color
        )

    collide3 = pygame.sprite.spritecollide(
         GLOBAL.main_char, GLOBAL.item_group,
        False
    )
    for item in collide3:
        LOGIC.ItemMgr.item_collide(item)


def barrage_collide() -> None:
    collide1 = pygame.sprite.spritecollide(
        GLOBAL.decision_point,
        GLOBAL.barrage_group,
        False,
        pygame.sprite.collide_mask
    )
    for barrage in collide1:
        if (
            barrage.color != GLOBAL.color_dict[6]
            and not (
                GLOBAL.collide or
                GLOBAL.is_s_divide
            )
        ):
            LOGIC.PlaneMgr.collide_barrage()
            LOGIC.ParticleMgr.spawn_particles(
                8,
                9,
                GLOBAL.main_char.rect.center,
                (10, 16),
                GLOBAL.main_char.color,
                GLOBAL.color_dict[6]
            )
            LOGIC.PlaneMgr.life_logic()

            barrage.kill()


def bullet_collide() -> None:
    collide2 = pygame.sprite.groupcollide(
        GLOBAL.bullet_group,
        GLOBAL.brick_group,
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
                    brick.color, GLOBAL.color_dict[6]
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
            GLOBAL.run and
            not GLOBAL.save and
            not GLOBAL.pause
        ):
            if (
                not GLOBAL.summary and
                not GLOBAL.talk and
                GLOBAL.level_load
            ):
                if GLOBAL.is_s_divide:
                    GLOBAL.main_char.free()

                LOGIC.PlaneMgr.turn_side()
                LOGIC.PlaneMgr.move_plane()
                LOGIC.PlaneMgr.invinc()

                LOGIC.ItemMgr.item_spawn_regular()
            
                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()

                remove_sprite(GLOBAL.bullet_group, GLOBAL.effective)
                remove_sprite(GLOBAL.barrage_group, GLOBAL.effective)
                remove_sprite(GLOBAL.item_group, GLOBAL.effective)
                remove_sprite(GLOBAL.particle_group, GLOBAL.window)

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