# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import random
import json
import os

import SCRIPT.GLOBAL as GLOBAL


def next_level() -> None:
    GLOBAL.score += GLOBAL.total_s_power * 512
    GLOBAL.score += GLOBAL.no_hurt * 4096
    GLOBAL.score += 2 ** GLOBAL.combo + GLOBAL.combo * 2

    GLOBAL.reset1()
    GLOBAL.group_empty()

    GLOBAL.no_hurt += 1
    GLOBAL.main_char.rect.center = (292, 331)
    GLOBAL.plane_group.add(GLOBAL.main_char)
    GLOBAL.plane_group.add(GLOBAL.decision_point)


def summary_closer() -> None:
    GLOBAL.summary = False

    if GLOBAL.stage >= 3 and GLOBAL.level == 6:
        GLOBAL.save = True
        GLOBAL.is_blit = False
    else:
        next_level()
        level_logic()


def sprite_loader() -> None:
    if GLOBAL.level == 6:
        GLOBAL.char = chs_shhm()
        GLOBAL.char.rect.center = (292, 60)
        GLOBAL.text = load_text(GLOBAL.stage)
        GLOBAL.talk = True
        GLOBAL.is_blit = False

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        level_file = os.path.join(GLOBAL.asset_path, f"STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg")
        with open(level_file, 'r', encoding="ascii") as f:
            string = f.read().splitlines()
            
            for row, line in enumerate(string, 0):
                load_stage(row, line)

            choose_brick()


def level_load() -> None:
    if GLOBAL.wait_level_load_timer <= 60:
        GLOBAL.wait_level_load_timer += 1
    else:
        sprite_loader()

        GLOBAL.second_background = GLOBAL.picture[GLOBAL.stage]
        GLOBAL.second_background.set_alpha(159)
        GLOBAL.wait_level_load_timer = 0
        GLOBAL.level_load = True


def level_summary() -> None:
    if len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.talk:
        GLOBAL.summary = True
        GLOBAL.is_blit = False


def level_process() -> None:
    if not GLOBAL.level_load:
        level_load()
    else:
        level_summary()


def level_logic() -> None:
    if GLOBAL.level >= 6:
        GLOBAL.stage += 1
        GLOBAL.level = 1
    else:
        GLOBAL.level += 1


def chs_shhm() -> object:
    return GLOBAL.char_dict.get(GLOBAL.stage)()


def shhm_lose() -> None:
    GLOBAL.text_part += 1
    GLOBAL.text_number = 0

    GLOBAL.talk = True
    GLOBAL.is_blit = False


def load_stage(row, line) -> None:
    rand = random.random

    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = GLOBAL.color_dict[GLOBAL.stage] if rand() >= 0.031 else (255, 255, 255)
            brick = GLOBAL.char_dict[7](color=c, shape=shape, type="brick")

            if not hasattr(brick, "hp"):
                brick.hp = 4
            brick.rect.center = (127 + i * 15, 22 + row * 15)

            GLOBAL.brick_group.add(brick)


def choose_brick() -> None:
    sample = random.sample
    brick_list = list(GLOBAL.brick_group)
    choose_power = sample(range(len(brick_list)), 10 + GLOBAL.level)
    choose_flash = sample(range(len(brick_list)), 1)
    
    for i in choose_power:
        brick_list[i].have_power = True
    for j in choose_flash:
        brick_list[j].have_flash = True


def load_text(stage) -> str:
    file = os.path.join(GLOBAL.asset_path, f"JSON\TALK_{stage}.json")

    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)