import random as rand
import json
import os

from typing import Optional, Any

import FUNC
import SCRIPT.DICT
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.RESET

from SCRIPT.LOGIC.FRIEND.BASE import Base


def next_level() -> None:
    VARIABLE.score += VARIABLE.total_s_power * 512
    VARIABLE.score += VARIABLE.no_hurt * 4096

    SCRIPT.RESET.reset1()

    VARIABLE.no_hurt += 1
    VARIABLE.main_char.rect.center = (292, 331)
    VARIABLE.plane_group.add(VARIABLE.main_char)
    VARIABLE.plane_group.add(VARIABLE.d_pt)


def level_load() -> None:
    if VARIABLE.timer <= 60:
        VARIABLE.timer += 1
    else:
        if VARIABLE.level == 6:
            VARIABLE.char = chs_shhm()
            VARIABLE.char.rect.center = (292, 60)
            VARIABLE.text = load_text(VARIABLE.stage)
            VARIABLE.text_number = 0
            VARIABLE.talk = True

            VARIABLE.brick_group.add(VARIABLE.char)
        else:
            for i in FUNC.Process.process_file(
                os.path.join(SCRIPT.DICT.asset_path, f"STG_{VARIABLE.stage}-{VARIABLE.level}.stg"),
                'ascii',
                0,
                load_stage
            ):
                i

        VARIABLE.second_background = VARIABLE.picture[VARIABLE.stage]
        VARIABLE.second_background.set_alpha(159)
        VARIABLE.timer = 0
        VARIABLE.level_load = True


def level_summary() -> None:
    if (
        len(VARIABLE.brick_group) == 0
        and not VARIABLE.talk
    ):
        if VARIABLE.timer <= 90:
            VARIABLE.timer += 1
            VARIABLE.summary = True
        else:
            if VARIABLE.stage >= 2 and VARIABLE.level == 6:
                VARIABLE.summary = False
                VARIABLE.save = True
                VARIABLE.timer = 0
            else:
                next_level()
                level_logic()

                VARIABLE.summary = False
                VARIABLE.timer = 0


def level_process() -> None:
    if not VARIABLE.level_load:
        level_load()
    else:
        level_summary()


def level_logic() -> None:
    if VARIABLE.level >= 6:
        VARIABLE.stage += 1
        VARIABLE.level = 1
    else:
        VARIABLE.level += 1


def chs_shhm() -> Optional[Any]:
    return SCRIPT.DICT.char_dict.get(VARIABLE.stage)()


def shhm_lose() -> None:
    VARIABLE.text_part += 1
    VARIABLE.text_number = 0

    VARIABLE.talk = True


def load_stage(row, line) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = (
                SCRIPT.DICT.color_dict[VARIABLE.stage]
                if rand.random() >= 0.063 
                else SCRIPT.DICT.color_dict[6]
            )
            x = 127 + i * 15
            y = 22 + row * 15

            brick = Base(
                (15, 15, 2),
                c,
                shape
            )

            if not hasattr(brick, "hp"):
                brick.hp = 4
            brick.rect.center = (x, y)

            VARIABLE.brick_group.add(brick)


def load_text(stage) -> str:
    file = os.path.join(SCRIPT.DICT.asset_path, f"TALK_{stage}.json")

    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)