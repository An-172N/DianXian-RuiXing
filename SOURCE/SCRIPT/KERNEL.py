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
from LOGIC.STAGE import *
from LOGIC.FILE import *
from LOGIC.SPRITE import *
from SCRIPT import GLOBAL
from SCRIPT.HUMAN import Ono, Hro, Nre, Qdi, Kli
import SCRIPT.SPRITE as Sprite


keydown_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL.major, "is_move_right", True),
    pg.K_LEFT: lambda: setattr(GLOBAL.major, "is_move_left", True),
    pg.K_x: lambda: setattr(GLOBAL.major, "is_fast", True),
    pg.K_z: lambda: setattr(GLOBAL.major, "is_shoot", False),
    pg.K_SPACE: lambda: (lambda i: (setattr(GLOBAL.major.divided, 'condition', i[0]), setattr(GLOBAL, 'power', i[1])))(bomb(GLOBAL.major.divided.condition, GLOBAL.power, 12)),
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", True), setattr(GLOBAL, "pop_timer", 0), sound_cache["pick"].play())
}


keydown_talk_dict = {
    pg.K_z: lambda: (setattr(GLOBAL, "text_number", GLOBAL.text_number + 1), setattr(GLOBAL, "pop_timer", 0)),
    pg.K_x: lambda: (setattr(GLOBAL, "is_talk", False), setattr(GLOBAL, "pop_timer", 0))
}


keydown_pause_dict = {
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", False), setattr(GLOBAL, "pop_timer", 0)),
    pg.K_DELETE: lambda: (mode_one(), mode_two())
}


keydown_start_dict = {
    pg.K_z: lambda: (setattr(GLOBAL, "is_run", True), setattr(GLOBAL, "pop_timer", 0), mode_one()),
    pg.K_q: lambda: setattr(GLOBAL, "is_exit", True),
    pg.K_c: lambda: (setattr(GLOBAL, "is_check", True), setattr(GLOBAL, "pop_timer", 0)) if GLOBAL.total_files > 0 else None
}


keydown_over_dict = {
    pg.K_RETURN: lambda: (save_file(), mode_one(), mode_two()),
    pg.K_ESCAPE: lambda: (mode_one(), mode_two()),
    pg.K_BACKSPACE: lambda: setattr(GLOBAL, "name", GLOBAL.name[:-1])
}


keydown_check_dict = {
    pg.K_DELETE: lambda: (os.remove(GLOBAL.json_files[GLOBAL.index]), setattr(GLOBAL, "json_files", get(f'{os.environ["USERPROFILE"]}/Saved Games/DX00')), setattr(GLOBAL, "total_files", len(GLOBAL.json_files)), setattr(GLOBAL, "index", clamp(GLOBAL.index, 0, GLOBAL.total_files - 1)), setattr(GLOBAL, "pop_timer", 0)) if GLOBAL.total_files > 0 else None,
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_check", False), setattr(GLOBAL, "index", 0), setattr(GLOBAL, "pop_timer", 0)),
    pg.K_LEFT: lambda: (setattr(GLOBAL, "index", GLOBAL.index - 1), setattr(GLOBAL, "pop_timer", 0)) if GLOBAL.index > 0 else None,
    pg.K_RIGHT: lambda: (setattr(GLOBAL, "index", GLOBAL.index + 1), setattr(GLOBAL, "pop_timer", 0)) if GLOBAL.index < GLOBAL.total_files - 1 else None
}


keyup_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL.major, "is_move_right", False),
    pg.K_LEFT: lambda: setattr(GLOBAL.major, "is_move_left", False),
    pg.K_x: lambda: setattr(GLOBAL.major, "is_fast", False),
    pg.K_z: lambda: setattr(GLOBAL.major, "is_shoot", True)
}


