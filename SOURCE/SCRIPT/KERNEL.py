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
from LOGIC.STAGE import *
from LOGIC.FILE import *
from LOGIC.SPRITE import *
from LOGIC.DRAW import *
from SCRIPT import GLOBAL
from SCRIPT.HUMAN import Ono, Hro, Nre, Qdi, Kli
import SCRIPT.SPRITE as Sprite


keydown_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL.major, "is_move_right", True),
    pg.K_LEFT: lambda: setattr(GLOBAL.major, "is_move_left", True),
    pg.K_x: lambda: setattr(GLOBAL.major, "is_fast", True),
    pg.K_z: lambda: setattr(GLOBAL.major, "is_shoot", False),
    pg.K_SPACE: lambda: (lambda i: (setattr(GLOBAL.major, 'is_divide', i[0]), setattr(GLOBAL, 'power', i[1])))(single_bomb(GLOBAL.major.is_divide, GLOBAL.power, 12)),
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", True), setattr(GLOBAL, "pop_timer", 0), sound_cache["pick"].play())
}


keydown_talk_dict = {
    pg.K_z: lambda: (setattr(GLOBAL, "text_number", GLOBAL.text_number + 1), setattr(GLOBAL, "pop_timer", 0)),
    pg.K_x: lambda: (setattr(GLOBAL, "is_talk", False), setattr(GLOBAL, "pop_timer", 0))
}


keydown_pause_dict = {
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", False), setattr(GLOBAL, "pop_timer", 0)),
    pg.K_q: lambda: (mode_one(), mode_two())
}


keydown_start_dict = {
    pg.K_z: lambda: (setattr(GLOBAL, "is_run", True), setattr(GLOBAL, "pop_timer", 0), mode_one()),
    pg.K_q: lambda: (pg.time.wait(int(sound_cache["pick"].get_length() * 8000)), sys.exit())
}


keydown_over_dict = {
    pg.K_RETURN: lambda: (save_file(), mode_one(), mode_two()),
    pg.K_ESCAPE: lambda: (mode_one(), mode_two()),
    pg.K_BACKSPACE: lambda: setattr(GLOBAL, "name", GLOBAL.name[:-1])
}


keyup_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL.major, "is_move_right", False),
    pg.K_LEFT: lambda: setattr(GLOBAL.major, "is_move_left", False),
    pg.K_x: lambda: setattr(GLOBAL.major, "is_fast", False),
    pg.K_z: lambda: setattr(GLOBAL.major, "is_shoot", True)
}


def situation(screen: pg.Surface, clock: pg.time.Clock):
    GLOBAL.fps_text, GLOBAL.last_time = update_fps(GLOBAL.fps_text, GLOBAL.last_time, 0, 500, clock)

    text = [
        f"分　{GLOBAL.score:9d}",
        f"形　{GLOBAL.power:02d} , {GLOBAL.total_point:02d}",
        f"闪　{GLOBAL.flash:02d}",
        f"连　{GLOBAL.combo:02d} , {(GLOBAL.major.bullets if GLOBAL.major is not None else 0):02d}"
    ]

    ui(screen, text, GLOBAL.fps_text)


def pause(screen: pg.Surface):
    title = "休息ing"
    text = ["ESC 休息好了", "Q 不玩了"]

    half_menu(screen, title, text)


def load(screen: pg.Surface):
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    title = "这一关是————"
    text = [f"Stage {stage_text} - {GLOBAL.level} !!", "START!!!!"]

    half_menu(screen, title, text)


def talk(screen: pg.Surface):
    try:
        text = GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]
        human = text["char"]
        contest1 = text["1"]
        contest2 = text["2"] if "2" in text else ''

        half_menu(screen, human, [contest1, contest2], (0, 6, 12))
    except KeyError:
        GLOBAL.is_talk = False


