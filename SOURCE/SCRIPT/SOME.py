# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys
import os
import json
from datetime import datetime
from random import random, sample


import pygame as pg


from LOGIC.FILE import *
from LOGIC.STAGE import *
from SCRIPT.HUMAN import Ono, Hro, Nre, Qdi
from SCRIPT.SPAWN import *


def load_json(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def spawn_barrage(stage: int, group: pg.sprite.Group, fib: list, type: int, color: tuple, spawn_pos: tuple, locate: tuple):
    if random() <= fib[stage - 1]:
        {
            1: lambda: circle_barrage(type, color[0], spawn_pos, locate, group),
            2: lambda: polygon_barrage(type, color[0], spawn_pos, locate, group),
            3: lambda: line_barrage((randint(120, 465), 15), (locate[0] + randint(-32, 32), 345), group, color[1], color[2]),
            4: lambda: point_barrage(type, color[0], locate, group)
        }[stage]()


def brick_blast(group: pg.sprite.Group, stage: int, color: list, *spawn_pos: tuple):
    if color[0] == color_dict[6]:
        {
            1: lambda: circle_brick(group, spawn_pos[3], randint(0, 45)),
            2: lambda: polygon_brick(group, spawn_pos[0], spawn_pos[1], spawn_pos[2]),
            3: lambda: line_brick(group, spawn_pos[3]),
            4: lambda: point_brick(group)
        }[stage]()


def sprite_loader(numbers: tuple, *group: pg.sprite.Group):
    stage, level = numbers
    char = None
    text = None

    if level == 6:
        char = choose_human(stage, *group)
        text = json.loads(asset(rf"ASSET\JSON\{stage}.json").decode('utf-8'))
    else:
        load(asset(rf"ASSET\STAGE\{stage}-{level}.stg"), load_brick, color_dict[stage], 4, 0.031, (127, 22), (15, 15))
        choose_brick(brick_ready, (stage, level), 4, 1)

    return char, text


def spawn(condition: bool, sprite: object, *args, group: pg.sprite.Group = None, timer: int = 0) -> int:
    timer += 1

    if condition:
        char = sprite(*args)

        if group is not None:
            group.add(char)

        timer = 0

    return timer


def choose_human(stage: int, *group: pg.sprite.Group):
    return {
        1: Ono,
        2: Hro,
        3: Nre,
        4: Qdi
    }[stage](*group)


def pop_bricks(remaining_brick: list, brick_ready: list, wait_load_timer: int, brick_group: pg.sprite.Group):
    if wait_load_timer >= 30 and wait_load_timer % 30 == 0:
        if not remaining_brick:
            remaining_brick = list(range(len(brick_ready)))
        if remaining_brick:
            size = len(remaining_brick) if wait_load_timer == 90 else min(len(brick_ready) // 3, len(remaining_brick))
            choose_brick = sample(remaining_brick, size)

            for i in choose_brick:
                brick_group.add(brick_ready[i])

            remaining_brick = [i for i in remaining_brick if i not in choose_brick]

    wait_load_timer += 1

    return wait_load_timer


def close_summary(level: int, is_talk: bool, remaining_brick: list, brick_ready: list):
    wait_load_timer = 0
    is_level_load = True
    pop_timer = 0
    if level == 6:
        is_talk = True

    remaining_brick.clear()
    brick_ready.clear()

    return wait_load_timer, is_level_load, pop_timer, is_talk


def fade_surface(alpha: int, timer: int, is_exit: bool, surface: pg.Surface, screen: pg.Surface):
    if is_exit:
        if timer % 30 == 0 and alpha < 255:
            alpha += 85
        timer -= 1

        surface.set_alpha(alpha)
        screen.blit(surface)
        if timer <= -30:
            sys.exit()
    elif alpha > 0 and not is_exit:
        if timer % 30 == 0 and alpha > 0:
            alpha -= 85
        timer += 1

        surface.set_alpha(alpha)
        screen.blit(surface)

    return alpha, timer


def save_file(name: str, score: int, game_total_point: int, flashed: int, flash: int, numbers: tuple):
    stage, level = numbers
    name = name.translate(str.maketrans('!<>:"/\\|?*', '__________'))
    time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    content = {
        'Name': name,
        'Score': score,
        'Stage': f"{stage if stage < 3 else 'Final' if stage == 3 else 'Extra'} - {level}",
        'Rate': calculate_item_rate(game_total_point, stage <= 3, (153, 61)),
        'Flashed': flashed,
        'Date': time[0],
        'Flash': flash
    }

    record(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{time[0]}_{time[1]}.json', ("DX00", content))


def calculate_item_rate(number: int, condition: bool, critical: tuple) -> str:
    return f"{(number / (critical[0] if condition else critical[1])) * 100:.2f} %"