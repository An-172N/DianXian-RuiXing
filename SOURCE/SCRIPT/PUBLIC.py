# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import json


import PRELOAD
from LOGIC import File
from SCRIPT import HUMAN, SPRITE, GLOBAL


def sprite_loader() -> None:
    if GLOBAL.level == 6:
        GLOBAL.char = choose_human()
        GLOBAL.text = json.loads(PRELOAD.asset(rf"ASSET\JSON\TALK_{GLOBAL.stage}.json").decode('utf-8'))
        GLOBAL.is_talk = True
        GLOBAL.is_blit = False

        GLOBAL.brick_group.add(GLOBAL.char)
    else:
        File.read_level(PRELOAD.asset(rf"ASSET\STAGE\STG_{GLOBAL.stage}-{GLOBAL.level}.stg"), SPRITE.Brick.load_brick, PRELOAD.color_dict[GLOBAL.stage], 4, 0.031, (127, 22), (15, 15), GLOBAL.brick_group)
        SPRITE.Brick.choose_brick(GLOBAL.brick_group, (GLOBAL.stage, GLOBAL.level), 4, 1)


def choose_human() -> HUMAN.Ono | HUMAN.Hro | HUMAN.Nre | HUMAN.Qdi:
    char_dict = {
        1: HUMAN.Ono,
        2: HUMAN.Hro,
        3: HUMAN.Nre,
        4: HUMAN.Qdi
    }

    return char_dict.get(GLOBAL.stage)(GLOBAL.barrage_group, GLOBAL.particle_group, GLOBAL.main_char.rect.center)