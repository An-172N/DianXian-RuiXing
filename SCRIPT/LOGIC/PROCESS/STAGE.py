# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import random
import json
import os

from SCRIPT import GLOBAL, LOGIC


def next_level() -> None:
    LOGIC.Reset.mode_one()
    LOGIC.Reset.group_empty()

    GLOBAL.no_hurt += 1
    GLOBAL.plane_group.add(GLOBAL.main_char)
    GLOBAL.plane_group.add(GLOBAL.decision_point)
    GLOBAL.main_char.rect.center = (292, 332)
    GLOBAL.decision_point.rect.center = (292, 332)


def score_summary(power: int, unhurt: int, combo: int, collection: tuple):
    return power * collection[0] + unhurt * collection[1] + collection[2] ** combo + combo * collection[3]


def summary_closer() -> None:
    GLOBAL.is_summary = False

    GLOBAL.score += score_summary(GLOBAL.total_power, GLOBAL.no_hurt, GLOBAL.combo, (512, 4096, 2, 2))

    if GLOBAL.stage >= 3 and GLOBAL.level == 6:
        GLOBAL.is_save = True
        GLOBAL.is_blit = False
    else:
        next_level()
        level_logic()


def sprite_loader() -> None:
    if GLOBAL.level == 6:
        GLOBAL.char = chs_shhm()
        GLOBAL.char.rect.center = (292, 60)
        GLOBAL.text = load_text(GLOBAL.stage)
        GLOBAL.is_talk = True
        GLOBAL.is_blit = False

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        level_file = os.path.join(GLOBAL.asset_path, f"STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg")
        with open(level_file, 'r', encoding="ascii") as f:
            string = f.read().splitlines()
            
            for row, line in enumerate(string):
                load_stage(row, line)

            choose_brick()


def level_load() -> None:
    if GLOBAL.wait_level_load_timer <= 60:
        GLOBAL.wait_level_load_timer += 1
    else:
        sprite_loader()

        GLOBAL.second_background = GLOBAL.picture[GLOBAL.stage]
        GLOBAL.second_background.set_alpha(191)
        GLOBAL.wait_level_load_timer = 0
        GLOBAL.is_level_load = True


def level_summary() -> None:
    if len(GLOBAL.brick_group) == 0 and len(GLOBAL.item_group) == 0 and not GLOBAL.is_talk:
        GLOBAL.is_summary = True
        GLOBAL.is_blit = False


def level_process() -> None:
    if not GLOBAL.is_level_load:
        level_load()
    else:
        level_summary()


def level_logic() -> None:
    if GLOBAL.level >= 6:
        GLOBAL.stage += 1
        GLOBAL.level = 1
    else:
        GLOBAL.level += 1


def chs_shhm() -> LOGIC.Ono | LOGIC.Hro | LOGIC.Nre | LOGIC.Qdi:
    char_dict = {
        1: LOGIC.Ono,
        2: LOGIC.Hro,
        3: LOGIC.Nre,
        4: LOGIC.Qdi,
        5: LOGIC.Kli
    }

    return char_dict.get(GLOBAL.stage)()


def shhm_lose() -> None:
    GLOBAL.text_part += 1
    GLOBAL.text_number = 0

    GLOBAL.is_talk = True
    GLOBAL.is_blit = False


def load_stage(row: int, line: str) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = GLOBAL.color_dict[GLOBAL.stage] if random.random() >= 0.031 else (255, 255, 255)
            brick = LOGIC.Brick(shape, 4, c)
            brick.rect.center = (127 + i * 15, 22 + row * 15)

            GLOBAL.brick_group.add(brick)


def choose_brick() -> None:
    brick_list = list(GLOBAL.brick_group)
    choose_power = random.sample(range(len(brick_list)), 4 + GLOBAL.level + GLOBAL.stage)
    choose_flash = random.sample(range(len(brick_list)), 1)
    
    for i in choose_power:
        brick_list[i].have_power = True
    for j in choose_flash:
        brick_list[j].have_flash = True


def load_text(stage: int) -> str:
    file = os.path.join(GLOBAL.asset_path, f"JSON\TALK_{stage}.json")

    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)