# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys
import os
from datetime import datetime


import pygame as pg


from PRELOAD import picture, color_dict
from LOGIC.FILE import dump_file, return_file_with_makedir
from LOGIC.PLANE import single_bomb
from LOGIC.STAGE import level_logic, close_summary
from LOGIC.DRAW import rectangle
from SCRIPT.SPRITE import Barrage
from SCRIPT.HUMAN import Kli
from SCRIPT import GLOBAL


keydown_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", True),
    pg.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", True),
    pg.K_x: lambda: setattr(GLOBAL, "is_fast", True),
    pg.K_z: lambda: setattr(GLOBAL, "is_shoot", False),
    pg.K_SPACE: lambda: (lambda ret: (setattr(GLOBAL, 'is_divide', ret[0]), setattr(GLOBAL, 'power', ret[1])))(single_bomb(GLOBAL.is_divide, GLOBAL.power, 12)),
    pg.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", True), setattr(GLOBAL, "pop_time", 0))
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
    pg.K_q: lambda: sys.exit()
}


keydown_over_dict = {
    pg.K_RETURN: lambda: (save_file(), mode_one(), mode_two()),
    pg.K_ESCAPE: lambda: (mode_one(), mode_two()),
    pg.K_BACKSPACE: lambda: (setattr(GLOBAL, "name", GLOBAL.name[:-1]))
}


keydown_summary_dict = {
    pg.K_z: lambda: summary()
}


keyup_game_dict = {
    pg.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", False),
    pg.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", False),
    pg.K_x: lambda: setattr(GLOBAL, "is_fast", False),
    pg.K_z: lambda: setattr(GLOBAL, "is_shoot", True)
}


def save_file() -> None:
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

    dump_file(return_file_with_makedir(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{date_time[0]}_{date_time[1]}.json'), "锐山抚形日志", dump_content)


def next_level() -> None:
    def stage_logic() -> None:
        GLOBAL.stage, GLOBAL.level = level_logic((GLOBAL.stage, GLOBAL.level), 6)

    mode_one()
    stage_logic()

    GLOBAL.no_flash += 1


def summary():
    def next_logic():
        GLOBAL.is_save = True

    GLOBAL.is_summary, GLOBAL.score = close_summary(((GLOBAL.stage, GLOBAL.level), (3, 6)), GLOBAL.score, GLOBAL.score_summary(GLOBAL.total_power, GLOBAL.no_flash, GLOBAL.combo, (512, 4096, 2)), next_logic, next_level)
    GLOBAL.pop_time = 0
    GLOBAL.second_backdrop = picture[GLOBAL.stage]


def key_event() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYUP:
            keyup(event)
        elif event.type == pg.KEYDOWN:
            keydown(event)


def keyup(event: pg.event.Event) -> None:
    if GLOBAL.is_run and event.key in keyup_game_dict:
        keyup_game_dict[event.key]()


def keydown(event: pg.event.Event) -> None:
    if not GLOBAL.is_run and event.key in keydown_start_dict:
        keydown_start_dict[event.key]()
    elif GLOBAL.is_save:
        if event.key in keydown_over_dict:
            keydown_over_dict[event.key]()
        else:
            GLOBAL.name = (GLOBAL.name + event.unicode)[:8]
    elif GLOBAL.is_pause and event.key in keydown_pause_dict:
        keydown_pause_dict[event.key]()
    elif GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_talk_dict:
        keydown_talk_dict[event.key]()
    elif GLOBAL.is_summary and event.key in keydown_summary_dict:
        keydown_summary_dict[event.key]()
    elif not GLOBAL.is_summary and GLOBAL.is_level_load and not GLOBAL.is_talk and event.key in keydown_game_dict:
        keydown_game_dict[event.key]()


def mode_one() -> None:
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
    GLOBAL.decision_point = Barrage.Rect(rectangle((2, 2), 0, color_dict[7]).convert(), GLOBAL.plane_group, pos=(292, 332), mask=True)
    GLOBAL.total_power = 0

    GLOBAL.shoot_count = 0
    GLOBAL.is_shoot = True

    GLOBAL.item_spawn_time = 0
    GLOBAL.combo = 0
    GLOBAL.combo_time = 120

    GLOBAL.text_part = 0
    GLOBAL.text_number = 0


def mode_two() -> None:
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