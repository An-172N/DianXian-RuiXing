# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import os
import re
import sys
import json
import datetime

import pygame

from SCRIPT import GLOBAL, LOGIC


keydown_game_dict = {
    pygame.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", True),
    pygame.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", True),
    pygame.K_x: lambda: setattr(GLOBAL, "is_fast", True),
    pygame.K_z: lambda: setattr(GLOBAL, "is_shoot", False),
    pygame.K_SPACE: lambda: LOGIC.BulletMgr.single_bomb(),
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
        LOGIC.Reset.mode_one(),
        LOGIC.Reset.mode_two(),
        LOGIC.Reset.group_empty(),
        setattr(GLOBAL, "is_blit", False)
    )
}

keydown_start_dict = {
    pygame.K_z: lambda: (
        setattr(GLOBAL, "is_run", True),
        setattr(GLOBAL, "is_blit", False),
        LOGIC.StageMgr.next_level(),
        LOGIC.StageMgr.level_logic()
    ),
    pygame.K_q: lambda: sys.exit()
}

keydown_over_dict = {
    pygame.K_RETURN: lambda: (
        LOGIC.Key.save_file(),
        LOGIC.Reset.mode_one(),
        LOGIC.Reset.mode_two(),
        LOGIC.Reset.group_empty(),
        setattr(GLOBAL, "is_blit", False)
    ),
    pygame.K_ESCAPE: lambda: (
        LOGIC.Reset.mode_one(),
        LOGIC.Reset.mode_two(),
        LOGIC.Reset.group_empty(),
        setattr(GLOBAL, "is_blit", False)
    ),
    pygame.K_BACKSPACE: lambda: (
        setattr(GLOBAL, "name", GLOBAL.name[:-1]),
        setattr(GLOBAL, "is_blit", False)
    )
}

keydown_summary_dict = {
    pygame.K_z: lambda: LOGIC.StageMgr.summary_closer()
}


keyup_game_dict = {
    pygame.K_RIGHT: lambda: setattr(GLOBAL, "is_move_right", False),
    pygame.K_LEFT: lambda: setattr(GLOBAL, "is_move_left", False),
    pygame.K_x: lambda: setattr(GLOBAL, "is_fast", False),
    pygame.K_z: lambda: setattr(GLOBAL, "is_shoot", True)
}


def save_file() -> None:
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H-%M-%S')

    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{illegal_char(GLOBAL.name)}_{date}_{time}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    dump = ["RuiShan FuXing Log"]
    stage = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'
    dump.append(
        {
            'Help recorder': GLOBAL.name,
            'Score': GLOBAL.score,
            'The farthest station that you reached': f"{stage} - {GLOBAL.level}",
            'Pick up Shape Power rate': LOGIC.Reset.cal_s_power(),
            'Shape Flash': GLOBAL.use_flash,
            'Record date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
    )
        
    with open(file, 'w') as f:
        json.dump(dump, f, indent=4)


def illegal_char(name: str) -> str:
    char = r'[!<>:"/\\|?*]'

    return re.sub(char, '_', name)


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