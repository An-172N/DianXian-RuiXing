# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import random


import pygame


from PRELOAD import color_dict, barrage_rate, text_cache
from LOGIC.CALCULATE import clamp
from LOGIC.ITEM import item_spawn
from SCRIPT import GLOBAL
from SCRIPT.SPRITE import Barrage, Line, Bullet, Particle, Item, Brick


def spawn_barrage(stage: int, group: pygame.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, locate: tuple) -> None:
    if random() <= fib[stage - 1]:
        barrage_dict = {
            1: Barrage.circle_barrage,
            2: Barrage.polygon_barrage
        }

        if stage in [1, 2]:
            return barrage_dict.get(stage)(type, color, spawn_pos, locate, group)
        elif stage == 3:
            return Line.line_barrage(color, locate, group)
        else:
            return Barrage.point_barrage(type, color, locate, group)


def brick_blast(group: pygame.sprite.Group, stage: int, color: list, *spawn_pos: tuple) -> None:
    if color[0] == color_dict[6]:
        process_dict = {
            1: Bullet.circle_brick,
            3: Line.line_brick
        }

        if stage == 2:
            return Bullet.polygon_brick(group, spawn_pos[0], spawn_pos[1], spawn_pos[2])
        elif stage in [1, 3]:
            return process_dict.get(stage)(group, spawn_pos[3])
        else:
            return Bullet.point_brick(group)


def item_collide() -> None:
    if GLOBAL.is_shoot and GLOBAL.shoot_counter > 0:
        GLOBAL.main_char.fire(GLOBAL.power)
        GLOBAL.shoot_counter -= 1
        Particle.spawn_particles(GLOBAL.particle_group, (2, 2), GLOBAL.main_char.rect.center, (4, 8), GLOBAL.main_char.color)

    collide = pygame.sprite.spritecollide(GLOBAL.main_char, GLOBAL.item_group, False)

    if collide:
        for item in collide:
            GLOBAL.combo_timer = 120
            GLOBAL.shoot_counter = int(clamp(GLOBAL.shoot_counter + 1, 0, 6))

            if item.type == "power":
                GLOBAL.power = int(clamp(GLOBAL.power + 1, 0, 32))
                GLOBAL.combo += 1
            elif item.type == "flash":
                GLOBAL.flash += 1
                GLOBAL.combo += 1

                GLOBAL.text_group.add(Barrage.Text(GLOBAL.main_char.rect.midtop, (45, 60), 0.5, text_cache[f"extend_{color_dict[6]}"], text_cache[f"extend_{color_dict[2]}"]))

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
            if barrage.color != color_dict[6] and not (GLOBAL.is_collide or GLOBAL.is_s_divide):
                GLOBAL.is_collide = True
                Particle.spawn_particles(GLOBAL.particle_group, (9, 9), position, (10, 16), color_dict[5], color_dict[6])

                GLOBAL.no_flash = 0
                GLOBAL.flash -= 1
                GLOBAL.use_flash += 1

                if GLOBAL.flash == 0:
                    GLOBAL.is_save = True

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
                    if not brick.is_die:
                        Particle.spawn_particles(GLOBAL.particle_group, (2, 2), brick.rect.center, (4, 8), brick.color, color_dict[6])
                        if hasattr(brick, "free"):
                            GLOBAL.text_part, GLOBAL.text_number, GLOBAL.is_talk, GLOBAL.animate_timer = Brick.boss_lose(GLOBAL.text_part)
                        else:
                            spawn_barrage(GLOBAL.stage, GLOBAL.barrage_group, barrage_rate, brick.type, [brick.color, color_dict[6], color_dict[3]], brick.rect.center, GLOBAL.main_char.rect.center)
                        if hasattr(brick, "have_power"):
                            item_spawn(GLOBAL.item_group, brick.have_power, Item.Item, "power", 2.5, brick.rect.center)
                        if hasattr(brick, "have_flash"):
                            item_spawn(GLOBAL.item_group, brick.have_flash, Item.Item, "flash", 2.5, brick.rect.center)
                        brick_blast(GLOBAL.bullet_group, GLOBAL.stage, [brick.color, color_dict[5], color_dict[3]], brick.rect.midleft, brick.rect.midright, brick.rect.midbottom, brick.rect.center)
                        brick.kill()

                    brick.death()
                if bullet.type in ("bullet", "bomb"):
                    bullet.kill()