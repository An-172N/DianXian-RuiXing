# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random

import pygame

import LOGIC
from SCRIPT import GLOBAL, SPRITE


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

        if stage == 2:
            return process_dict.get(stage)(group, spawn_pos[0], spawn_pos[1], spawn_pos[2])
        elif stage in [1, 3]:
            return process_dict.get(stage)(group, spawn_pos[3])
        else:
            return process_dict.get(stage)(group)


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
            GLOBAL.main_char.color
        )

    collide = pygame.sprite.spritecollide(GLOBAL.main_char, GLOBAL.item_group, False)

    if collide:
        for item in collide:
            GLOBAL.combo_timer = 120
            GLOBAL.shoot_counter = int(LOGIC.FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6))

            if item.type == "power":
                GLOBAL.power = int(LOGIC.FUNC.clamp(GLOBAL.power + 1, 0, 32))
                GLOBAL.combo += 1
            elif item.type == "flash":
                GLOBAL.flash += 1
                GLOBAL.combo += 1

            if item.type in ['flash', 'power']:
                GLOBAL.total_power += 1
                GLOBAL.stage_total_power += 1

            item.kill()


def barrage_collide(position) -> None:
    if GLOBAL.is_collide or GLOBAL.is_s_divide:
        return

    collide = pygame.sprite.spritecollide(GLOBAL.decision_point, GLOBAL.barrage_group, False, pygame.sprite.collide_mask)

    if collide:
        for barrage in collide:
            if barrage.color != (255, 255, 255) and not (GLOBAL.is_collide or GLOBAL.is_s_divide):
                GLOBAL.is_collide = True
                SPRITE.Particle.spawn_particles(
                    GLOBAL.particle_group,
                    (9, 9),
                    position,
                    (10, 16),
                    GLOBAL.color_dict[5],
                    (255, 255, 255)
                )

                GLOBAL.no_flash = 0
                GLOBAL.flash -= 1
                GLOBAL.use_flash += 1

                if GLOBAL.flash == 0:
                    GLOBAL.is_save = True
                    GLOBAL.is_blit = False

                barrage.kill()


def bullet_collide() -> None:
    collide = pygame.sprite.groupcollide(GLOBAL.bullet_group, GLOBAL.brick_group, False, False)

    if collide:
        for bullet, hit_bricks in collide.items():
            for brick in hit_bricks:
                if brick.hp > 0:
                    GLOBAL.score += 64
                brick.hp -= bullet.damage

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
                        brick.color,
                        (255, 255, 255)
                    )
                    if hasattr(brick, "free"):
                        GLOBAL.text_part, GLOBAL.text_number, GLOBAL.is_talk, GLOBAL.is_blit = SPRITE.Brick.boss_lose(
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