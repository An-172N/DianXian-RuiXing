# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import sys
import os


import pygame


import PRELOAD
from LOGIC import Tool, File, Stage, Plane, Item
from SCRIPT import GLOBAL, RESET


keydown_game_dict = {
    pygame.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", True),
    pygame.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", True),
    pygame.K_x: lambda: setattr(GLOBAL, "is_fast", True),
    pygame.K_z: lambda: setattr(GLOBAL, "is_shoot", False),
    pygame.K_SPACE: lambda: single_bomb(),
    pygame.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", True), setattr(GLOBAL, "animate_timer", 0))
}


keydown_talk_dict = {
    pygame.K_z: lambda: (setattr(GLOBAL, "text_number", GLOBAL.text_number + 1), setattr(GLOBAL, "animate_timer", 0)),
    pygame.K_x: lambda: setattr(GLOBAL, "is_talk", False)
}


keydown_pause_dict = {
    pygame.K_ESCAPE: lambda: (setattr(GLOBAL, "is_pause", False), setattr(GLOBAL, "animate_timer", 0)),
    pygame.K_q: lambda: (RESET.mode_one(), RESET.mode_two())
}


keydown_start_dict = {
    pygame.K_z: lambda: (setattr(GLOBAL, "is_run", True), setattr(GLOBAL, "animate_timer", 0), next_level(), level_logic()),
    pygame.K_q: lambda: sys.exit()
}


keydown_over_dict = {
    pygame.K_RETURN: lambda: (save_file(), RESET.mode_one(), RESET.mode_two()),
    pygame.K_ESCAPE: lambda: (RESET.mode_one(), RESET.mode_two()),
    pygame.K_BACKSPACE: lambda: (setattr(GLOBAL, "name", GLOBAL.name[:-1]))
}


keydown_summary_dict = {
    pygame.K_z: lambda: close_summary()
}


keyup_game_dict = {
    pygame.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", False),
    pygame.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", False),
    pygame.K_x: lambda: setattr(GLOBAL, "is_fast", False),
    pygame.K_z: lambda: setattr(GLOBAL, "is_shoot", True)
}


def save_file() -> None:
    name = Tool.replace_illegal_char(GLOBAL.name)
    date_time = Tool.get_datetime()
    dump_content = {
        '助记者': GLOBAL.name,
        '分数': GLOBAL.score,
        '最远到达的地方': f"{GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level}",
        '拾形点率': Item.calculate_item_rate(GLOBAL.stage_total_power, GLOBAL.stage <= 3, (153, 61)),
        '形闪次数': GLOBAL.use_flash,
        '记录日期': date_time[0]
    }

    File.dump_file(File.return_file_with_makedir(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{date_time[0]}_{date_time[1]}.json'), "锐山抚形日志", dump_content)


def single_bomb() -> None:
    GLOBAL.is_s_divide, GLOBAL.power = Plane.single_bomb(GLOBAL.is_s_divide, GLOBAL.power, 12)


def level_logic() -> None:
    GLOBAL.stage, GLOBAL.level = Stage.level_logic((GLOBAL.stage, GLOBAL.level), 6)


def next_level() -> None:
    RESET.mode_one()

    GLOBAL.no_flash += 1
    GLOBAL.plane_group.add(GLOBAL.main_char)
    GLOBAL.plane_group.add(GLOBAL.decision_point)


def close_summary():
    def next_logic1():
        GLOBAL.is_save = True

    def next_logic2():
        next_level()
        level_logic()

    GLOBAL.is_summary, GLOBAL.score = Stage.close_summary(GLOBAL.is_summary, ((GLOBAL.stage, GLOBAL.level), (3, 6)), GLOBAL.score, Stage.score_summary(GLOBAL.total_power, GLOBAL.no_flash, GLOBAL.combo, (512, 4096, 2, 2)), next_logic1, next_logic2)
    GLOBAL.second_background = PRELOAD.picture[GLOBAL.stage]


def key_event() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            keyup(event)
        elif event.type == pygame.KEYDOWN:
            keydown(event)


def keyup(event: pygame.event.Event) -> None:
    if GLOBAL.is_run and event.key in keyup_game_dict:
        keyup_game_dict[event.key]()


def keydown(event: pygame.event.Event) -> None:
    if not GLOBAL.is_run and event.key in keydown_start_dict:
        keydown_start_dict[event.key]()
    elif GLOBAL.is_save:
        if event.key in keydown_over_dict:
            keydown_over_dict[event.key]()
        else:
            GLOBAL.name = Tool.truncate(GLOBAL.name + event.unicode, 8)
    elif GLOBAL.is_pause and event.key in keydown_pause_dict:
        keydown_pause_dict[event.key]()
    elif GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_talk_dict:
        keydown_talk_dict[event.key]()
    elif GLOBAL.is_summary and event.key in keydown_summary_dict:
        keydown_summary_dict[event.key]()
    elif not GLOBAL.is_summary and GLOBAL.is_level_load and not GLOBAL.is_talk and event.key in keydown_game_dict:
        keydown_game_dict[event.key]()