import SCRIPT.VARIABLE as VARIABLE


def reset1() -> None:
    VARIABLE.pause = False
    VARIABLE.summary = False
    VARIABLE.talk = False
    VARIABLE.save = False
    VARIABLE.level_load = False

    VARIABLE.item_group.empty(),
    VARIABLE.brick_group.empty(),
    VARIABLE.plane_group.empty(),
    VARIABLE.bullet_group.empty(),
    VARIABLE.particle_group.empty(),
    VARIABLE.barrage_group.empty()

    VARIABLE.collide = False
    VARIABLE.is_s_divide = False
    VARIABLE.cooldown_time = 0
    VARIABLE.main_char.bomb.bomb_cnt = 0
    VARIABLE.main_char.bomb.timer = 0
    VARIABLE.total_s_power = 0

    VARIABLE.shoot_cnt = 0
    VARIABLE.can_shoot = True

    VARIABLE.item_spawn_timer = 0

    VARIABLE.text_part = 0
    VARIABLE.text_number = 0

def reset2() -> None:
    VARIABLE.stage = 1
    VARIABLE.level = 0
    VARIABLE.char = None

    VARIABLE.no_hurt = 0
    VARIABLE.player = 4
    VARIABLE.score = 0
    VARIABLE.s_flash = 0

    VARIABLE.s_power = 0
    VARIABLE.can_shoot = False

    VARIABLE.combo = 0

    VARIABLE.run = False