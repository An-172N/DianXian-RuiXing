import os
import sys
import json
import datetime

import pygame

import SCRIPT.TABLE as TABLE
import SCRIPT.VARIABLE as VARIABLE


def save_file() -> None:
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H-%M-%S')

    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{VARIABLE.name}_{date}_{time}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    dump = ["RuiShan FuXing Log"]
    stage = VARIABLE.stage if VARIABLE.stage <= 3 else f'Extra'
    dump.append(
        {
            'Nickname': VARIABLE.name,
            'Score': VARIABLE.score,
            'The farthest place that you reached': f"{stage} - {VARIABLE.level}",
            'Pick up SPower rate': VARIABLE.cal_s_power(),
            'Shape Flash': VARIABLE.s_flash,
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
    if (
        VARIABLE.run
        and event.key in TABLE.keyup_game_dict
    ):
        TABLE.keyup_game_dict[event.key]()


def keydown(event) -> None:
    if (
        not VARIABLE.run
        and event.key in TABLE.keydown_start_dict
    ):
        TABLE.keydown_start_dict[event.key]()
    elif VARIABLE.save:
        if event.key in TABLE.keydown_over_dict:
            TABLE.keydown_over_dict[event.key]()
        else:
            VARIABLE.name += event.unicode
            VARIABLE.is_blit = False
    elif (
        VARIABLE.pause
        and event.key in TABLE.keydown_pause_dict
    ):
        TABLE.keydown_pause_dict[event.key]()
    elif (
        VARIABLE.talk
        and event.key in TABLE.keydown_talk_dict
    ):
        TABLE.keydown_talk_dict[event.key]()
    elif (
        not VARIABLE.summary
        and VARIABLE.level_load
        and event.key in TABLE.keydown_game_dict
    ):
        TABLE.keydown_game_dict[event.key]()