def situation(screen: pg.Surface, clock: pg.time.Clock):
    text = (
        f"{GLOBAL.score:9d}",
        f"{GLOBAL.power:02d} , {GLOBAL.total_point:02d}",
        f"{GLOBAL.flash:02d}",
        f"{GLOBAL.combo:02d} , {(GLOBAL.major.bullets if GLOBAL.major is not None else 0):02d}"
    )

    ui(screen, text, f"{int(clock.get_fps())} FPS")


def pause_menu(screen: pg.Surface):
    title = "休息ing"
    text = ("Esc 休息好了", "Del 不玩了")

    half_menu(screen, title, text)


def load_menu(screen: pg.Surface):
    title = "这一关是————"
    text = (f"Stage {GLOBAL.stage if GLOBAL.stage < 3 else 'Final' if GLOBAL.stage == 3 else 'Extra'} - {GLOBAL.level} !!", "START!!!!")

    half_menu(screen, title, text)


def talk_menu(screen: pg.Surface):
    try:
        text = GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]
        human = text["char"]
        content = (text["1"], text["2"] if "2" in text else '')

        half_menu(screen, human, content, (0, 6, 12))
    except KeyError:
        GLOBAL.is_talk = False


def summary_menu(screen: pg.Surface):
    stage = f"Stage {GLOBAL.stage if GLOBAL.stage <= 3 else 'Extra'} - {GLOBAL.level} Clear! {'Hit Z Key.' if GLOBAL.level <= 5 else ''}"
    text = (
        f"得点 {GLOBAL.total_point} * 512 = {GLOBAL.total_point * 512}",
        f"无闪 {GLOBAL.unflash} * 4096 = {GLOBAL.unflash * 4096}",
        f"面数 {GLOBAL.stage} * 16384 = {GLOBAL.stage * 16384}",
        f"形力 {GLOBAL.power} / 32 * 8192 = {int(GLOBAL.power / 32 * 8192)}",
        ""
    )
    title = {
        1: "水边的秋霜店 ~ Sweet Reservoir",
        2: "X 在树林 ~ Hypnotized",
        3: "午夜行至最高峰 ~ Thunder Studio",
        4: "享受禁饮 ~ Point's Hideaway"
    }
    key = ("Z 继续", "", "")

    half_menu(screen, stage, (text[0], text[1])) if GLOBAL.level <= 5 else full_menu(screen, stage, text, key, title.get(GLOBAL.stage))


def start_menu(screen: pg.Surface):
    title = "锐行 ~ Thunder Out of the Mountain"
    other = "(C)opyright 2026 An_172N"
    text = ('Ver 1.1.0', '', '', '', '')
    key = ("Z 开玩", "C 日志", "Q 退了")

    full_menu(screen, title, text, key, other)


def save_menu(screen: pg.Surface):
    shortly = False
    title = "抚形日志"
    name = f"谢谢 {GLOBAL.name} 的帮助"
    text = (
        f"今天是 {datetime.now().strftime('%Y-%m-%d')}",
        f"得到了 {GLOBAL.score} 分",
        f"最远到达的地方是 {GLOBAL.stage if GLOBAL.stage < 3 else 'Final' if GLOBAL.stage == 3 else 'Extra'} - {GLOBAL.level} 站",
        f"拾形点率为 {GLOBAL.calculate_item_rate(GLOBAL.game_total_point, GLOBAL.stage <= 3, (153, 61))}",
        f"使用了 {GLOBAL.flashed} 次形闪{'（躺' if GLOBAL.flash == 0 else ''}"
    )
    key = ("", "Ent 记录", "Esc 算了")
    keys = pg.key.get_pressed()
    for i in range(len(keys)):
        if keys[i]:
            shortly = True

    full_menu(screen, title, text, key, name, shortly=shortly)


