import SCRIPT.GLOBAL as GLOBAL


def group_empty() -> None:
    GLOBAL.item_group.empty()
    GLOBAL.brick_group.empty()
    GLOBAL.plane_group.empty()
    GLOBAL.bullet_group.empty()
    GLOBAL.particle_group.empty()
    GLOBAL.barrage_group.empty()


def reset1() -> None:
    GLOBAL.pause = False
    GLOBAL.summary = False
    GLOBAL.talk = False
    GLOBAL.save = False
    GLOBAL.level_load = False

    GLOBAL.collide = False
    GLOBAL.is_s_divide = False
    GLOBAL.cooldown_timer = 0
    GLOBAL.main_char = GLOBAL.char_dict.get(5)()
    GLOBAL.total_s_power = 0

    GLOBAL.shoot_counter = 0
    GLOBAL.can_shoot = True

    GLOBAL.item_spawn_timer = 0
    GLOBAL.combo = 0
    GLOBAL.combo_timer = 135

    GLOBAL.text_part = 0
    GLOBAL.text_number = 0

def reset2() -> None:
    GLOBAL.stage = 1
    GLOBAL.level = 0
    GLOBAL.char = None

    GLOBAL.no_hurt = 0
    GLOBAL.player = 4
    GLOBAL.score = 0
    GLOBAL.s_flash = 0

    GLOBAL.s_power = 0
    GLOBAL.can_shoot = False

    GLOBAL.run = False


def cal_s_power() -> str:
    return f"{GLOBAL.divide(GLOBAL.stage_total_s_power, GLOBAL.total_spawn_s_power, 0) * 100:.2f} %"