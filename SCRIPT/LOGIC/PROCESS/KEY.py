# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import os
import sys
import json
import datetime

import pygame

import SCRIPT.GLOBAL as GLOBAL


def save_file() -> None:
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H-%M-%S')

    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{GLOBAL.name}_{date}_{time}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    dump = ["RuiShan FuXing Log"]
    stage = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'
    dump.append(
        {
            'Nickname': GLOBAL.name,
            'Score': GLOBAL.score,
            'The farthest place that you reached': f"{stage} - {GLOBAL.level}",
            'Pick up SPower rate': GLOBAL.cal_s_power(),
            'Shape Flash': GLOBAL.s_flash,
            'Record date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
    )
        
    with open(file, 'w') as f:
        json.dump(dump, f, indent=4)


def key_event() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            keyup(event)
        elif event.type == pygame.KEYDOWN:
            keydown(event)


def keyup(event) -> None:
    if GLOBAL.run and event.key in GLOBAL.keyup_game_dict:
        GLOBAL.keyup_game_dict[event.key]()


def keydown(event) -> None:
    if not GLOBAL.run and event.key in GLOBAL.keydown_start_dict:
        GLOBAL.keydown_start_dict[event.key]()
    elif GLOBAL.save:
        if event.key in GLOBAL.keydown_over_dict:
            GLOBAL.keydown_over_dict[event.key]()
        else:
            GLOBAL.name += event.unicode
            GLOBAL.is_blit = False
    elif GLOBAL.pause and event.key in GLOBAL.keydown_pause_dict:
        GLOBAL.keydown_pause_dict[event.key]()
    elif GLOBAL.talk and event.key in GLOBAL.keydown_talk_dict:
        GLOBAL.keydown_talk_dict[event.key]()
    elif not GLOBAL.summary and GLOBAL.level_load and event.key in GLOBAL.keydown_game_dict:
        GLOBAL.keydown_game_dict[event.key]()