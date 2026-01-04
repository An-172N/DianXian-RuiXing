import random

import SCRIPT.TABLE as TABLE
import SCRIPT.VARIABLE as VARIABLE


def combo_counter() -> None:
    VARIABLE.combo_timer -= 1

    if VARIABLE.combo_timer <= 0:
        if 0 < VARIABLE.combo <= 15:
            VARIABLE.score += 2 ** VARIABLE.combo

        VARIABLE.combo = 0
        VARIABLE.combo_timer = 120
    else:
        if VARIABLE.combo >= 16:
            VARIABLE.score += 2 ** VARIABLE.combo
            VARIABLE.combo = 0


def item_spawn_regular() -> None:
    VARIABLE.item_spawn_timer += 1
    if VARIABLE.item_spawn_timer >= 45:
        sprite = TABLE.char_dict[7](
            color=TABLE.color_dict[6],
            shape=1,
            type="fire"
        )
        sprite.speed = -2
        sprite.rect.center = (random.randint(120, 465), 10)
        TABLE.item_group.add(sprite)

        VARIABLE.item_spawn_timer = 0


def item_collide(source) -> None:
    VARIABLE.combo_timer = 120
    if VARIABLE.shoot_counter <= 5:
        VARIABLE.shoot_counter += 1

    if source.type is "power":
        if VARIABLE.s_power < 32:
            VARIABLE.s_power += 1
        VARIABLE.combo += 1
        VARIABLE.total_s_power += 1
        VARIABLE.stage_total_s_power += 1
    elif source.type is "flash":
        VARIABLE.player += 1
        VARIABLE.combo += 1
        VARIABLE.total_s_power += 1
        VARIABLE.stage_total_s_power += 1

    source.kill()


def item_spawn(brick) -> None:
    brick_pos = brick.rect.center
    if random.random() <= 0.125:
        sprite = TABLE.char_dict[7](
            color=TABLE.color_dict[5],
            shape=1,
            type="power"
        )
        sprite.speed = -2
        sprite.rect.center = brick_pos
        TABLE.item_group.add(sprite)
        VARIABLE.total_spawn_s_power += 1
    elif random.random() <= 0.007:
        sprite = TABLE.char_dict[7](
            color=TABLE.color_dict[2],
            shape=1,
            type="flash"
        )
        sprite.speed = -2
        sprite.rect.center = brick_pos
        TABLE.item_group.add(sprite)
        VARIABLE.total_spawn_s_power += 1