def summary(screen: pg.Surface):
    stage = f"Stage {GLOBAL.stage if GLOBAL.stage <= 3 else 'Extra'} - {GLOBAL.level} Cleaer!{'Hit Z Key.' if GLOBAL.level <= 5 else ''}"
    text = [
        f"得点 {GLOBAL.total_point} * 512 = {GLOBAL.total_point * 512}",
        f"无闪 {GLOBAL.unflash} * 4096 = {GLOBAL.unflash * 4096}"
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
        half_menu(screen, stage, text)
    else:
        full_menu(screen, stage, text + over, ["Z 继续", "W 木鱼"], title.get(GLOBAL.stage))


def start(screen: pg.Surface):
    title = "锐行 ~ Thunder Out of the Mountain"
    other = "(C)opyright 2026 An_172N"
    text = ['Ver 1.0.9', '', '', '', '']
    key = ["Z 开玩", "Q 退了"]

    full_menu(screen, title, text, key, other)


def save(screen: pg.Surface):
    title = "抚形日志"
    name = f"由 {GLOBAL.name} 助记"
    text = [
        f"今天是：{datetime.now().strftime('%Y-%m-%d')}",
        f"得到了 {GLOBAL.score} 分",
        f"最远到达的地方是 {GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level} 站",
        f"拾形点率为 {GLOBAL.calculate_item_rate(GLOBAL.game_total_point, GLOBAL.stage <= 3, (153, 61))}",
        f"使用了 {GLOBAL.flashed} 次形闪"
    ]
    key = ["Ent 记录", "ESC 不了"]

    full_menu(screen, title, text, key, name)


def full_menu(surface: pg.Surface, title: str, text: list, key: list, other: str, interval: tuple=(0, 30, 60)):
    group = (
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
    )

    (backdrop := picture[5], backdrop.fill(color_dict[8]))[0]

    menu, GLOBAL.pop_timer = pop_animate(backdrop, font, group, GLOBAL.pop_timer, interval, sound_cache["pick"].play)

    surface.blit(menu, (120, 15))


def half_menu(surface: pg.Surface, title: str, text: list, interval: tuple=(0, 30, 60)):
    group = (
        [{"text": title, "pos": (8, 8)}],
        [{"text": text[0], "pos": (8, 33)}],
        [{"text": text[1], "pos": (8, 58)}]
    )

    (backdrop := picture[5].subsurface((0, 0, 345, 85)), backdrop.fill(color_dict[8]))[0]

    menu, GLOBAL.pop_timer = pop_animate(backdrop, font, group, GLOBAL.pop_timer, interval, sound_cache["pick"].play)

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


def save_file():
    name = GLOBAL.name.translate(str.maketrans('!<>:"/\\|?*', '__________'))
    date_time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    dump_content = {
        '助记者': GLOBAL.name,
        '分数': GLOBAL.score,
        '最远到达的地方': f"{GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level}",
        '拾形点率': GLOBAL.calculate_item_rate(GLOBAL.game_total_point, GLOBAL.stage <= 3, (153, 61)),
        '形闪次数': GLOBAL.flashed,
        '记录日期': date_time[0]
    }

    save_record(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{date_time[0]}_{date_time[1]}.json', "锐山抚形日志", dump_content)


def summary_logic():
    def level_logic():
        mode_one()

        GLOBAL.stage, GLOBAL.level = next_level((GLOBAL.stage, GLOBAL.level), 6)
        GLOBAL.unflash += 1

    def close_summary(numbers: tuple, final: object, proceed: object, *args):
        return final(*args) if numbers[0][0] >= numbers[1][0] and numbers[0][1] == numbers[1][1] else proceed(*args)

    GLOBAL.score += GLOBAL.score_summary(GLOBAL.total_point, GLOBAL.power, GLOBAL.unflash, GLOBAL.combo, (GLOBAL.stage, GLOBAL.level))
    GLOBAL.is_summary = False

    close_summary(((GLOBAL.stage, GLOBAL.level), (3, 6)), lambda: setattr(GLOBAL, 'is_save', True), level_logic)

    GLOBAL.pop_timer = 0


def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYUP:
            if not GLOBAL.is_summary and GLOBAL.is_level_load and not GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keyup_game_dict:
                keyup_game_dict[event.key]()
        elif event.type == pg.KEYDOWN:
            for condition, handler in [
                (
                    lambda: not GLOBAL.is_run and event.key in keydown_start_dict,
                    lambda: (sound_cache["pick"].play(), keydown_start_dict[event.key]())
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
                    lambda: (summary_logic(), sound_cache["pick"].play()) if event.key == pg.K_z else (sound_cache["pick"].play() if event.key == pg.K_w and GLOBAL.level == 6 else None)
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
    GLOBAL.pop_timer = 0

    GLOBAL.item_group.empty()
    GLOBAL.brick_group.empty()
    GLOBAL.plane_group.empty()
    GLOBAL.bullet_group.empty()
    GLOBAL.particle_group.empty()
    GLOBAL.barrage_group.empty()

    GLOBAL.major = Kli(GLOBAL.bullet_group, GLOBAL.particle_group, GLOBAL.plane_group)
    GLOBAL.total_point = 0
    GLOBAL.item_spawn_timer = 0
    GLOBAL.combo = 0
    GLOBAL.combo_timer = 120
    GLOBAL.text_part = 0
    GLOBAL.text_number = 0


def mode_two():
    GLOBAL.stage = 1
    GLOBAL.level = 1
    GLOBAL.char = None
    GLOBAL.unflash = 1
    GLOBAL.flash = 3
    GLOBAL.score = 0
    GLOBAL.flashed = 0
    GLOBAL.power = 0
    GLOBAL.game_total_point = 0
    GLOBAL.is_run = False


def spawn_barrage(stage: int, group: pg.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, locate: tuple):
    barrage_dict = {
        1: Sprite.circle_barrage,
        2: Sprite.polygon_barrage
    }

    if random() <= fib[stage - 1]:
        if stage in [1, 2]:
            barrage_dict.get(stage)(type, color, spawn_pos, locate, group)
        elif stage == 3:
            Sprite.line_barrage(color, locate, group)
        else:
            Sprite.point_barrage(type, color, locate, group)


def brick_blast(group: pg.sprite.Group, stage: int, color: list, *spawn_pos: tuple):
    process_dict = {
        1: Sprite.circle_brick,
        3: Sprite.line_brick
    }

    if color[0] == color_dict[6]:
        if stage == 2:
            Sprite.polygon_brick(group, spawn_pos[0], spawn_pos[1], spawn_pos[2])
        elif stage in [1, 3]:
            process_dict.get(stage)(group, spawn_pos[3])
        else:
            Sprite.point_brick(group)


def item_collide():
    collide = pg.sprite.spritecollide(GLOBAL.major, GLOBAL.item_group, False)

    if collide:
        for item in collide:
            GLOBAL.combo_timer = 120
            GLOBAL.major.bullets = int(clamp(GLOBAL.major.bullets + 1, 0, 6))

            if item.type in ['flash', 'power']:
                if item.type == "power":
                    GLOBAL.power = int(clamp(GLOBAL.power + 1, 0, 32))
                    GLOBAL.combo += 1

                    sound_cache["pick"].play()
                elif item.type == "flash":
                    GLOBAL.flash += 1
                    GLOBAL.combo += 1

                    Sprite.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, text_cache[("extend", color_dict[6])], text_cache[("extend", color_dict[2])], GLOBAL.particle_group)

                GLOBAL.total_point += 1
                GLOBAL.game_total_point += 1

            sound_cache["charge"].play(maxtime=24)
            item.kill()


def barrage_collide(position):
    collide = pg.sprite.spritecollide(GLOBAL.major.decision_box, GLOBAL.barrage_group, False, pg.sprite.collide_mask)

    if collide:
        for barrage in collide:
            if barrage.color != color_dict[6]:
                if not (GLOBAL.major.is_collide or GLOBAL.major.is_divide):
                    GLOBAL.major.is_collide = True
                    GLOBAL.unflash = 0
                    GLOBAL.flash -= 1
                    GLOBAL.flashed += 1
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
                            GLOBAL.text_part, GLOBAL.text_number, GLOBAL.is_talk, GLOBAL.pop_timer = Sprite.boss_lose(GLOBAL.text_part)
                        else:
                            spawn_barrage(GLOBAL.stage, GLOBAL.barrage_group, difficulty, brick.type, [brick.color, color_dict[6], color_dict[3]], brick.rect.center, GLOBAL.major.rect.center)

                        if sound_cache["fire"].get_num_channels() < 2:
                            sound_cache["fire"].play()
                        if hasattr(brick, "power"):
                            spawn_sprite(brick.power, Sprite.Item, "power", 2.5, brick.rect.center, GLOBAL.item_group)
                        if hasattr(brick, "flash"):
                            spawn_sprite(brick.flash, Sprite.Item, "flash", 2.5, brick.rect.center, GLOBAL.item_group)
                        brick_blast(GLOBAL.bullet_group, GLOBAL.stage, [brick.color, color_dict[5], color_dict[3]], brick.rect.midleft, brick.rect.midright, brick.rect.midbottom, brick.rect.center)
                        brick.kill()

                    brick.is_die = True
                if bullet.type in ("bullet", "bomb"):
                    bullet.kill()


def sprite_loader():
    if GLOBAL.level == 6:
        GLOBAL.char = choose_human()
        GLOBAL.text = json.loads(asset(rf"ASSET\JSON\{GLOBAL.stage}.json").decode('utf-8'))
        GLOBAL.is_talk = True

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        read_level(asset(rf"ASSET\STAGE\{GLOBAL.stage}-{GLOBAL.level}.stg"), Sprite.load_brick, color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)
        Sprite.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)

    GLOBAL.wait_load_timer = 0
    GLOBAL.pop_timer = 0


def choose_human() -> Ono | Hro | Nre | Qdi:
    char_dict = {
        1: Ono,
        2: Hro,
        3: Nre,
        4: Qdi
    }

    return char_dict.get(GLOBAL.stage)(GLOBAL.major.rect.center, GLOBAL.barrage_group, GLOBAL.particle_group)


def display(screen: pg.Surface, clock: pg.time.Clock):
    if GLOBAL.is_run:
        screen.blit(picture[GLOBAL.stage], (120, 15))

        GLOBAL.bullet_group.draw(screen)
        if GLOBAL.major is not None and GLOBAL.major.is_visitable:
            GLOBAL.plane_group.draw(screen)
        GLOBAL.brick_group.draw(screen)
        GLOBAL.item_group.draw(screen)
        GLOBAL.particle_group.draw(screen)
        GLOBAL.barrage_group.draw(screen)

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

    screen.blit(picture[6], (0, 0))
    situation(screen, clock)

    pg.display.flip()


def update(clock: pg.time.Clock, screen: pg.Surface, args: tuple):
    GLOBAL.stage = clamp(args[0], 1, 4)
    GLOBAL.level = clamp(args[1], 1, 6)
    GLOBAL.flash = clamp(args[2], 1, 96)
    GLOBAL.power = clamp(args[3], 0, 32)

    picture[6].set_clip(window)
    picture[6].fill((0, 0, 0, 0))

    while True:
        key_event()

        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if hasattr(GLOBAL.char, "locate"):
                    GLOBAL.char.locate = GLOBAL.major.rect.center
                GLOBAL.major.power = GLOBAL.power
                GLOBAL.item_spawn_timer = spawn_sprite(GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0, Sprite.Item, "fire", -2, (randint(120, 465), 10), GLOBAL.item_group, timer=GLOBAL.item_spawn_timer)
                if GLOBAL.combo_timer <= 1 and GLOBAL.combo > 0:
                    Sprite.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, text_cache[(2 ** GLOBAL.combo, color_dict[6])], text_cache[(2 ** GLOBAL.combo, color_dict[7])], GLOBAL.particle_group)
                GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score = count_combo(GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.plane_group.update()
                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()

                barrage_collide(GLOBAL.major.rect.center)
                bullet_collide()

                if len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                    GLOBAL.is_summary = True

                item_collide()
            if not GLOBAL.is_level_load:
                GLOBAL.wait_load_timer, GLOBAL.is_level_load = load_level(GLOBAL.wait_load_timer, GLOBAL.is_level_load, 90, sprite_loader)

        display(screen, clock)

        clock.tick(60)