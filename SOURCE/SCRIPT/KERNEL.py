# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys
import os
from datetime import datetime
from random import randint


import pygame as pg


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.STAGE import *
from LOGIC.FILE import *
from LOGIC.SPRITE import *
from SCRIPT import GLOBAL
from SCRIPT.SPRITE import *
from SCRIPT.SOME import *
from SCRIPT.SPAWN import *


one = GLOBAL.One()
two = GLOBAL.Two()
log = GLOBAL.Log()
reset = lambda: (one.__init__(), two.__init__(), log.__init__())


keydown_game_dict = {
    pg.K_RIGHT: lambda: setattr(one.major, "is_move_right", True),
    pg.K_LEFT: lambda: setattr(one.major, "is_move_left", True),
    pg.K_x: lambda: setattr(one.major, "is_fast", True),
    pg.K_z: lambda: setattr(one.major, "is_shoot", False),
    pg.K_SPACE: lambda: (lambda i: (setattr(one.major.divided, 'condition', i[0]), setattr(two, 'power', i[1])))(bomb(one.major.divided.condition, two.power, 12)),
    pg.K_ESCAPE: lambda: (setattr(one, "is_pause", True), setattr(one, "pop_timer", 0), sound_cache["pick"].play())
}


keydown_talk_dict = {
    pg.K_z: lambda: (setattr(one, "text_number", one.text_number + 1), setattr(one, "pop_timer", 0)),
    pg.K_x: lambda: (setattr(one, "is_talk", False), setattr(one, "pop_timer", 0))
}


keydown_pause_dict = {
    pg.K_ESCAPE: lambda: (setattr(one, "is_pause", False), setattr(one, "pop_timer", 0)),
    pg.K_DELETE: lambda: reset()
}


keydown_start_dict = {
    pg.K_z: lambda: (setattr(two, "is_run", True), setattr(one, "pop_timer", 0), one.__init__()),
    pg.K_q: lambda: setattr(one, "is_exit", True),
    pg.K_c: lambda: (setattr(one, "is_check", True), setattr(one, "pop_timer", 0)) if log.total_files > 0 else None
}


keydown_over_dict = {
    pg.K_RETURN: lambda: (save_file(log.name, two.score, two.total_point, two.flashed, two.flash, (two.stage, two.level)), reset()),
    pg.K_ESCAPE: lambda: reset(),
    pg.K_BACKSPACE: lambda: setattr(log, "name", log.name[:-1])
}


keydown_check_dict = {
    pg.K_DELETE: lambda: (os.remove(log.json_files[log.index]), log.__init__(), setattr(one, "pop_timer", 0)),
    pg.K_ESCAPE: lambda: (setattr(one, "is_check", False), setattr(log, "index", 0), setattr(one, "pop_timer", 0)),
    pg.K_LEFT: lambda: (setattr(log, "index", (log.index - 1) if log.index > 0 else log.total_files - 1), setattr(one, "pop_timer", 0)),
    pg.K_RIGHT: lambda: (setattr(log, "index", (log.index + 1) if log.index < log.total_files - 1 else 0), setattr(one, "pop_timer", 0))
}


keyup_game_dict = {
    pg.K_RIGHT: lambda: setattr(one.major, "is_move_right", False),
    pg.K_LEFT: lambda: setattr(one.major, "is_move_left", False),
    pg.K_x: lambda: setattr(one.major, "is_fast", False),
    pg.K_z: lambda: setattr(one.major, "is_shoot", True)
}


def situation(screen: pg.Surface, clock: pg.time.Clock):
    text = (
        f"{two.score:9d}",
        f"{int(clock.get_fps()): 9d}",
        f"{two.power:02d}  ,  {one.total_point:02d}",
        f"{two.flash:02d}",
        f"{one.combo:02d}  ,  {one.major.bullets:02d}"
    )
    for info in (
        {"text": text[0], "pos": (39, 25)},
        {"text": text[1], "pos": (39, 50)},
        {"text": text[2], "pos": (39, 270)},
        {"text": text[3], "pos": (39, 295)},
        {"text": text[4], "pos": (39, 320)},
    ):
        screen.blit(font.render(f"{info['text']}", False, color_dict[6]), info["pos"])


def pause_menu(screen: pg.Surface):
    shortly = False
    title = "休息ing"
    text = ("Esc 休息好了", "Del 不爬了") if one.pop_timer >= 60 else ("", "")
    if one.pop_timer == 60:
        shortly = True
    half_menu(screen, title, text, shortly=shortly)


def load_menu(screen: pg.Surface):
    title = "这一站是————"
    text = (f"Stage {get_stage(two.stage)} - {two.level} !!", "START!!!!")
    half_menu(screen, title, text)


