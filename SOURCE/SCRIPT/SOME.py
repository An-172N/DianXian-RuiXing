# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys
import os
import json
from datetime import datetime
from random import random, sample


import pygame as pg
from pygame.sprite import Group


from PRELOAD import *
from LOGIC import *
from SCRIPT.HUMAN import *
from SCRIPT.SPAWN import *


def load_json(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def spawn_barrage(stage: int, group: Group, power: int, type: int, spawn_pos: tuple, locate: tuple):
    index = stage - 1
    if random() <= difficulty[index] + power / 1000:
        (
            lambda: circle_barrage(type, spawn_pos, locate, group),
            lambda: polygon_barrage(type, spawn_pos, locate, group),
            lambda: line_barrage((randint(120, 465), 15), (locate[0] + randint(-64, 64), 345), group, color_dict[6], color_dict[3]),
            lambda: point_barrage(type, locate, group)
        )[index]()


def brick_blast(group: Group, stage: int, color: tuple, rect: pg.Rect):
    if color == color_dict[6]:
        dy = lambda point, dy: (point[0], point[1] + dy)
        (
            lambda: circle_brick(group, rect.center),
            lambda: polygon_brick(group, dy(rect.midleft, -1), dy(rect.midright, -1), dy(rect.midbottom, -1)),
            lambda: line_brick(group, rect.center),
            lambda: point_brick(group)
        )[stage - 1]()


def sprite_loader(numbers: tuple, barrage_group: Group, particle_group: Group, brick_group: Group, bullet_group: Group):
    stage, level = numbers
    char = None
    text = None
    if level == 6:
        char = choose_human(stage, barrage_group, particle_group, brick_group, bullet_group)
        text = json.loads(asset(rf"ASSET\JSON\{stage}.json").decode('utf-8'))
    else:
        load_stage(asset(rf"ASSET\STAGE\{stage}-{level}.stg"), load_brick, color_dict[stage], 4, (127, 22), (15, 15))
        choose_brick(brick_ready, (stage, level), 4, 1)

    return char, text


def choose_human(stage: int, barrage_group: Group, particle_group: Group, brick_group: Group, bullet_group: Group):
    return (
        Ono,
        Hro,
        Nre,
        Qdi
    )[stage - 1](barrage_group, particle_group, brick_group, bullet_group)


def pop_bricks(remaining_brick: list, brick_ready: list, wait_load_timer: int, brick_group: Group):
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


def save_file(name: str, score: int, total_point: int, flashed: int, flash: int, numbers: tuple):
    stage, level = numbers
    name = name.translate(str.maketrans('!<>:"/\\|?*', '__________'))
    time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    content = {
        'Name': name,
        'Score': score,
        'Stage': f"{get_stage(stage)} - {level}",
        'Rate': calculate_item_rate(total_point, stage <= 3),
        'Flashed': flashed,
        'Date': time[0],
        'Flash': flash
    }
    record_json(f'{os.environ["USERPROFILE"]}/Saved Games/DX00', f'{name}_{time[0]}_{time[1]}.json', ("DX00", content))


def calculate_item_rate(number: int, condition: bool):
    return f"{(number / (153 if condition else 61) * 100):.2f} %"