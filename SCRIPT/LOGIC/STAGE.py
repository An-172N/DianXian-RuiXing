# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import json

import pygame

from SCRIPT import SPRITE


def score_summary(power: int, unflash: int, combo: int, collection: tuple) -> int:
    return power * collection[0] + unflash * collection[1] + collection[2] ** combo + combo * collection[3]


def close_summary(is_summary: bool, stage_level: tuple, score: int, add_score: int, end_stage_level: tuple, end: object, not_end: object) -> tuple:
    is_summary = False
    score += add_score

    end() if stage_level[0] >= end_stage_level[0] and stage_level[1] == end_stage_level[1] else not_end()

    return is_summary, score


def change_background(picture: pygame.Surface, alpha: int) -> pygame.Surface:
    second_background = picture
    second_background.set_alpha(alpha)

    return second_background


def level_load(timer: int, is_level_load: bool, end: int, load: object) -> tuple:
    if timer <= end:
        timer += 1
    else:
        load()

        timer = 0
        is_level_load = True

    return timer, is_level_load


def level_summary(condition: bool, is_summary: bool) -> bool:
    if condition:
        is_summary = True

    return is_summary


def level_logic(stage_level: tuple, end: int) -> tuple:
    stage = stage_level[0]
    level = stage_level[1]

    if level >= end:
        stage += 1
        level = 1
    else:
        level += 1

    return stage, level


def load_stage(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple, group: pygame.sprite.Group) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if random.random() >= rate else (255, 255, 255)
            brick = SPRITE.Brick(shape, hp, c, (size[0] + i * interval[0], size[1] + row * interval[1]))

            group.add(brick)


def load_text(file: str) -> str:
    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)