def talk_menu(screen: pg.Surface):
    try:
        text = one.text[f"{one.text_part}"][f"{one.text_number}"]
        human = text["char"]
        content = (text["1"], text["2"] if "2" in text else '')
        half_menu(screen, human, content, (0, 6, 12))
    except KeyError:
        one.is_talk = False


def summary_menu(screen: pg.Surface):
    shortly = False
    hit = 'Hit Z Key.' if two.level <= 5 and one.pop_timer >= 60 else ''
    stage = f"Stage {get_stage(two.stage)} - {two.level} Clear! {hit}"
    text = (
        f"得点 {one.total_point} * 512 = {one.total_point * 512}",
        f"无闪 {two.unflash} * 4096 = {two.unflash * 4096}",
        f"面数 {two.stage} * 16384 = {two.stage * 16384}",
        f"形力 {two.power} / 32 * 8192 = {int(two.power / 32 * 8192)}",
        ""
    )
    key = ("", "", "Z 继续")
    if one.pop_timer == 60:
        shortly = True
    if two.level <= 5:
        half_menu(screen, stage, (text[0], text[1]), shortly=shortly)
    else:
        full_menu(screen, stage, text, key, title.get(two.stage))


def start_menu(screen: pg.Surface, version: str, title: str):
    other = "(C)opyright 2026 An_172N"
    text = (f"Ver {version}", '', '', '', '')
    climb = "Z 爬山" if two.stage < 4 else "Z 下山"
    wood = "C 日志" if log.total_files > 0 else "C 木鱼"
    key = (climb, wood, "Q 拜拜")
    full_menu(screen, title, text, key, other)


def save_menu(screen: pg.Surface):
    shortly = False
    title = "爬山日志"
    name = f"{f'谢谢 {log.name} 的帮助' if one.pop_timer >= 60 else ''}"
    text = (
        f"今天是 {datetime.now().strftime('%Y-%m-%d')}",
        f"得到了 {two.score} 分",
        f"最终到达 {get_stage(two.stage)} - {two.level} 站",
        f"拾形点率为 {calculate_item_rate(two.total_point, two.stage <= 3, (153, 61))}",
        f"使用了 {two.flashed} 次形闪{'（躺' if two.flash == 0 else ''}"
    )
    key = ("", "Ent 记录", "Esc 算了")
    if one.pop_timer == 60:
        shortly = True
    if one.pop_timer >= 60:
        keys = pg.key.get_pressed()
        for i in range(len(keys)):
            if keys[i]:
                shortly = True
    full_menu(screen, title, text, key, name, shortly=shortly)


def check_menu(screen: pg.Surface):
    try:
        if one.pop_timer == 0:
            log.log = load_json(log.json_files[log.index])[1]
        logs = log.log
        title = f"爬山日志簿第 {log.total_files - log.index} / {log.total_files} 页"
        text = (
            f"今天是 {logs['Date']}",
            f"得到了 {logs['Score']} 分",
            f"最终到达 {logs['Stage']} 站",
            f"拾形点率为 {logs['Rate']}",
            f"使用了 {logs['Flashed']} 次形闪{'（躺' if logs['Flash'] == 0 else ''}"
        )
        key = ("<-> 翻页", "Del 丢掉", "Esc 合上")
        full_menu(screen, title, text, key, f"谢谢 {logs['Name']} 的帮助")
    except:
        one.is_check = False


def full_menu(surface: pg.Surface, title: str, text: list, key: list, other: str, interval: tuple=(0, 30, 60), shortly: bool=False):
    group = (
        (
            render(title, (8, 10)),
            render(other, (8, 305))
        ),
        (
            *[render(text[i], (8, 60 + (25 * i))) for i in range(0, 5)],
        ),
        (
            *[render(key[i], (275, 170 + (50 * i))) for i in range(0, 3)],
        )
    )
    if one.pop_timer == interval[0]:
        picture[5].fill(color_dict[8])
    surface.blit(Change.layers(picture[5], group, one.pop_timer, interval, shortly), (120, 15))
    if one.pop_timer == interval[2]:
        sound_cache["pick"].play()
    if one.pop_timer < interval[2] + 1:
        one.pop_timer += 1


def half_menu(surface: pg.Surface, title: str, text: list, interval: tuple=(0, 30, 60), shortly: bool=False):
    group = (
        (render(title, (8, 10)),),
        (render(text[0], (8, 60)),),
        (render(text[1], (8, 85)),)
    )

    if one.pop_timer == interval[0]:
        picture[5].fill(color_dict[8])
    source = Change.layers(picture[5].subsurface((0, 0, 345, 110)), group, one.pop_timer, interval, shortly)
    surface.blit(source, (120, 15))
    if one.pop_timer == interval[2]:
        sound_cache["pick"].play()
    if one.pop_timer < interval[2] + 1:
        one.pop_timer += 1


