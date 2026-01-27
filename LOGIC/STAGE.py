# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def score_summary(power: int, unflash: int, combo: int, collection: tuple) -> int:
    return power * collection[0] + unflash * collection[1] + collection[2] ** combo + combo * collection[3]


def close_summary(summary: bool, stage_level: tuple, score: int, add_score: int, final_stage: tuple, end: object, not_end: object) -> tuple:
    summary = False
    score += add_score

    end() if stage_level[0] >= final_stage[0] and stage_level[1] == final_stage[1] else not_end()

    return summary, score


def change_background(picture: pygame.Surface, alpha: int) -> pygame.Surface:
    background = picture
    background.set_alpha(alpha)

    return background


def level_load(timer: int, is_level_load: bool, end: int, load: object) -> tuple:
    if timer <= end:
        timer += 1
    else:
        load()

        timer = 0
        is_level_load = True

    return timer, is_level_load


def level_logic(stage_level: tuple, end: int) -> tuple:
    stage, level = stage_level

    if level >= end:
        stage += 1
        level = 1
    else:
        level += 1

    return stage, level