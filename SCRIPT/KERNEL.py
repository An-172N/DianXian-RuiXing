# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import argparse
import random
import os

import pygame

import LOGIC
from SCRIPT import HUMAN, SPRITE, GLOBAL, GUI, KEY


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


def remove_sprite(sprite_group: pygame.sprite.Group, effective_range: pygame.Rect) -> None:
    for sprite in sprite_group:
        if not effective_range.collidepoint(sprite.rect.center):
            sprite.kill()


def item_collide() -> None:
    if GLOBAL.is_shoot and GLOBAL.shoot_counter > 0:
        GLOBAL.main_char.fire(GLOBAL.power)
        GLOBAL.shoot_counter -= 1
        SPRITE.Particle.spawn_particles(
            GLOBAL.particle_group,
            (2, 2),
            GLOBAL.main_char.rect.center,
            (4, 8),
            45,
            GLOBAL.main_char.color
        )

    collide3 = pygame.sprite.spritecollide(GLOBAL.main_char, GLOBAL.item_group, False)

    for item in collide3:
        if item.type == "power":
            GLOBAL.combo_timer, GLOBAL.shoot_counter, GLOBAL.combo, GLOBAL.power = LOGIC.Item.item_collide(
                GLOBAL.combo_timer,
                int(LOGIC.FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6)),
                GLOBAL.power,
                GLOBAL.combo,
                120
            )
            GLOBAL.power = int(LOGIC.FUNC.clamp(GLOBAL.power, 0, 32))
        elif item.type == "flash":
            GLOBAL.combo_timer, GLOBAL.shoot_counter, GLOBAL.combo, GLOBAL.flash = LOGIC.Item.item_collide(
                GLOBAL.combo_timer,
                int(LOGIC.FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6)),
                GLOBAL.flash,
                GLOBAL.combo,
                120
            )
        else:
            GLOBAL.combo_timer, GLOBAL.shoot_counter, _, __ = LOGIC.Item.item_collide(
                GLOBAL.combo_timer,
                int(LOGIC.FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6)),
                0,
                0,
                120
            )

        if item.type in ['flash', 'power']:
            GLOBAL.total_power, GLOBAL.stage_total_power = LOGIC.Plane.collide_item(
                GLOBAL.total_power,
                GLOBAL.stage_total_power
            )
        item.kill()


def barrage_collide(position) -> None:
    collide1 = pygame.sprite.spritecollide(GLOBAL.decision_point, GLOBAL.barrage_group, False, pygame.sprite.collide_mask)

    for barrage in collide1:
        if barrage.color != (255, 255, 255) and not (GLOBAL.is_collide or GLOBAL.is_s_divide):
            GLOBAL.is_collide = True
            SPRITE.Particle.spawn_particles(
                GLOBAL.particle_group,
                (9, 9),
                position,
                (10, 16),
                45,
                GLOBAL.color_dict[5],
                (255, 255, 255)
            )
            GLOBAL.no_flash, GLOBAL.flash, GLOBAL.use_flash = LOGIC.Plane.flash_logic(
                GLOBAL.no_flash,
                GLOBAL.flash,
                GLOBAL.use_flash,
            )
            if GLOBAL.flash == 0:
                GLOBAL.is_save = True
                GLOBAL.is_blit = False

            barrage.kill()


def bullet_collide() -> None:
    collide2 = pygame.sprite.groupcollide(GLOBAL.bullet_group, GLOBAL.brick_group, False, False)

    for bullet, hit_bricks in collide2.items():
        for brick in hit_bricks:
            brick.hp, GLOBAL.score = LOGIC.Bullet.bullet_collide(brick.hp, bullet.damage, GLOBAL.score, 64)
            if brick.hp <= 0:
                if bullet.type in ("bullet", "line", "bomb") and brick.is_die:
                    bullet.kill()
                    break

                brick.is_die = True
                SPRITE.Particle.spawn_particles(
                    GLOBAL.particle_group,
                    (2, 2),
                    brick.rect.center,
                    (4, 8),
                    45,
                    brick.color,
                    (255, 255, 255)
                )
                if hasattr(brick, "free"):
                    GLOBAL.text_part, GLOBAL.text_number, GLOBAL.is_talk, GLOBAL.is_blit = boss_lose(
                        GLOBAL.text_part,
                        GLOBAL.text_number,
                        GLOBAL.is_talk,
                        GLOBAL.is_blit
                    )
                else:
                    spawn_barrage(
                        GLOBAL.stage,
                        GLOBAL.barrage_group,
                        GLOBAL.fibonacci_list,
                        brick.type,
                        [brick.color, (255, 255, 255), GLOBAL.color_dict[3]],
                        brick.rect.center,
                        GLOBAL.main_char.rect.center
                    )
                SPRITE.Item.item_spawn(
                    GLOBAL.item_group,
                    brick.have_power,
                    brick.rect.center,
                    2.5,
                    GLOBAL.color_dict[5],
                    "power"
                )
                SPRITE.Item.item_spawn(
                    GLOBAL.item_group,
                    brick.have_flash,
                    brick.rect.center,
                    2.5,
                    GLOBAL.color_dict[2],
                    "flash"
                )
                brick_blast(
                    GLOBAL.bullet_group,
                    GLOBAL.stage,
                    [brick.color, GLOBAL.color_dict[5], GLOBAL.color_dict[3]],
                    brick.rect.midleft,
                    brick.rect.midright,
                    brick.rect.midbottom,
                    brick.rect.center
                )
                brick.kill()
            if bullet.type in ("bullet", "bomb"):
                bullet.kill()