def check_menu(screen: pg.Surface):
    def load_json(filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    try:
        log = load_json(GLOBAL.json_files[GLOBAL.index])[1]
        title = "抚形日志"
        text = (
            f"今天是 {log['Date']}",
            f"得到了 {log['Score']} 分",
            f"最远到达的地方是 {log['Stage']} 站",
            f"拾形点率为 {log['Rate']}",
            f"使用了 {log['Flashed']} 次形闪{'（躺' if log['Flash'] == 0 else ''}"
        )
        key = ("<-> 翻页", "Del 丢掉", "Esc 合上")

        full_menu(screen, title, text, key, f"谢谢 {log['Name']} 的帮助")
    except:
        GLOBAL.is_check = False


def full_menu(surface: pg.Surface, title: str, text: list, key: list, other: str, interval: tuple=(0, 30, 60), shortly: bool=False):
    func = lambda i, j: {"surface": font.render(i, False, (255, 255, 255)), "pos": j}
    group = (
        (
            func(title, (8, 9)),
            func(other, (8, 304))
        ),
        (
            *[func(text[i], (8, 59 + (25 * i))) for i in range(0, 5)],
        ),
        (
            *[func(key[i], (276, 169 + (50 * i))) for i in range(0, 3)],
        )
    )

    if GLOBAL.pop_timer == interval[0]:
        picture[5].fill(color_dict[8])
    if GLOBAL.pop_timer == interval[2]:
        sound_cache["pick"].play()
    surface.blit(Change.layers(picture[5], group, GLOBAL.pop_timer, interval, shortly), (120, 15))

    if GLOBAL.pop_timer < interval[2] + 1:
        GLOBAL.pop_timer += 1


def half_menu(surface: pg.Surface, title: str, text: list, interval: tuple=(0, 30, 60), shortly: bool=False):
    func = lambda i, j: ({"surface": font.render(i, False, (255, 255, 255)), "pos": j},)
    group = (
        func(title, (8, 9)),
        func(text[0], (8, 59)),
        func(text[1], (8, 84))
    )

    if GLOBAL.pop_timer == interval[0]:
        picture[5].fill(color_dict[8])
    if GLOBAL.pop_timer == interval[2]:
        sound_cache["pick"].play()
    surface.blit(Change.layers(picture[5].subsurface((0, 0, 345, 110)), group, GLOBAL.pop_timer, interval, shortly), (120, 15))

    if GLOBAL.pop_timer < interval[2] + 1:
        GLOBAL.pop_timer += 1


def ui(surface: pg.Surface, text: list, fps: str):
    for text_info in (
        {"text": text[0], "pos": (38, 25)},
        {"text": text[1], "pos": (38, 270)},
        {"text": text[2], "pos": (38, 295)},
        {"text": text[3], "pos": (38, 320)},
        {"text": fps, "pos": (405, 343)}
    ):
        surface.blit(font.render(f"{text_info['text']}", False, color_dict[6]), text_info["pos"])


def save_file():
    name = GLOBAL.name.translate(str.maketrans('!<>:"/\\|?*', '__________'))
    time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    content = {
        'Name': GLOBAL.name,
        'Score': GLOBAL.score,
        'Stage': f"{GLOBAL.stage if GLOBAL.stage < 3 else 'Final' if GLOBAL.stage == 3 else 'Extra'} - {GLOBAL.level}",
        'Rate': GLOBAL.calculate_item_rate(GLOBAL.game_total_point, GLOBAL.stage <= 3, (153, 61)),
        'Flashed': GLOBAL.flashed,
        'Date': time[0],
        'Flash': GLOBAL.flash
    }

    record(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{time[0]}_{time[1]}.json', ("DX00", content))


def summary_logic():
    def level_logic():
        mode_one()

        GLOBAL.stage, GLOBAL.level = follow((GLOBAL.stage, GLOBAL.level), 6)
        GLOBAL.unflash += 1

    GLOBAL.score += GLOBAL.score_summary(GLOBAL.total_point, GLOBAL.power, GLOBAL.unflash, GLOBAL.combo, (GLOBAL.stage, GLOBAL.level))
    GLOBAL.is_summary = False
    GLOBAL.is_save = True if GLOBAL.stage >= 3 and GLOBAL.level == 6 else level_logic()
    GLOBAL.pop_timer = 0


def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYUP:
            if not GLOBAL.is_summary and GLOBAL.is_level_load and event.key in keyup_game_dict:
                keyup_game_dict[event.key]()
        elif event.type == pg.KEYDOWN:
            if GLOBAL.is_check and event.key in keydown_check_dict:
                (keydown_check_dict[event.key](), sound_cache["pick"].play())
            elif not GLOBAL.is_run and not GLOBAL.is_check and event.key in keydown_start_dict:
                (sound_cache["pick"].play(), keydown_start_dict[event.key]())
            elif GLOBAL.is_save:
                if event.key in keydown_over_dict:
                    keydown_over_dict[event.key]()
                else:
                    GLOBAL.name = (GLOBAL.name + event.unicode)[:8]

                sound_cache["pick"].play()
            elif GLOBAL.is_pause and event.key in keydown_pause_dict:
                (keydown_pause_dict[event.key](), sound_cache["pick"].play())
            elif GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_talk_dict:
                (keydown_talk_dict[event.key](), sound_cache["pick"].play())
            elif GLOBAL.is_summary:
                (summary_logic(), sound_cache["pick"].play()) if event.key == pg.K_z else None
            elif not GLOBAL.is_summary and GLOBAL.is_level_load and not GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_game_dict:
                keydown_game_dict[event.key]()


def mode_one():
    GLOBAL.item_group.empty()
    GLOBAL.brick_group.empty()
    GLOBAL.plane_group.empty()
    GLOBAL.bullet_group.empty()
    GLOBAL.particle_group.empty()
    GLOBAL.barrage_group.empty()

    GLOBAL.is_pause = False
    GLOBAL.is_summary = False
    GLOBAL.is_talk = False
    GLOBAL.is_save = False
    GLOBAL.is_level_load = False
    GLOBAL.major = Kli(GLOBAL.bullet_group, GLOBAL.particle_group, GLOBAL.plane_group)
    GLOBAL.total_point = 0
    GLOBAL.item_spawn_timer = 0
    GLOBAL.combo = 0
    GLOBAL.combo_timer = 120
    GLOBAL.text_part = 0
    GLOBAL.text_number = 0
    GLOBAL.pop_timer = 0


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
    GLOBAL.json_files = get(f'{os.environ["USERPROFILE"]}/Saved Games/DX00')
    GLOBAL.index = 0
    GLOBAL.total_files = len(GLOBAL.json_files)


def spawn_barrage(stage: int, group: pg.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, locate: tuple):
    if random() <= fib[stage - 1]:
        {
            1: lambda: Sprite.circle_barrage(type, color, spawn_pos, locate, group),
            2: lambda: Sprite.polygon_barrage(type, color, spawn_pos, locate, group),
            3: lambda: Sprite.line_barrage(color, (randint(120, 465), 15), (locate[0] + randint(-32, 32), 345), group),
            4: lambda: Sprite.point_barrage(type, color, locate, group)
        }[stage]()


def brick_blast(group: pg.sprite.Group, stage: int, color: list, *spawn_pos: tuple):
    if color[0] == color_dict[6]:
        {
            1: lambda: Sprite.circle_brick(group, spawn_pos[3], randint(0, 45)),
            2: lambda: Sprite.polygon_brick(group, spawn_pos[0], spawn_pos[1], spawn_pos[2]),
            3: lambda: Sprite.line_brick(group, spawn_pos[3]),
            4: lambda: Sprite.point_brick(group)
        }[stage]()


def item_collide():
    for item in pg.sprite.spritecollide(GLOBAL.major, GLOBAL.item_group, False):
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

                Sprite.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, "Extend", color_dict[6], color_dict[2], GLOBAL.particle_group)

            GLOBAL.total_point += 1
            GLOBAL.game_total_point += 1
        else:
            sound_cache["charge"].play(maxtime=24)

        item.kill()


def barrage_collide(position):
    for barrage in pygame.sprite.spritecollide(GLOBAL.major.point, GLOBAL.barrage_group, False, collide):
        if barrage.color != color_dict[6]:
            if not GLOBAL.major.collided.condition and not GLOBAL.major.divided.condition:
                GLOBAL.major.collided.condition = True
                GLOBAL.unflash = 0
                GLOBAL.flash -= 1
                GLOBAL.flashed += 1
                if GLOBAL.flash == 0:
                    GLOBAL.is_save = True

                Sprite.spawn_particles(GLOBAL.particle_group, 9, position, (10, 16), color_dict[5], color_dict[6])
                sound_cache["fire"].play()

            barrage.kill()


def bullet_collide():
    for bullet, hit_bricks in pg.sprite.groupcollide(GLOBAL.bullet_group, GLOBAL.brick_group, False, False, collide).items():
        for brick in hit_bricks:
            if brick.hp > 0:
                GLOBAL.score += 64
                brick.hp -= bullet.damage
            else:
                if not brick.is_die:
                    if hasattr(brick, "free"):
                        GLOBAL.text_part += 1
                        GLOBAL.text_number = 0
                        GLOBAL.is_talk = True
                        GLOBAL.pop_timer = 0
                    else:
                        spawn_barrage(GLOBAL.stage, GLOBAL.barrage_group, difficulty, brick.type, [brick.color, color_dict[6], color_dict[3]], brick.rect.center, GLOBAL.major.rect.center)

                    if sound_cache["fire"].get_num_channels() < 2:
                        sound_cache["fire"].play()
                    if hasattr(brick, "power"):
                        spawn(brick.power, Sprite.Item, "power", 2.5, brick.rect.center, GLOBAL.item_group)
                    if hasattr(brick, "flash"):
                        spawn(brick.flash, Sprite.Item, "flash", 2.5, brick.rect.center, GLOBAL.item_group)
                    brick_blast(GLOBAL.bullet_group, GLOBAL.stage, [brick.color, color_dict[5], color_dict[3]], brick.rect.midleft, brick.rect.midright, brick.rect.midbottom, brick.rect.center)
                    Sprite.spawn_particles(GLOBAL.particle_group, 2, brick.rect.center, (4, 8), brick.color, color_dict[6])
                    brick.kill()

                brick.is_die = True

            if bullet.type in ("bullet", "bomb"):
                bullet.kill()


def sprite_loader():
    if GLOBAL.level == 6:
        GLOBAL.char = choose_human()
        GLOBAL.text = json.loads(asset(rf"ASSET\JSON\{GLOBAL.stage}.json").decode('utf-8'))
        GLOBAL.is_talk = True
    else:
        load(asset(rf"ASSET\STAGE\{GLOBAL.stage}-{GLOBAL.level}.stg"), Sprite.load_brick, color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)
        Sprite.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)

    GLOBAL.wait_load_timer = 0
    GLOBAL.pop_timer = 0


