# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from PRELOAD import color_dict, picture
from LOGIC.TOOL import draw_rectangle
from LOGIC.SPRITE import Rect
from SCRIPT.HUMAN import Kli
from SCRIPT import GLOBAL


def mode_one() -> None:
    GLOBAL.is_pause = False
    GLOBAL.is_summary = False
    GLOBAL.is_talk = False
    GLOBAL.is_save = False
    GLOBAL.is_level_load = False

    GLOBAL.animate_timer = 0

    GLOBAL.item_group.empty()
    GLOBAL.brick_group.empty()
    GLOBAL.plane_group.empty()
    GLOBAL.bullet_group.empty()
    GLOBAL.particle_group.empty()
    GLOBAL.barrage_group.empty()
    GLOBAL.text_group.empty()

    GLOBAL.is_collide = False
    GLOBAL.is_s_divide = False
    GLOBAL.cooldown_timer = 0
    GLOBAL.main_char = Kli(GLOBAL.bullet_group, GLOBAL.particle_group)
    GLOBAL.decision_point = Rect(draw_rectangle((2, 2), 0, color_dict[7]).convert(), (292, 332), True)
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

    GLOBAL.second_background = picture[GLOBAL.stage]

    GLOBAL.no_flash = 0
    GLOBAL.flash = 3
    GLOBAL.score = 0
    GLOBAL.use_flash = 0

    GLOBAL.power = 0
    GLOBAL.is_shoot = False

    GLOBAL.is_run = False