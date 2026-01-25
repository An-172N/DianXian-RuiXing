# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import json

import pygame

from SCRIPT import SPRITE


def score_summary(power: int, unhurt: int, combo: int, collection: tuple):
    return power * collection[0] + unhurt * collection[1] + collection[2] ** combo + combo * collection[3]


def close_summary(is_summary: bool, is_save: bool, is_blit: bool, stage: int, level: int, score: int, add_score: int, not_end: object) -> tuple:
    is_summary = False

    score += add_score

    if stage >= 3 and level == 6:
        is_save = True
        is_blit = False
    else:
        not_end()

    return is_summary, is_save, is_blit, score


def change_background(picture: pygame.Surface):
    second_background = picture
    second_background.set_alpha(128)

    return second_background


def level_load(timer: int, is_level_load: bool, load: object) -> tuple:
    if timer <= 60:
        timer += 1
    else:
        load()

        timer = 0
        is_level_load = True

    return timer, is_level_load


def level_summary(group1: pygame.sprite.Group, group2: pygame.sprite.Group, condition: bool, is_summary: bool, is_blit: bool) -> tuple:
    if len(group1) == 0 and len(group2) == 0 and not condition:
        is_summary = True
        is_blit = False

    return is_summary, is_blit


def level_logic(stage: int, level: int) -> tuple:
    if level >= 6:
        stage += 1
        level = 1
    else:
        level += 1

    return stage, level


def boss_lose(part: int, number: int, is_talk: bool, is_blit: bool) -> tuple:
    part += 1
    number = 0

    is_talk = True
    is_blit = False

    return part, number, is_talk, is_blit


def load_stage(row: int, line: str, color: tuple, group: pygame.sprite.Group) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if random.random() >= 0.031 else (255, 255, 255)
            brick = SPRITE.Brick(shape, 4, c, (127 + i * 15, 22 + row * 15))

            group.add(brick)


def choose_brick(group: pygame.sprite.Group, stage: int, level: int) -> None:
    brick_list = list(group)
    choose_power = random.sample(range(len(brick_list)), 4 + level + stage)
    choose_flash = random.sample(range(len(brick_list)), 1)
    
    for i in choose_power:
        brick_list[i].have_power = True
    for j in choose_flash:
        brick_list[j].have_flash = True


def load_text(file: str) -> str:
    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)