def summary_logic(score: int, total_point: int, power: int, unflash: int, combo: int, numbers: tuple):
    stage, level = numbers
    is_save = False
    score += GLOBAL.score_summary(total_point, power, unflash, combo, (stage, level))
    is_summary = False
    pop_timer = 0
    if stage >= 3 and level == 6:
        is_save = True
    else:
        stage, level, unflash = level_logic((stage, level), unflash)

    return score, is_summary, pop_timer, is_save, stage, level, unflash


def level_logic(numbers: tuple, unflash: int):
    stage, level = numbers
    one.__init__()
    stage, level = follow((stage, level), 6)
    unflash += 1

    return stage, level, unflash


def item_collide():
    major = one.major
    for item in pg.sprite.spritecollide(major, one.item_group, True):
        one.combo_timer = 120
        major.bullets = clamp(major.bullets + 1, 0, 3)
        if item.type in ('flash', 'power'):
            if item.type == "power":
                two.power = clamp(two.power + 1, 0, 32)
                one.combo += 1
                sound_cache["pick"].play()
            else:
                two.flash += 1
                one.combo += 1
                Text(major.rect.midtop, (45, 60), 0.5, "Extend", color_dict[6], color_dict[2], one.particle_group)
            one.total_point += 1
            two.total_point += 1
        else:
            sound_cache["charge"].play(maxtime=24)


def barrage_collide():
    major = one.major
    for barrage in pygame.sprite.spritecollide(major.point, one.barrage_group, False, collide):
        if barrage.color != color_dict[6]:
            if not major.collided.condition and not major.divided.condition:
                major.collided.condition = True
                two.unflash = 0
                two.flash -= 1
                two.flashed += 1
                if two.flash == 0:
                    one.is_save = True
                spawn_particles(one.particle_group, 9, major.rect.center, (10, 16), color_dict[5], color_dict[6])
                sound_cache["fire"].play()
            barrage.kill()


def bullet_collide():
    for bullet, hit_bricks in pg.sprite.groupcollide(one.bullet_group, one.brick_group, False, False, collide).items():
        for brick in hit_bricks:
            rect = brick.rect
            if brick.hp > 0:
                two.score += 64
                brick.hp -= bullet.damage
                if brick.hp > 0 and sound_cache["tick"].get_num_channels() < 2:
                    spawn_particles(one.particle_group, 2, rect.center, (4, 8), brick.color, color_dict[6])
                    sound_cache["tick"].play()
            if brick.hp <= 0:
                if not brick.is_die:
                    if hasattr(brick, "free"):
                        one.text_part += 1
                        one.text_number = 0
                        one.is_talk = True
                        one.pop_timer = 0
                        for _ in range(12):
                            spawn_particles(one.particle_group, 2, rect.center, (2, 8), brick.color, color_dict[6])
                    else:
                        colors = (brick.color, color_dict[6], color_dict[3])
                        poses = (rect.center, one.major.rect.center)
                        spawn_barrage(two.stage, one.barrage_group, two.power, brick.type, colors, *poses)
                        spawn_particles(one.particle_group, 2, rect.center, (4, 8), brick.color, color_dict[6])
                    if sound_cache["fire"].get_num_channels() < 2:
                        sound_cache["fire"].play()
                    if hasattr(brick, "power"):
                        spawn(brick.power, Item, "power", 2.5, rect.center, one.item_group)
                    if hasattr(brick, "flash"):
                        spawn(brick.flash, Item, "flash", 2.5, rect.center, one.item_group)
                    poses = (offset_y(rect.midleft, -1), offset_y(rect.midright, -1), offset_y(rect.midbottom, -1), rect.center)
                    brick_blast(one.bullet_group, two.stage, brick.color, *poses)
                    brick.kill()
                brick.is_die = True
            if bullet.type in ("bullet", "bomb"):
                bullet.kill()


