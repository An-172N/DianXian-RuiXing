import random
import json
import os

from typing import Optional, Any

import SCRIPT.FUNC as FUNC
import SCRIPT.TABLE as TABLE
import SCRIPT.VARIABLE as VARIABLE


def next_level() -> None:
    VARIABLE.score += VARIABLE.total_s_power * 512
    VARIABLE.score += VARIABLE.no_hurt * 4096

    VARIABLE.reset1()

    VARIABLE.no_hurt += 1
    VARIABLE.main_char.rect.center = (292, 331)
    TABLE.plane_group.add(VARIABLE.main_char)
    TABLE.plane_group.add(VARIABLE.decision_point)


def level_load() -> None:
    if VARIABLE.wait_level_load_timer <= 60:
        VARIABLE.wait_level_load_timer += 1
    else:
        if VARIABLE.level == 6:
            VARIABLE.char = chs_shhm()
            VARIABLE.char.rect.center = (292, 60)
            VARIABLE.text = load_text(VARIABLE.stage)
            VARIABLE.talk = True
            VARIABLE.is_blit = False

            TABLE.brick_group.add(VARIABLE.char)
        else:
            level_file = os.path.join(TABLE.asset_path, f"STAGE\STG_{VARIABLE.stage}-{VARIABLE.level}.stg")
            with open(level_file, 'r', encoding="ascii") as f:
                string = f.read()
                for i in FUNC.Process.process_file(
                    string,
                    0,
                    load_stage
                ):
                    i

        VARIABLE.second_background = VARIABLE.picture[VARIABLE.stage]
        VARIABLE.second_background.set_alpha(159)
        VARIABLE.wait_level_load_timer = 0
        VARIABLE.level_load = True


def level_summary() -> None:
    if (
        len(TABLE.brick_group) == 0
        and not VARIABLE.talk
    ):
        if VARIABLE.wait_level_load_timer <= 120:
            VARIABLE.wait_level_load_timer += 1
            VARIABLE.summary = True
            VARIABLE.is_blit = False
        else:
            if VARIABLE.stage >= 3 and VARIABLE.level == 6:
                VARIABLE.summary = False
                VARIABLE.save = True
                VARIABLE.is_blit = False
                VARIABLE.wait_level_load_timer = 0
            else:
                next_level()
                level_logic()

                VARIABLE.summary = False
                VARIABLE.wait_level_load_timer = 0


def level_process() -> None:
    if not VARIABLE.level_load:
        level_load()
        VARIABLE.is_blit = False
    else:
        level_summary()


def level_logic() -> None:
    if VARIABLE.level >= 6:
        VARIABLE.stage += 1
        VARIABLE.level = 1
    else:
        VARIABLE.level += 1


def chs_shhm() -> Optional[Any]:
    return TABLE.char_dict.get(VARIABLE.stage)()


def shhm_lose() -> None:
    VARIABLE.text_part += 1
    VARIABLE.text_number = 0

    VARIABLE.talk = True
    VARIABLE.is_blit = False


def load_stage(row, line) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = (
                TABLE.color_dict[VARIABLE.stage]
                if random.random() >= 0.042
                else TABLE.color_dict[6]
            )
            x = 127 + i * 15
            y = 22 + row * 15

            brick = TABLE.char_dict[7](
                color=c,
                shape=shape,
                type="brick"
            )

            if not hasattr(brick, "hp"):
                brick.hp = 4
            brick.rect.center = (x, y)

            TABLE.brick_group.add(brick)


def load_text(stage) -> str:
    file = os.path.join(TABLE.asset_path, f"JSON\TALK_{stage}.json")

    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)