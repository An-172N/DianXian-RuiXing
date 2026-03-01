# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import json
import sys
import os
from datetime import datetime
from random import randint, random


import pygame as pg


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.PLANE import *
from LOGIC.ITEM import *
from LOGIC.STAGE import *
from LOGIC.FILE import *
from LOGIC.DRAW import *
from SCRIPT import GLOBAL
from SCRIPT.HUMAN import Ono, Hro, Nre, Qdi, Kli
import SCRIPT.SPRITE as Sprite


keydown_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", True),
    pg.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", True),
    pg.K_x: lambda: setattr(GLOBAL, "is_fast", True),
    pg.K_z: lambda: setattr(GLOBAL, "is_shoot", False),
    pg.K_SPACE: lambda: (lambda ret: (setattr(GLOBAL, 'is_divide', ret[0]), setattr(GLOBAL, 'power', ret[1])))(single_bomb(GLOBAL.is_divide, GLOBAL.power, 12)),
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", True), setattr(GLOBAL, "pop_time", 0), sound_cache["pick"].play())
}


keydown_talk_dict = {
    pg.K_z: lambda: (setattr(GLOBAL, "text_number", GLOBAL.text_number + 1), setattr(GLOBAL, "pop_time", 0)),
    pg.K_x: lambda: (setattr(GLOBAL, "is_talk", False), setattr(GLOBAL, "pop_time", 0))
}


keydown_pause_dict = {
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", False), setattr(GLOBAL, "pop_time", 0)),
    pg.K_q: lambda: (mode_one(), mode_two())
}


keydown_start_dict = {
    pg.K_z: lambda: (setattr(GLOBAL, "is_run", True), setattr(GLOBAL, "pop_time", 0), next_level()),
    pg.K_q: lambda: (sound_cache["pick"].play(), pg.time.wait(int(sound_cache["pick"].get_length() * 8000)), sys.exit())
}


keydown_over_dict = {
    pg.K_RETURN: lambda: (save_file(), mode_one(), mode_two()),
    pg.K_ESCAPE: lambda: (mode_one(), mode_two()),
    pg.K_BACKSPACE: lambda: setattr(GLOBAL, "name", GLOBAL.name[:-1])
}


keydown_summary_dict = {
    pg.K_z: lambda: summary_logic()
}


keyup_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", False),
    pg.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", False),
    pg.K_x: lambda: setattr(GLOBAL, "is_fast", False),
    pg.K_z: lambda: setattr(GLOBAL, "is_shoot", True)
}


def situation(screen: pg.Surface, clock: pg.time.Clock):
    GLOBAL.fps_text, GLOBAL.last_time = update_fps(GLOBAL.fps_text, GLOBAL.last_time, 0, 500, clock)

    text = [
        f"分　{GLOBAL.score:9d}",
        f"形　{GLOBAL.power:02d} , {GLOBAL.total_power:02d}",
        f"闪　{GLOBAL.flash:02d}",
        f"连　{GLOBAL.combo:02d} , {GLOBAL.shoot_count:02d}"
    ]

    ui(screen, text, GLOBAL.fps_text)


def pause(screen: pg.Surface):
    title = "休息ing"
    text = ["ESC 休息好了", "Q 不玩了"]

    return half_menu(screen, title, text)


def load(screen: pg.Surface):
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    title = "这一关是————"
    text = [f"Stage {stage_text} - {GLOBAL.level} !!", "START!!!!"]

    return half_menu(screen, title, text)


def talk(screen: pg.Surface):
    try:
        human = GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["char"]
        text = [
            GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["1"],
            GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["2"] if "2" in GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"] else ''
        ]

        return half_menu(screen, human, text, (0, 6, 12))
    except KeyError:
        GLOBAL.is_talk = False


def summary(screen: pg.Surface):
    stage = (f"Stage {GLOBAL.stage if GLOBAL.stage <= 3 else 'Extra'} - {GLOBAL.level} Cleaer!{"Hit Z Key." if GLOBAL.level <= 5 else ""}")
    text = [
        f"得点 {GLOBAL.total_power} * 512 = {GLOBAL.total_power * 512}",
        f"无闪 {GLOBAL.no_flash} * 4096 = {GLOBAL.no_flash * 4096}"
    ]
    over = [
        f"面数 {GLOBAL.stage} * 16384 = {GLOBAL.stage * 16384}",
        f"形力 {GLOBAL.power} / 32 * 8192 = {int(GLOBAL.power / 32 * 8192)}",
        ""
    ]
    title = {
        1: "水边的秋霜店 ~ Sweet Reservoir",
        2: "X 在树林 ~ Hypnotized",
        3: "午夜行至最高峰 ~ Thunder Studio",
        4: "享受禁饮 ~ Point's Hideaway"
    }

    if GLOBAL.level <= 5:
        return half_menu(screen, stage, text)
    else:
        return full_menu(screen, stage, text + over, ["Z 继续", "W 木鱼"], title.get(GLOBAL.stage))


