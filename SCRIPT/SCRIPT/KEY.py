# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import sys

import pygame

from SCRIPT import LOGIC, TOOL
from SCRIPT.SCRIPT import GLOBAL, RESET


keydown_game_dict = {
    pygame.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", True),
    pygame.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", True),
    pygame.K_x: lambda: setattr(GLOBAL, "is_fast", True),
    pygame.K_z: lambda: setattr(GLOBAL, "is_shoot", False),
    pygame.K_SPACE: lambda: single_bomb(),
    pygame.K_ESCAPE: lambda: (
        setattr(GLOBAL, "is_pause", True),
        setattr(GLOBAL, "is_blit", False)
    )
}

keydown_talk_dict = {
    pygame.K_z: lambda: (
        setattr(GLOBAL, "text_number", GLOBAL.text_number + 1),
        setattr(GLOBAL, "is_blit", False)
    ),
    pygame.K_x: lambda: setattr(GLOBAL, "is_talk", False)
}

keydown_pause_dict = {
    pygame.K_ESCAPE: lambda: (
        setattr(GLOBAL, "is_pause", False),
        setattr(GLOBAL, 'is_blit', False)    
    ),
    pygame.K_q: lambda: (
        RESET.mode_one(),
        RESET.mode_two(),
        setattr(GLOBAL, "is_blit", False)
    )
}

keydown_start_dict = {
    pygame.K_z: lambda: (
        setattr(GLOBAL, "is_run", True),
        setattr(GLOBAL, "is_blit", False),
        next_level(),
        level_logic()
    ),
    pygame.K_q: lambda: sys.exit()
}

keydown_over_dict = {
    pygame.K_RETURN: lambda: (
        save_file(),
        RESET.mode_one(),
        RESET.mode_two(),
        setattr(GLOBAL, "is_blit", False)
    ),
    pygame.K_ESCAPE: lambda: (
        RESET.mode_one(),
        RESET.mode_two(),
        setattr(GLOBAL, "is_blit", False)
    ),
    pygame.K_BACKSPACE: lambda: (
        setattr(GLOBAL, "name", GLOBAL.name[:-1]),
        setattr(GLOBAL, "is_blit", False)
    )
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
    name = TOOL.replace_illegal_char(GLOBAL.name)

    LOGIC.File.dump_file(
        LOGIC.File.create_file(name, "DX00", TOOL.get_datetime()),
        GLOBAL.name,
        (GLOBAL.stage, GLOBAL.level),
        GLOBAL.score,
        LOGIC.Item.calculate_item_rate(GLOBAL.stage_total_power, GLOBAL.stage <= 3, (153, 61)),
        GLOBAL.use_flash
    )


def single_bomb() -> None:
    GLOBAL.is_s_divide, GLOBAL.power = LOGIC.Bullet.single_bomb(GLOBAL.is_s_divide, GLOBAL.power, 12)


def level_logic() -> None:
    GLOBAL.stage, GLOBAL.level = LOGIC.Stage.level_logic((GLOBAL.stage, GLOBAL.level), 6)


def next_level() -> None:
    RESET.mode_one()

    GLOBAL.no_flash += 1
    GLOBAL.plane_group.add(GLOBAL.main_char)
    GLOBAL.plane_group.add(GLOBAL.decision_point)
    GLOBAL.main_char.rect.center = (292, 332)
    GLOBAL.decision_point.rect.center = (292, 332)


def close_summary():
    def next_logic1():
        GLOBAL.is_save = True
        GLOBAL.is_blit = False

    def next_logic2():
        next_level()
        level_logic()

    GLOBAL.is_summary, GLOBAL.score = LOGIC.Stage.close_summary(
        GLOBAL.is_summary,
        (GLOBAL.stage, GLOBAL.level),
        GLOBAL.score,
        LOGIC.Stage.score_summary(GLOBAL.total_power, GLOBAL.no_flash, GLOBAL.combo, (512, 4096, 2, 2)),
        (3, 6),
        next_logic1,
        next_logic2
    )
    GLOBAL.second_background = LOGIC.Stage.change_background(GLOBAL.picture[GLOBAL.stage], 128)


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
            GLOBAL.name += event.unicode
            GLOBAL.is_blit = False
    elif GLOBAL.is_pause and event.key in keydown_pause_dict:
        keydown_pause_dict[event.key]()
    elif GLOBAL.is_talk and not GLOBAL.is_pause and event.key in keydown_talk_dict:
        keydown_talk_dict[event.key]()
    elif GLOBAL.is_summary and event.key in keydown_summary_dict:
        keydown_summary_dict[event.key]()
    elif not GLOBAL.is_summary and GLOBAL.is_level_load and event.key in keydown_game_dict:
        keydown_game_dict[event.key]()