def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYUP:
            if not one.is_summary and one.is_level_load and event.key in keyup_game_dict:
                keyup_game_dict[event.key]()
        elif event.type == pg.KEYDOWN:
            if one.pop_timer >= 60:
                if one.is_check and event.key in keydown_check_dict:
                    keydown_check_dict[event.key]()
                    sound_cache["pick"].play()
                elif not two.is_run and not one.is_check and not one.is_exit and event.key in keydown_start_dict:
                    sound_cache["pick"].play()
                    keydown_start_dict[event.key]()
                elif one.is_save:
                    if event.key in keydown_over_dict:
                        keydown_over_dict[event.key]()
                    else:
                        log.name = (log.name + event.unicode)[:8]
                    sound_cache["pick"].play()
                elif one.is_pause and event.key in keydown_pause_dict:
                    (keydown_pause_dict[event.key](), sound_cache["pick"].play())
                elif one.is_summary and event.key == pg.K_z:
                    two.score, one.is_summary, one.pop_timer, one.is_save, two.stage, two.level, two.unflash = summary_logic(two.score, one.total_point, two.power, two.unflash, one.combo, (two.stage, two.level))
                    sound_cache["pick"].play()
            elif one.is_talk and not one.is_pause and event.key in keydown_talk_dict and one.pop_timer >= 12:
                keydown_talk_dict[event.key]()
                sound_cache["pick"].play()
            elif not one.is_summary and one.is_level_load and not one.is_talk and not one.is_pause and event.key in keydown_game_dict:
                keydown_game_dict[event.key]()


def display(screen: pg.Surface, clock: pg.time.Clock, version: str, title: str):
    major = one.major
    if two.is_run:
        screen.blit(picture[two.stage], (120, 15))
        one.bullet_group.draw(screen)
        if major.collided.visitable and major.divided.visitable and one.is_level_load:
            one.plane_group.draw(screen)
        one.brick_group.draw(screen)
        one.item_group.draw(screen)
        one.particle_group.draw(screen)
        one.barrage_group.draw(screen)
    if not one.is_exit:
        if one.is_check:
            check_menu(screen)
        elif not two.is_run:
            start_menu(screen, version, title)
        else:
            for condition, func in (
                (one.is_pause, pause_menu),
                (not one.is_level_load, load_menu),
                (one.is_talk, talk_menu),
                (one.is_summary, summary_menu),
                (one.is_save, save_menu)
            ):
                if condition:
                    func(screen)
                    break
    screen.blit(picture[6])
    situation(screen, clock)


def update(clock: pg.time.Clock, screen: pg.Surface, args: tuple, version: str, title: str):
    two.stage = clamp(args[0], 1, 4)
    two.level = clamp(args[1], 1, 6)
    two.flash = clamp(args[2], 1, 96)
    two.power = clamp(args[3], 0, 32)
    alpha = 255
    timer = 0
    for text_info in (
        {"text": "分", "pos": (9, 25)},
        {"text": "刷", "pos": (9, 50)},
        {"text": '形', "pos": (9, 270)},
        {"text": '闪', "pos": (9, 295)},
        {"text": '连', "pos": (9, 320)},
    ):
        picture[6].blit(font.render(f"{text_info['text']}", False, color_dict[6]), text_info["pos"])
    picture[6].set_clip(window)
    picture[6].fill((0, 0, 0, 0))
    while True:
        key_event()
        if two.is_run and not one.is_save and not one.is_pause:
            if not one.is_summary and not one.is_talk and one.is_level_load:
                major = one.major
                if hasattr(one.char, "locate"):
                    one.char.locate = major.rect.center
                major.power = two.power
                one.item_spawn_timer = spawn(one.item_spawn_timer >= 45 and len(one.brick_group) > 0, Item, "fire", -2, (randint(120, 465), 10), one.item_group, timer=one.item_spawn_timer)
                if one.combo_timer <= 1 and one.combo > 0:
                    Text(major.rect.midtop, (45, 60), 0.5, f"{2 ** one.combo}", color_dict[6], color_dict[7], one.particle_group)
                one.combo_timer, one.combo, two.score = GLOBAL.combo_counter(one.combo_timer, one.combo, two.score, 2 ** one.combo, 120)
                one.plane_group.update()
                one.bullet_group.update()
                one.barrage_group.update()
                one.item_group.update()
                one.particle_group.update()
                one.brick_group.update()
                barrage_collide()
                bullet_collide()
                item_collide()
                if len(one.brick_group) == 0 and len(one.item_group) == 0 and not one.is_talk:
                    one.is_summary = True
            if not one.is_level_load:
                if two.wait_load_timer <= 90:
                    if two.wait_load_timer == 0:
                        one.char, one.text = sprite_loader((two.stage, two.level), one.barrage_group, one.particle_group, one.brick_group, one.bullet_group)
                    two.wait_load_timer = pop_bricks(two.remaining_brick, brick_ready, two.wait_load_timer, one.brick_group)
                else:
                    two.wait_load_timer, one.is_level_load, one.pop_timer, one.is_talk = close_summary(two.level, one.is_talk, two.remaining_brick, brick_ready)
        display(screen, clock, version, title)
        alpha, timer = fade_surface(alpha, timer, one.is_exit, picture[7], screen)
        pg.display.flip()
        clock.tick(60)