def start(screen: pg.Surface):
    title = "锐行 ~ Thunder Out of the Mountain"
    other = "(C)opyright 2026 An_172N"
    text = ['Ver 1.0.8', '', '', '', '']
    key = ["Z 开玩", "Q 退了"]

    return full_menu(screen, title, text, key, other)


def save(screen: pg.Surface):
    title = "抚形日志"
    name = f"由 {GLOBAL.name} 助记"
    text = [
        f"今天是：{datetime.now().strftime('%Y-%m-%d')}",
        f"得到了 {GLOBAL.score} 分",
        f"最远到达的地方是 {GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level} 站",
        f"拾形点率为 {GLOBAL.calculate_item_rate(GLOBAL.game_total_power, GLOBAL.stage <= 3, (153, 61))}",
        f"使用了 {GLOBAL.use_flash} 次形闪"
    ]
    key = ["Ent 记录", "ESC 不了"]

    return full_menu(screen, title, text, key, name)


def full_menu(surface: pg.Surface, title: str, text: list, key: list, other: str, interval: tuple=(0, 30, 60)):
    group = [
        [
            {"text": title, "pos": (8, 10)},
            {"text": other, "pos": (8, 305)}
        ],
        [
            {"text": text[0], "pos": (8, 60)},
            {"text": text[1], "pos": (8, 85)},
            {"text": text[2], "pos": (8, 110)},
            {"text": text[3], "pos": (8, 135)},
            {"text": text[4], "pos": (8, 160)}
        ],
        [
            {"text": key[0], "pos": (270, 220)},
            {"text": key[1], "pos": (270, 270)}
        ]
    ]

    (backdrop := picture[5], backdrop.fill(color_dict[8]))[0]

    menu, GLOBAL.pop_time = pop_animate(backdrop, font, group, GLOBAL.pop_time, interval)

    surface.blit(menu, (120, 15))


def half_menu(surface: pg.Surface, title: str, text: list, interval: tuple=(0, 30, 60)):
    group = [
        [{"text": title, "pos": (8, 8)}],
        [{"text": text[0], "pos": (8, 33)}],
        [{"text": text[1], "pos": (8, 58)}]
    ]

    (backdrop := picture[5].subsurface((0, 0, 345, 85)), backdrop.fill(color_dict[8]))[0]

    menu, GLOBAL.pop_time = pop_animate(backdrop, font, group, GLOBAL.pop_time, interval)

    surface.blit(menu, (120, 15))


def ui(surface: pg.Surface, text: list, fps: str):
    text_type = [
        {"text": text[0], "pos": (8, 25)},
        {"text": text[1], "pos": (8, 270)},
        {"text": text[2], "pos": (8, 295)},
        {"text": text[3], "pos": (8, 320)},
        {"text": fps, "pos": (405, 343)}
    ]

    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, color_dict[6])

        surface.blit(text, text_info["pos"])


def pop_animate(surface: pg.Surface, font: pg.font.Font, group: list, timer: int, interval: tuple, color: tuple=(255, 255, 255)) -> tuple:
    def for_text(timer: int, interval: int, gather: list):
        if timer >= interval:
            for i in gather:
                text = font.render(i["text"], False, color).convert_alpha()

                surface.blit(text, i["pos"])

    for_text(timer, interval[0], group[0])
    for_text(timer, interval[1], group[1])
    for_text(timer, interval[2], group[2])

    if timer < interval[2]:
        timer += 1

        if timer == interval[2]:
            sound_cache["pick"].play()

    return surface, timer


