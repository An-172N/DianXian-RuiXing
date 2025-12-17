import random

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


def combo_counter() -> None:
    VARIABLE.comboo_timer -= 1

    if VARIABLE.comboo_timer <= 0:
        if 0 < VARIABLE.combo <= 15:
            VARIABLE.score += 2 ** VARIABLE.combo

        VARIABLE.combo = 0
        VARIABLE.comboo_timer = 90
    else:
        if VARIABLE.combo >= 16:
            VARIABLE.score += 2 ** VARIABLE.combo
            VARIABLE.combo = 0


def item_spawn_regular() -> None:
    VARIABLE.item_spawn_timer += 1
    if VARIABLE.item_spawn_timer >= 45:
        sprite = Base(
            (9, 9, 2),
            DICT.color_dict[6],
            1,
            0
        )
        sprite.speed = -2
        sprite.rect.center = (random.randint(120, 465), 10)
        VARIABLE.item_group.add(sprite)

        VARIABLE.item_spawn_timer = 0


def item_collide(source) -> None:
    VARIABLE.comboo_timer = 90
    if VARIABLE.shoot_cnt <= 7:
        VARIABLE.shoot_cnt += 1

    if source.type == 1:
        if VARIABLE.s_power < 32:
            VARIABLE.s_power += 1
        VARIABLE.combo += 1
        VARIABLE.total_s_power += 1
        VARIABLE.stage_total_s_power += 1
    elif source.type == 2:
        VARIABLE.player += 1
        VARIABLE.combo += 1
        VARIABLE.total_s_power += 1
        VARIABLE.stage_total_s_power += 1

    source.kill()


def item_spawn(brick_pos) -> None:
    if random.random() <= 0.125:
        sprite = Base(
            (9, 9, 2),
            DICT.color_dict[5],
            1,
            1
        )
        sprite.speed = -2
        sprite.rect.center = brick_pos
        VARIABLE.item_group.add(sprite)
        VARIABLE.total_spawn_s_power += 1
    elif random.random() <= 0.007:
        sprite = Base(
            (9, 9, 2),
            DICT.color_dict[2],
            1,
            2
        )
        sprite.speed = -2
        sprite.rect.center = brick_pos
        VARIABLE.item_group.add(sprite)
        VARIABLE.total_spawn_s_power += 1