def spawn(condition: bool, sprite: object, *args, group: pg.sprite.Group = None, timer: int = 0) -> int:
    timer += 1

    if condition:
        char = sprite(*args)

        if group is not None:
            group.add(char)

        timer = 0

    return timer


def choose_human():
    return {
        1: Ono,
        2: Hro,
        3: Nre,
        4: Qdi
    }[GLOBAL.stage](GLOBAL.major.rect.center, GLOBAL.barrage_group, GLOBAL.particle_group, GLOBAL.brick_group)


def display(screen: pg.Surface, clock: pg.time.Clock):
    if GLOBAL.is_run:
        screen.blit(picture[GLOBAL.stage], (120, 15))
        if GLOBAL.is_level_load:
            GLOBAL.bullet_group.draw(screen)
            if GLOBAL.major is not None and GLOBAL.major.collided.visitable and GLOBAL.major.divided.visitable:
                GLOBAL.plane_group.draw(screen)
            GLOBAL.brick_group.draw(screen)
            GLOBAL.item_group.draw(screen)
            GLOBAL.particle_group.draw(screen)
            GLOBAL.barrage_group.draw(screen)

    for condition, func in (
        (lambda: GLOBAL.is_check, check_menu),
        (lambda: not GLOBAL.is_run, start_menu),
        (lambda: GLOBAL.is_pause, pause_menu),
        (lambda: not GLOBAL.is_level_load, load_menu),
        (lambda: GLOBAL.is_talk, talk_menu),
        (lambda: GLOBAL.is_summary, summary_menu),
        (lambda: GLOBAL.is_save, save_menu)
    ):
        if condition() and not GLOBAL.is_exit:
            func(screen)

            break

    screen.blit(picture[6])
    situation(screen, clock)


