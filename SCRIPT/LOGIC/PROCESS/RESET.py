from SCRIPT import GLOBAL, LOGIC


def group_empty() -> None:
    GLOBAL.item_group.empty()
    GLOBAL.brick_group.empty()
    GLOBAL.plane_group.empty()
    GLOBAL.bullet_group.empty()
    GLOBAL.particle_group.empty()
    GLOBAL.barrage_group.empty()


def mode_one() -> None:
    GLOBAL.is_pause = False
    GLOBAL.is_summary = False
    GLOBAL.is_talk = False
    GLOBAL.is_save = False
    GLOBAL.is_level_load = False

    GLOBAL.is_collide = False
    GLOBAL.is_s_divide = False
    GLOBAL.cooldown_timer = 0
    GLOBAL.main_char = LOGIC.Kli()
    GLOBAL.total_power = 0

    GLOBAL.shoot_counter = 0
    GLOBAL.is_shoot = True

    GLOBAL.item_spawn_timer = 0
    GLOBAL.combo = 0
    GLOBAL.combo_timer = 120

    GLOBAL.text_part = 0
    GLOBAL.text_number = 0

def mode_two() -> None:
    GLOBAL.stage = 1
    GLOBAL.level = 0
    GLOBAL.char = None

    GLOBAL.no_hurt = 0
    GLOBAL.flash = 3
    GLOBAL.score = 0
    GLOBAL.use_flash = 0

    GLOBAL.power = 0
    GLOBAL.is_shoot = False

    GLOBAL.is_run = False


def cal_s_power() -> str:
    return f"{GLOBAL.divide(GLOBAL.stage_total_power, 153 if GLOBAL.stage <= 3 else 61, 0) * 100:.2f} %"