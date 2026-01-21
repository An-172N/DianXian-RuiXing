# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from SCRIPT import GLOBAL, LOGIC, FUNC


def combo_counter() -> None:
    GLOBAL.combo_timer -= 1

    if GLOBAL.combo_timer <= 0:
        if GLOBAL.combo > 0:
            GLOBAL.score += 2 ** GLOBAL.combo

        GLOBAL.combo = 0
        GLOBAL.combo_timer = 120


def item_collide(item: LOGIC.Item) -> None:
    GLOBAL.combo_timer = 120
    GLOBAL.shoot_counter = int(FUNC.clamp(GLOBAL.shoot_counter + 1, 0, 6))

    if item.type == "power":
        GLOBAL.power = int(FUNC.clamp(GLOBAL.power + 1, 0, 32))
        GLOBAL.combo += 1
        GLOBAL.total_power += 1
        GLOBAL.stage_total_power += 1
    elif item.type == "flash":
        GLOBAL.flash += 1
        GLOBAL.combo += 1
        GLOBAL.total_power += 1
        GLOBAL.stage_total_power += 1

    item.kill()


def item_spawn(condition: bool, pos: tuple, speed: float, color: tuple, item_type: str, timer: int=0) -> None:
    timer += 1

    if condition:
        sprite = LOGIC.Item(item_type, speed, color)
        sprite.rect.center = pos

        GLOBAL.item_group.add(sprite)

        timer = 0

    return timer