def update(clock: pg.time.Clock, screen: pg.Surface, args: tuple):
    GLOBAL.stage = clamp(args[0], 1, 4)
    GLOBAL.level = clamp(args[1], 1, 6)
    GLOBAL.flash = clamp(args[2], 1, 96)
    GLOBAL.power = clamp(args[3], 0, 32)
    alpha = 255
    timer = 0

    for text_info in (
        {"text": "分", "pos": (8, 25)},
        {"text": '形', "pos": (8, 270)},
        {"text": '闪', "pos": (8, 295)},
        {"text": '连', "pos": (8, 320)},
    ):
        picture[6].blit(font.render(f"{text_info['text']}", False, color_dict[6]), text_info["pos"])
    picture[6].set_clip(window)
    picture[6].fill((0, 0, 0, 0))

    while True:
        key_event()

        if GLOBAL.is_run and not GLOBAL.is_save and not GLOBAL.is_pause:
            if not GLOBAL.is_summary and not GLOBAL.is_talk and GLOBAL.is_level_load:
                if hasattr(GLOBAL.char, "locate"):
                    GLOBAL.char.locate = GLOBAL.major.rect.center
                GLOBAL.major.power = GLOBAL.power
                GLOBAL.item_spawn_timer = spawn(GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0, Sprite.Item, "fire", -2, (randint(120, 465), 10), GLOBAL.item_group, timer=GLOBAL.item_spawn_timer)
                if GLOBAL.combo_timer <= 1 and GLOBAL.combo > 0:
                    Sprite.Text(GLOBAL.major.rect.midtop, (45, 60), 0.5, f"{2 ** GLOBAL.combo}", color_dict[6], color_dict[7], GLOBAL.particle_group)
                GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score = GLOBAL.combo_counter(GLOBAL.combo_timer, GLOBAL.combo, GLOBAL.score, 2 ** GLOBAL.combo, 120)

                GLOBAL.plane_group.update()
                GLOBAL.bullet_group.update()
                GLOBAL.barrage_group.update()
                GLOBAL.item_group.update()
                GLOBAL.particle_group.update()
                GLOBAL.brick_group.update()
                barrage_collide(GLOBAL.major.rect.center)
                bullet_collide()
                item_collide()

                if len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
                    GLOBAL.is_summary = True
            if not GLOBAL.is_level_load:
                GLOBAL.wait_load_timer, GLOBAL.is_level_load = GLOBAL.wait(GLOBAL.wait_load_timer, GLOBAL.is_level_load, 90, sprite_loader)

        display(screen, clock)

        if GLOBAL.is_exit:
            if timer % 30 == 0 and alpha < 255:
                alpha += 85
            timer -= 1

            picture[7].set_alpha(alpha)
            screen.blit(picture[7])
            if timer <= -30:
                sys.exit()
        elif alpha > 0 and not GLOBAL.is_exit:
            if timer % 30 == 0 and alpha > 0:
                alpha -= 85
            timer += 1

            picture[7].set_alpha(alpha)
            screen.blit(picture[7])

        pg.display.flip()
        clock.tick(60)