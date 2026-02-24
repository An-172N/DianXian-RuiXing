# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import json
from random import randint, random


import pygame as pg


from PRELOAD import picture, window, asset, color_dict, text_cache, char_image, difficulty
from LOGIC.CALCULATE import clamp
from LOGIC.PLANE import turn_side, move_plane, invinc
from LOGIC.ITEM import item_spawn, combo_counter
from LOGIC.STAGE import load_level
from LOGIC.FILE import read_level


def update(clock: pg.time.Clock, screen: pg.Surface, args: tuple) -> None:
    from SCRIPT import GUI, KEY, GLOBAL
    from SCRIPT.SPRITE import Item, Brick
    from SCRIPT.HUMAN import Ono, Hro, Nre, Qdi
    from SCRIPT.SPRITE import Barrage, Line, Bullet, Item, Brick

    def spawn_barrage(stage: int, group: pg.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, locate: tuple) -> None:
        barrage_dict = {
            1: Barrage.circle_barrage,
            2: Barrage.polygon_barrage
        }

        if random() <= fib[stage - 1]:
            if stage in [1, 2]:
                return barrage_dict.get(stage)(type, color, spawn_pos, locate, group)
            elif stage == 3:
                return Line.line_barrage(color, locate, group)
            else:
                return Barrage.point_barrage(type, color, locate, group)

    def brick_blast(group: pg.sprite.Group, stage: int, color: list, *spawn_pos: tuple) -> None:
        process_dict = {
            1: Bullet.circle_brick,
            3: Line.line_brick
        }

        if color[0] == color_dict[6]:
            if stage == 2:
                return Bullet.polygon_brick(group, spawn_pos[0], spawn_pos[1], spawn_pos[2])
            elif stage in [1, 3]:
                return process_dict.get(stage)(group, spawn_pos[3])
            else:
                return Bullet.point_brick(group)

    def item_collide() -> None:
        if GLOBAL.is_shoot and GLOBAL.shoot_count > 0:
            GLOBAL.major.fire(GLOBAL.power)
            Barrage.spawn_particles(GLOBAL.particle_group, (2, 2), GLOBAL.major.rect.center, (4, 8), GLOBAL.major.color)

            GLOBAL.shoot_count -= 1

        collide = pg.sprite.spritecollide(GLOBAL.major, GLOBAL.item_group, False)

        if collide:
            for item in collide:
                GLOBAL.combo_time = 120
                GLOBAL.shoot_count = int(clamp(GLOBAL.shoot_count + 1, 0, 6))

                if item.type == "power":
                    GLOBAL.power = int(clamp(GLOBAL.power + 1, 0, 32))
                    GLOBAL.combo += 1
                elif item.type == "flash":
                    GLOBAL.flash += 1
                    GLOBAL.combo += 1

                    Barrage.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, text_cache[("extend", color_dict[6])], text_cache[("extend", color_dict[2])], GLOBAL.text_group)

                if item.type in ['flash', 'power']:
                    GLOBAL.total_power += 1
                    GLOBAL.game_total_power += 1

                item.kill()

    def barrage_collide(position) -> None:
        if GLOBAL.is_collide or GLOBAL.is_divide:
            return

        collide = pg.sprite.spritecollide(GLOBAL.decision_point, GLOBAL.barrage_group, False, pg.sprite.collide_mask)

        if collide:
            for barrage in collide:
                if barrage.color != color_dict[6] and not (GLOBAL.is_collide or GLOBAL.is_divide):
                    GLOBAL.is_collide = True
                    Barrage.spawn_particles(GLOBAL.particle_group, (9, 9), position, (10, 16), color_dict[5], color_dict[6])

                    GLOBAL.no_flash = 0
                    GLOBAL.flash -= 1
                    GLOBAL.use_flash += 1
                    if GLOBAL.flash == 0:
                        GLOBAL.is_save = True

                    barrage.kill()

    def bullet_collide() -> None:
        collide = pg.sprite.groupcollide(GLOBAL.bullet_group, GLOBAL.brick_group, False, False)

        if collide:
            for bullet, hit_bricks in collide.items():
                for brick in hit_bricks:
                    if brick.hp > 0:
                        GLOBAL.score += 64
                        brick.hp -= bullet.damage
                    if brick.hp <= 0:
                        if not brick.is_die:
                            Barrage.spawn_particles(GLOBAL.particle_group, (2, 2), brick.rect.center, (4, 8), brick.color, color_dict[6])
                            if hasattr(brick, "free"):
                                GLOBAL.text_part, GLOBAL.text_number, GLOBAL.is_talk, GLOBAL.pop_time = Brick.boss_lose(GLOBAL.text_part)
                            else:
                                spawn_barrage(GLOBAL.stage, GLOBAL.barrage_group, difficulty, brick.type, [brick.color, color_dict[6], color_dict[3]], brick.rect.center, GLOBAL.major.rect.center)
                            if hasattr(brick, "power"):
                                item_spawn(GLOBAL.item_group, brick.power, Item.Item, "power", 2.5, brick.rect.center)
                            if hasattr(brick, "flash"):
                                item_spawn(GLOBAL.item_group, brick.flash, Item.Item, "flash", 2.5, brick.rect.center)
                            brick_blast(GLOBAL.bullet_group, GLOBAL.stage, [brick.color, color_dict[5], color_dict[3]], brick.rect.midleft, brick.rect.midright, brick.rect.midbottom, brick.rect.center)
                            brick.kill()

                        brick.is_die = True
                    if bullet.type in ("bullet", "bomb"):
                        bullet.kill()

    def mask() -> None:
        GLOBAL.backdrop.set_clip(window)
        GLOBAL.backdrop.fill((0, 0, 0, 0))

    def sprite_loader() -> None:
        if GLOBAL.level == 6:
            GLOBAL.char = choose_human()
            GLOBAL.text = json.loads(asset(rf"ASSET\JSON\{GLOBAL.stage}.json").decode('utf-8'))
            GLOBAL.is_talk = True

            GLOBAL.brick_group.add(GLOBAL.char)
        else:
            read_level(asset(rf"ASSET\STAGE\{GLOBAL.stage}-{GLOBAL.level}.stg"), Brick.load_brick, color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)
            Brick.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)

        GLOBAL.pop_time = 0

    def choose_human() -> Ono | Hro | Nre | Qdi:
        char_dict = {
            1: Ono,
            2: Hro,
            3: Nre,
            4: Qdi
        }

        return char_dict.get(GLOBAL.stage)(GLOBAL.major.rect.center, GLOBAL.barrage_group, GLOBAL.particle_group)

    GLOBAL.stage = clamp(args[0], 0, 4)
    GLOBAL.level = clamp(args[1], 0, 5)
    GLOBAL.flash = clamp(args[2], 1, 96)
    GLOBAL.power = clamp(args[3], 0, 32)
    GLOBAL.second_backdrop = picture[GLOBAL.stage]

    mask()

    while True:
        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if GLOBAL.is_divide:
                    GLOBAL.major.free()

                GLOBAL.major.image = turn_side(char_image.subsurface((0, 0, 12, 26)), char_image.subsurface((12, 0, 12, 26)), GLOBAL.is_move_right, GLOBAL.is_move_left)
                GLOBAL.major.x = move_plane(GLOBAL.major.x, (4, 8), GLOBAL.is_move_left, GLOBAL.is_move_right, GLOBAL.is_fast)
                GLOBAL.major.y = 331 if GLOBAL.is_fast else 332
                keep_x = clamp(GLOBAL.major.x, window.left, window.right)
                GLOBAL.major.x = keep_x
                GLOBAL.decision_point.rect.center = (keep_x, GLOBAL.major.y)

                if hasattr(GLOBAL.char, "locate"):
                    GLOBAL.char.locate = GLOBAL.major.rect.center

                barrage_collide(GLOBAL.major.rect.center)
                GLOBAL.is_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_time = invinc(GLOBAL.is_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_time, 180, 6, GLOBAL.major.reset_bullet)

                GLOBAL.item_spawn_time = item_spawn(GLOBAL.item_group, GLOBAL.item_spawn_time >= 45 and len(GLOBAL.brick_group) > 0, Item.Item, "fire", -2, (randint(120, 465), 10), timer=GLOBAL.item_spawn_time)
                if GLOBAL.combo_time <= 1 and GLOBAL.combo > 0:
                    Barrage.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, text_cache[(2 ** GLOBAL.combo, color_dict[6])], text_cache[(2 ** GLOBAL.combo, color_dict[7])], GLOBAL.text_group)
                GLOBAL.combo_time, GLOBAL.combo, GLOBAL.score = combo_counter(GLOBAL.combo_time, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()
                GLOBAL.text_group.update()

                bullet_collide()
                item_collide()

            if not GLOBAL.is_level_load:
                GLOBAL.pop_time, GLOBAL.is_level_load = load_level(GLOBAL.pop_time, GLOBAL.is_level_load, 180, sprite_loader)
            elif len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                GLOBAL.is_summary = True

        KEY.key_event()
        GUI.display(screen, clock)

        clock.tick(60)