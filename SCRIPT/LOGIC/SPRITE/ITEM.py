import random

import SCRIPT.GLOBAL as GLOBAL


def combo_counter() -> None:
    GLOBAL.combo_timer -= 1

    if GLOBAL.combo_timer <= 0:
        if 0 < GLOBAL.combo <= 15:
            GLOBAL.score += 2 ** GLOBAL.combo

        GLOBAL.combo = 0
        GLOBAL.combo_timer = 120
    else:
        if GLOBAL.combo >= 16:
            GLOBAL.score += 2 ** GLOBAL.combo
            GLOBAL.combo = 0


def item_spawn_regular() -> None:
    GLOBAL.item_spawn_timer += 1
    if GLOBAL.item_spawn_timer >= 45:
        sprite = GLOBAL.char_dict[7](
            color=GLOBAL.color_dict[6],
            shape=1,
            type="fire"
        )
        sprite.speed = -2
        sprite.rect.center = (random.randint(120, 465), 10)
        GLOBAL.item_group.add(sprite)

        GLOBAL.item_spawn_timer = 0


def item_collide(source) -> None:
    GLOBAL.combo_timer = 120
    if GLOBAL.shoot_counter <= 5:
        GLOBAL.shoot_counter += 1

    if source.type is "power":
        if GLOBAL.s_power < 32:
            GLOBAL.s_power += 1
        GLOBAL.combo += 1
        GLOBAL.total_s_power += 1
        GLOBAL.stage_total_s_power += 1
    elif source.type is "flash":
        GLOBAL.player += 1
        GLOBAL.combo += 1
        GLOBAL.total_s_power += 1
        GLOBAL.stage_total_s_power += 1

    source.kill()


def item_spawn(brick) -> None:
    brick_pos = brick.rect.center
    if random.random() <= 0.125:
        sprite = GLOBAL.char_dict[7](
            color=GLOBAL.color_dict[5],
            shape=1,
            type="power"
        )
        sprite.speed = -2
        sprite.rect.center = brick_pos
        GLOBAL.item_group.add(sprite)
        GLOBAL.total_spawn_s_power += 1
    elif random.random() <= 0.007:
        sprite = GLOBAL.char_dict[7](
            color=GLOBAL.color_dict[2],
            shape=1,
            type="flash"
        )
        sprite.speed = -2
        sprite.rect.center = brick_pos
        GLOBAL.item_group.add(sprite)
        GLOBAL.total_spawn_s_power += 1