def display(screen: pg.Surface, clock: pg.time.Clock):
    screen.blit(GLOBAL.second_backdrop, (120, 15))

    GLOBAL.bullet_group.draw(screen)
    if GLOBAL.is_visitable:
        GLOBAL.plane_group.draw(screen)
    GLOBAL.brick_group.draw(screen)
    GLOBAL.item_group.draw(screen)
    GLOBAL.particle_group.draw(screen)
    GLOBAL.barrage_group.draw(screen)
    GLOBAL.text_group.draw(screen)

    for condition, func in [
        (lambda: not GLOBAL.is_run, start),
        (lambda: GLOBAL.is_pause, pause),
        (lambda: not GLOBAL.is_level_load, load),
        (lambda: GLOBAL.is_talk, talk),
        (lambda: GLOBAL.is_summary, summary),
        (lambda: GLOBAL.is_save, save),
    ]:
        if condition():
            func(screen)

            break

    screen.blit(GLOBAL.backdrop, (0, 0))
    situation(screen, clock)

    pg.display.flip()


def save_file():
    name = GLOBAL.name.translate(str.maketrans('!<>:"/\\|?*', '__________'))
    date_time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    dump_content = {
        '助记者': GLOBAL.name,
        '分数': GLOBAL.score,
        '最远到达的地方': f"{GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level}",
        '拾形点率': GLOBAL.calculate_item_rate(GLOBAL.game_total_power, GLOBAL.stage <= 3, (153, 61)),
        '形闪次数': GLOBAL.use_flash,
        '记录日期': date_time[0]
    }

    save_record(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{date_time[0]}_{date_time[1]}.json', "锐山抚形日志", dump_content)


def next_level():
    mode_one()

    GLOBAL.stage, GLOBAL.level = level_logic((GLOBAL.stage, GLOBAL.level), 6)
    GLOBAL.no_flash += 1


def summary_logic():
    GLOBAL.score += GLOBAL.score_summary(GLOBAL.total_power, GLOBAL.power, GLOBAL.no_flash, GLOBAL.combo, (GLOBAL.stage, GLOBAL.level))
    GLOBAL.is_summary = False

    close_summary(((GLOBAL.stage, GLOBAL.level), (3, 6)), lambda: setattr(GLOBAL, 'is_save', True), next_level)

    GLOBAL.pop_time = 0
    GLOBAL.second_backdrop = picture[GLOBAL.stage]


def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYUP:
            if GLOBAL.is_run and event.key in keyup_game_dict:
                keyup_game_dict[event.key]()
        elif event.type == pg.KEYDOWN:
            for condition, handler in [
                (
                    lambda: not GLOBAL.is_run and event.key in keydown_start_dict,
                    lambda: (keydown_start_dict[event.key](), sound_cache["pick"].play())
                ),
                (
                    lambda: GLOBAL.is_save,
                    lambda: ((keydown_over_dict[event.key]() if event.key in keydown_over_dict else setattr(GLOBAL, 'name', (GLOBAL.name + event.unicode)[:8])), sound_cache["pick"].play())
                ),
                (
                    lambda: GLOBAL.is_pause and event.key in keydown_pause_dict,
                    lambda: (keydown_pause_dict[event.key](), sound_cache["pick"].play())
                ),
                (
                    lambda: GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_talk_dict,
                    lambda: (keydown_talk_dict[event.key](), sound_cache["pick"].play())
                ),
                (
                    lambda: GLOBAL.is_summary,
                    lambda: (keydown_summary_dict[event.key]() or True) and sound_cache["pick"].play() if event.key in keydown_summary_dict else (sound_cache["pick"].play() if event.key == pg.K_w and GLOBAL.level == 6 else None)
                ),
                (
                    lambda: not GLOBAL.is_summary and GLOBAL.is_level_load and not GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_game_dict,
                    lambda: keydown_game_dict[event.key]()
                ),
            ]:
                if condition():
                    handler()

                    break


def mode_one():
    GLOBAL.is_pause = False
    GLOBAL.is_summary = False
    GLOBAL.is_talk = False
    GLOBAL.is_save = False
    GLOBAL.is_level_load = False
    GLOBAL.pop_time = 0

    GLOBAL.item_group.empty()
    GLOBAL.brick_group.empty()
    GLOBAL.plane_group.empty()
    GLOBAL.bullet_group.empty()
    GLOBAL.particle_group.empty()
    GLOBAL.barrage_group.empty()
    GLOBAL.text_group.empty()

    GLOBAL.is_collide = False
    GLOBAL.is_divide = False
    GLOBAL.cooldown_time = 0
    GLOBAL.major = Kli(GLOBAL.bullet_group, GLOBAL.particle_group, GLOBAL.plane_group)
    GLOBAL.decision_point = Sprite.Rect(rectangle((2, 2), 0, color_dict[7]).convert(), GLOBAL.plane_group, pos=(292, 332), mask=True)
    GLOBAL.total_power = 0
    GLOBAL.shoot_count = 0
    GLOBAL.is_shoot = True
    GLOBAL.item_spawn_time = 0
    GLOBAL.combo = 0
    GLOBAL.combo_time = 120
    GLOBAL.text_part = 0
    GLOBAL.text_number = 0


def mode_two():
    GLOBAL.stage = 1
    GLOBAL.level = 0
    GLOBAL.char = None
    GLOBAL.second_backdrop = picture[GLOBAL.stage]
    GLOBAL.no_flash = 0
    GLOBAL.flash = 3
    GLOBAL.score = 0
    GLOBAL.use_flash = 0
    GLOBAL.power = 0
    GLOBAL.is_shoot = False
    GLOBAL.is_run = False


def update(clock: pg.time.Clock, screen: pg.Surface, args: tuple):
    def spawn_barrage(stage: int, group: pg.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, locate: tuple):
        barrage_dict = {
            1: Sprite.circle_barrage,
            2: Sprite.polygon_barrage
        }

        if random() <= fib[stage - 1]:
            if stage in [1, 2]:
                return barrage_dict.get(stage)(type, color, spawn_pos, locate, group)
            elif stage == 3:
                return Sprite.line_barrage(color, locate, group)
            else:
                return Sprite.point_barrage(type, color, locate, group)

    def brick_blast(group: pg.sprite.Group, stage: int, color: list, *spawn_pos: tuple):
        process_dict = {
            1: Sprite.circle_brick,
            3: Sprite.line_brick
        }

        if color[0] == color_dict[6]:
            if stage == 2:
                return Sprite.polygon_brick(group, spawn_pos[0], spawn_pos[1], spawn_pos[2])
            elif stage in [1, 3]:
                return process_dict.get(stage)(group, spawn_pos[3])
            else:
                return Sprite.point_brick(group)

    def item_collide():
        if GLOBAL.is_shoot and GLOBAL.shoot_count > 0:
            GLOBAL.major.fire(GLOBAL.power)
            Sprite.spawn_particles(GLOBAL.particle_group, (2, 2), GLOBAL.major.rect.center, (4, 8), GLOBAL.major.color)

            GLOBAL.shoot_count -= 1

        collide = pg.sprite.spritecollide(GLOBAL.major, GLOBAL.item_group, False)

        if collide:
            for item in collide:
                GLOBAL.combo_time = 120
                GLOBAL.shoot_count = int(clamp(GLOBAL.shoot_count + 1, 0, 6))

                sound_cache["charge"].play(maxtime=24)

                if item.type == "power":
                    GLOBAL.power = int(clamp(GLOBAL.power + 1, 0, 32))
                    GLOBAL.combo += 1

                    sound_cache["pick"].play()
                elif item.type == "flash":
                    GLOBAL.flash += 1
                    GLOBAL.combo += 1

                    Sprite.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, text_cache[("extend", color_dict[6])], text_cache[("extend", color_dict[2])], GLOBAL.text_group)
                if item.type in ['flash', 'power']:
                    GLOBAL.total_power += 1
                    GLOBAL.game_total_power += 1

                item.kill()

    def barrage_collide(position):
        collide = pg.sprite.spritecollide(GLOBAL.decision_point, GLOBAL.barrage_group, False, pg.sprite.collide_mask)

        if collide:
            for barrage in collide:
                if barrage.color != color_dict[6]:
                    if not (GLOBAL.is_collide or GLOBAL.is_divide):
                        GLOBAL.is_collide = True
                        GLOBAL.no_flash = 0
                        GLOBAL.flash -= 1
                        GLOBAL.use_flash += 1
                        if GLOBAL.flash == 0:
                            GLOBAL.is_save = True

                        Sprite.spawn_particles(GLOBAL.particle_group, (9, 9), position, (10, 16), color_dict[5], color_dict[6])
                        sound_cache["fire"].play()

                    barrage.kill()

    def bullet_collide():
        collide = pg.sprite.groupcollide(GLOBAL.bullet_group, GLOBAL.brick_group, False, False)

        if collide:
            for bullet, hit_bricks in collide.items():
                for brick in hit_bricks:
                    if brick.hp > 0:
                        GLOBAL.score += 64
                        brick.hp -= bullet.damage
                    if brick.hp <= 0:
                        if not brick.is_die:
                            Sprite.spawn_particles(GLOBAL.particle_group, (2, 2), brick.rect.center, (4, 8), brick.color, color_dict[6])
                            if hasattr(brick, "free"):
                                GLOBAL.text_part, GLOBAL.text_number, GLOBAL.is_talk, GLOBAL.pop_time = Sprite.boss_lose(GLOBAL.text_part)
                            else:
                                spawn_barrage(GLOBAL.stage, GLOBAL.barrage_group, difficulty, brick.type, [brick.color, color_dict[6], color_dict[3]], brick.rect.center, GLOBAL.major.rect.center)
                            if sound_cache["fire"].get_num_channels() < 2:
                                sound_cache["fire"].play()
                            if hasattr(brick, "power"):
                                item_spawn(GLOBAL.item_group, brick.power, Sprite.Item, "power", 2.5, brick.rect.center)
                            if hasattr(brick, "flash"):
                                item_spawn(GLOBAL.item_group, brick.flash, Sprite.Item, "flash", 2.5, brick.rect.center)
                            brick_blast(GLOBAL.bullet_group, GLOBAL.stage, [brick.color, color_dict[5], color_dict[3]], brick.rect.midleft, brick.rect.midright, brick.rect.midbottom, brick.rect.center)
                            brick.kill()

                        brick.is_die = True
                    if bullet.type in ("bullet", "bomb"):
                        bullet.kill()

    def mask():
        GLOBAL.backdrop.set_clip(window)
        GLOBAL.backdrop.fill((0, 0, 0, 0))

    def sprite_loader():
        if GLOBAL.level == 6:
            GLOBAL.char = choose_human()
            GLOBAL.text = json.loads(asset(rf"ASSET\JSON\{GLOBAL.stage}.json").decode('utf-8'))
            GLOBAL.is_talk = True

            GLOBAL.brick_group.add(GLOBAL.char)
        else:
            read_level(asset(rf"ASSET\STAGE\{GLOBAL.stage}-{GLOBAL.level}.stg"), Sprite.load_brick, color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)
            Sprite.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)

        GLOBAL.wait_load_time = 0
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
                GLOBAL.major.x = move_plane(GLOBAL.major.x, (3, 8), GLOBAL.is_move_left, GLOBAL.is_move_right, GLOBAL.is_fast)
                GLOBAL.major.y = 331 if GLOBAL.is_fast else 332
                keep_x = clamp(GLOBAL.major.x, window.left, window.right)
                GLOBAL.major.x = keep_x
                GLOBAL.decision_point.rect.center = (keep_x, GLOBAL.major.y)

                if hasattr(GLOBAL.char, "locate"):
                    GLOBAL.char.locate = GLOBAL.major.rect.center

                barrage_collide(GLOBAL.major.rect.center)
                GLOBAL.is_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_time = invinc(GLOBAL.is_divide, GLOBAL.is_collide, GLOBAL.is_visitable, GLOBAL.cooldown_time, 180, 6, GLOBAL.major.reset_bullet)

                GLOBAL.item_spawn_time = item_spawn(GLOBAL.item_group, GLOBAL.item_spawn_time >= 45 and len(GLOBAL.brick_group) > 0, Sprite.Item, "fire", -2, (randint(120, 465), 10), timer=GLOBAL.item_spawn_time)
                if GLOBAL.combo_time <= 1 and GLOBAL.combo > 0:
                    Sprite.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, text_cache[(2 ** GLOBAL.combo, color_dict[6])], text_cache[(2 ** GLOBAL.combo, color_dict[7])], GLOBAL.text_group)
                GLOBAL.combo_time, GLOBAL.combo, GLOBAL.score = combo_counter(GLOBAL.combo_time, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()
                GLOBAL.text_group.update()

                bullet_collide()

                if len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                    GLOBAL.is_summary = True

                item_collide()
            if not GLOBAL.is_level_load:
                GLOBAL.wait_load_time, GLOBAL.is_level_load = load_level(GLOBAL.wait_load_time, GLOBAL.is_level_load, 90, sprite_loader)

        key_event()
        display(screen, clock)

        clock.tick(60)