def choose_brick(group: pygame.sprite.Group, stage_level: tuple, basic_power: int, basic_flash: int) -> None:
    brick_list = list(group)
    choose_power = random.sample(range(len(brick_list)), basic_power + stage_level[0] + stage_level[1])
    choose_flash = random.sample(range(len(brick_list)), basic_flash)
    
    for i in choose_power:
        brick_list[i].have_power = True
    for j in choose_flash:
        brick_list[j].have_flash = True


def boss_lose(part: int, number: int, is_talk: bool, is_blit: bool) -> tuple:
    part += 1
    number = 0

    is_talk = True
    is_blit = False

    return part, number, is_talk, is_blit


def spawn_barrage(stage: int, group: pygame.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, target_pos: tuple) -> None:
    if random.random() <= 0.17 + fib[stage - 1]:
        barrage_dict = {
            1: SPRITE.Barrage.circle_barrage,
            2: SPRITE.Barrage.polygon_barrage,
            3: SPRITE.Line.line_barrage,
            4: SPRITE.Barrage.point_barrage
        }

        if stage in [1, 2]:
            return barrage_dict.get(stage)(type, color, spawn_pos, target_pos, group)
        elif stage == 3:
            return barrage_dict.get(stage)(color, target_pos, group)
        else:
            return barrage_dict.get(stage)(type, color, target_pos, group)
        

def brick_blast(group: pygame.sprite.Group, stage: int, color: list, *spawn_pos: tuple) -> None:
    if color[0] == (255, 255, 255):
        process_dict = {
            1: SPRITE.Bullet.circle_brick,
            2: SPRITE.Bullet.polygon_brick,
            3: SPRITE.Line.line_brick,
            4: SPRITE.Bullet.point_brick
        }

        if stage in [1, 2]:
            return process_dict.get(stage)(group, *spawn_pos)
        elif stage == 3:
            return process_dict.get(stage)(group, color[1], color[2], *spawn_pos)
        else:
            return process_dict.get(stage)(group)


def sprite_loader() -> None:
    if GLOBAL.level == 6:
        GLOBAL.char = chs_shhm()
        GLOBAL.text = LOGIC.File.load_text(os.path.join(GLOBAL.asset_path, f"JSON\TALK_{GLOBAL.stage}.json"))
        GLOBAL.is_talk = True
        GLOBAL.is_blit = False

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        level_file = os.path.join(GLOBAL.asset_path, f"STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg")

        with open(level_file, 'r', encoding="ascii") as f:
            string = f.read().splitlines()

            for row, line in enumerate(string):
                SPRITE.Brick.load_brick(row, line, GLOBAL.color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)

            choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)


def chs_shhm() -> HUMAN.Ono | HUMAN.Hro | HUMAN.Nre | HUMAN.Qdi:
    char_dict = {
        1: HUMAN.Ono,
        2: HUMAN.Hro,
        3: HUMAN.Nre,
        4: HUMAN.Qdi,
    }

    if GLOBAL.stage in [2, 3, 4]:
        return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group, GLOBAL.main_char.rect.center)
    else:
        return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group)


def update(clock: pygame.time.Clock, screen: pygame.Surface, _: None) -> None:
    option()

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                main_char = GLOBAL.main_char
                decision_point = GLOBAL.decision_point

                if GLOBAL.is_s_divide:
                    main_char.free()

                GLOBAL.main_char.image = LOGIC.Plane.turn_side(
                    main_char.original_image.subsurface((0, 0, 12, 26)),
                    main_char.original_image.subsurface((12, 0, 12, 26)),
                    GLOBAL.is_move_right,
                    GLOBAL.is_move_left
                )
                main_char.rect.x, main_char.rect.centery = LOGIC.Plane.move_plane(
                    (main_char.rect.x, main_char.rect.centery),
                    (4, 8),
                    (331, 332),
                    GLOBAL.is_move_right,
                    GLOBAL.is_move_left,
                    GLOBAL.is_fast
                )
                keep_position = LOGIC.Plane.keep_position(
                    GLOBAL.window.left,
                    GLOBAL.window.right,
                    main_char.rect.center
                )
                main_char.rect.center = keep_position
                decision_point.rect.center = keep_position

                if hasattr(GLOBAL.char, "target_pos"):
                    GLOBAL.char.target_pos = GLOBAL.main_char.rect.center
                GLOBAL.is_s_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_timer = LOGIC.Plane.invinc(
                    GLOBAL.is_s_divide,
                    GLOBAL.is_collide,
                    GLOBAL.is_visitable,
                    GLOBAL.cooldown_timer,
                    180,
                    6,
                    main_char.reset_bullet
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

                remove_sprite(GLOBAL.bullet_group, GLOBAL.effective)
                remove_sprite(GLOBAL.barrage_group, GLOBAL.effective)
                remove_sprite(GLOBAL.item_group, GLOBAL.effective)
                remove_sprite(GLOBAL.particle_group, GLOBAL.window)

                barrage_collide(GLOBAL.main_char.rect.center)
                bullet_collide()
                item_collide()

            if not GLOBAL.is_level_load:
                GLOBAL.wait_level_load_timer, GLOBAL.is_level_load =LOGIC.Stage.level_load(
                    GLOBAL.wait_level_load_timer,
                    GLOBAL.is_level_load,
                    60,
                    sprite_loader
                )
            else:
                GLOBAL.is_summary = LOGIC.Stage.level_summary(
                    len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk,
                    GLOBAL.is_summary,
                )
                GLOBAL.is_blit = False

        KEY.key_event()

        GUI.window_display(screen)
        GUI.menu_display(screen)
        GUI.font_display(screen, clock)

        pygame.display.flip()
        clock.tick(60)