# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import random

import SCRIPT.GLOBAL as GLOBAL
import SCRIPT.FUNC as FUNC


def combo_counter() -> None:
    GLOBAL.combo_timer -= 1

    if GLOBAL.combo_timer <= 0:
        if GLOBAL.combo > 0:
            GLOBAL.score += 2 ** GLOBAL.combo

        GLOBAL.combo = 0
        GLOBAL.combo_timer = 136


def item_spawn_regular() -> None:
    GLOBAL.item_spawn_timer += 1
    randint = random.randint
    
    if GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0:
        sprite = GLOBAL.char_dict[7](color=(255, 255, 255), shape=1, type="fire")
        sprite.speed = -2
        sprite.rect.center = (randint(120, 465), 10)
        GLOBAL.item_group.add(sprite)

        GLOBAL.item_spawn_timer = 0


def item_collide(source) -> None:
    GLOBAL.combo_timer = 136
    GLOBAL.shoot_counter = int(FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6))

    if source.type == "power":
        GLOBAL.s_power = int(FUNC.clamp(GLOBAL.s_power + 1, 0, 32))
        GLOBAL.combo += 1
        GLOBAL.total_s_power += 1
        GLOBAL.stage_total_s_power += 1
    elif source.type == "flash":
        GLOBAL.player += 1
        GLOBAL.combo += 1
        GLOBAL.total_s_power += 1
        GLOBAL.stage_total_s_power += 1

    source.kill()


def item_spawn(brick) -> None:
    brick_pos = brick.rect.center
    uniform = random.uniform

    if brick.have_power:
        sprite = GLOBAL.char_dict[7](color=GLOBAL.color_dict[5], shape=1, type="power")
        sprite.speed = uniform(2.0, 3.5)
        sprite.rect.center = brick_pos
        GLOBAL.item_group.add(sprite)
        GLOBAL.total_spawn_s_power += 1
    elif brick.have_flash:
        sprite = GLOBAL.char_dict[7](color=GLOBAL.color_dict[2], shape=1, type="flash")
        sprite.speed = uniform(2.0, 3.5)
        sprite.rect.center = brick_pos
        GLOBAL.item_group.add(sprite)
        GLOBAL.total_spawn_s_power += 1