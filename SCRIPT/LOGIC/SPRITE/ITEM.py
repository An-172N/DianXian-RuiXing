# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import random

from SCRIPT import GLOBAL, LOGIC, FUNC


def combo_counter() -> None:
    GLOBAL.combo_timer -= 1

    if GLOBAL.combo_timer <= 0:
        if GLOBAL.combo > 0:
            GLOBAL.score += 2 ** GLOBAL.combo

        GLOBAL.combo = 0
        GLOBAL.combo_timer = 120


def item_spawn_regular() -> None:
    GLOBAL.item_spawn_timer += 1
    
    if GLOBAL.item_spawn_timer >= 45 and len(GLOBAL.brick_group) > 0:
        sprite = LOGIC.Item("fire", -2, (255, 255, 255))
        sprite.rect.center = (random.randint(120, 465), 10)

        GLOBAL.item_group.add(sprite)

        GLOBAL.item_spawn_timer = 0


def item_collide(item: LOGIC.Item) -> None:
    GLOBAL.combo_timer = 120
    GLOBAL.shoot_counter = int(FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6))

    if item.type == "power":
        GLOBAL.s_power = int(FUNC.clamp(GLOBAL.s_power + 1, 0, 32))
        GLOBAL.combo += 1
        GLOBAL.total_s_power += 1
        GLOBAL.stage_total_s_power += 1
    elif item.type == "flash":
        GLOBAL.player += 1
        GLOBAL.combo += 1
        GLOBAL.total_s_power += 1
        GLOBAL.stage_total_s_power += 1

    item.kill()


def item_spawn(condition: bool, pos: tuple, color: tuple, item_type: str) -> None:
    if condition:
        sprite = LOGIC.Item(item_type, 2.5, color)
        sprite.rect.center = pos

        GLOBAL.item_group.add(sprite)
        
        GLOBAL.total_spawn_s_power += 1