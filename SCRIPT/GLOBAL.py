# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import os
import sys

import pygame

import SCRIPT.LOGIC as LOGIC
import SCRIPT.FUNC as FUNC


asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')
current_module = sys.modules[__name__]
font = pygame.font.Font(os.path.join(asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)
icon = pygame.display.set_icon(pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_ICON.png')))


color_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    4: (251, 234, 18),
    5: (45, 194, 229)
}


char_dict = {
    1: LOGIC.Ono.Ono,
    2: LOGIC.Hro.Hro,
    3: LOGIC.Nre.Nre,
    4: LOGIC.Qdi.Qdi,
    5: LOGIC.Kli.Kli,
    6: LOGIC.DecisionPoint.DecisionPoint,
    7: LOGIC.Base.Base
}


keydown_game_dict = {
    pygame.K_RIGHT: lambda: setattr(current_module, "move_right", True),
    pygame.K_LEFT: lambda: setattr(current_module, "move_left", True),
    pygame.K_x: lambda: setattr(current_module, "is_fast", True),
    pygame.K_z: lambda : setattr(current_module, "can_shoot", False),
    pygame.K_SPACE: lambda : LOGIC.BulletMgr.single_bomb(),
    pygame.K_ESCAPE: lambda: (
        setattr(current_module, "pause", True),
        setattr(current_module, "is_blit", False)
    )
}

keydown_talk_dict = {
    pygame.K_z: lambda : (
        setattr(current_module, "text_number", text_number + 1),
        setattr(current_module, "is_blit", False)
    ),
    pygame.K_x: lambda : setattr(current_module, "talk", False)
}

keydown_pause_dict = {
    pygame.K_ESCAPE: lambda : setattr(current_module, "pause", False),
    pygame.K_q: lambda : (
        LOGIC.Reset.reset1(),
        LOGIC.Reset.reset2(),
        LOGIC.Reset.group_empty(),
        setattr(current_module, "is_blit", False)
    )
}

keydown_start_dict = {
    pygame.K_z: lambda: (
        setattr(current_module, "run", True),
        setattr(current_module, "is_blit", False),
        LOGIC.StageMgr.next_level(),
        LOGIC.StageMgr.level_logic()
    ),
    pygame.K_q: lambda: sys.exit()
}

keydown_over_dict = {
    pygame.K_RETURN: lambda: (
        LOGIC.Key.save_file(),
        LOGIC.Reset.reset1(),
        LOGIC.Reset.reset2(),
        LOGIC.Reset.group_empty(),
        setattr(current_module, "is_blit", False)
    ),
    pygame.K_ESCAPE: lambda: (
        LOGIC.Reset.reset1(),
        LOGIC.Reset.reset2(),
        LOGIC.Reset.group_empty(),
        setattr(current_module, "is_blit", False)
    ),
    pygame.K_BACKSPACE: lambda: (
        setattr(current_module, "name", name[:-1]),
        setattr(current_module, "is_blit", False)
    )
}

keydown_summary_dict = {
    pygame.K_z: lambda: LOGIC.StageMgr.summary_closer()
}


keyup_game_dict = {
    pygame.K_RIGHT: lambda: setattr(current_module, "move_right", False),
    pygame.K_LEFT: lambda: setattr(current_module, "move_left", False),
    pygame.K_x: lambda: setattr(current_module, "is_fast", False),
    pygame.K_z: lambda: setattr(current_module, "can_shoot", True)
}


fibonacci_list = [
    FUNC.fibonacci(0, 1, i) / 100
    for i in range(2, 6)
]


window = pygame.Rect((120, 15, 345, 330))
effective = pygame.Rect(105, -50, 375, 410)


run = False
pause = False
summary = False
talk = False
save = False
level_load = False
is_blit = False


name = ''


s_power = 0
shoot_counter = 0


can_shoot = True


item_spawn_timer = 0
combo_timer = 135
combo = 0


player = 4
no_hurt = 0
score = 0
cooldown_timer = 0
s_flash = 0
total_s_power = 0
stage_total_s_power = 0
total_spawn_s_power = 0


move_right = False
move_left = False
is_fast = False
is_visitable = True
is_s_divide = False
collide = True


text_number = 0
text_part = 0
wait_level_load_timer = 0
stage = 1
level = 0


picture = {
    key: pygame.image.load(file).convert_alpha() for key, file in [
        (1, os.path.join(asset_path, 'IMAGE\IMG_STAGE1BG.png')),
        (2, os.path.join(asset_path, 'IMAGE\IMG_STAGE2BG.png')),
        (3, os.path.join(asset_path, 'IMAGE\IMG_STAGE3BG.png')),
        (4, os.path.join(asset_path, 'IMAGE\IMG_STAGE4BG.png')),
        ("GAME_BG", os.path.join(asset_path, 'IMAGE\IMG_GAMEBG.png')),
        ("MENU_BG", os.path.join(asset_path, 'IMAGE\IMG_MENU.png'))
    ]
}
char_image = {
    key: pygame.image.load(file).convert_alpha() for key, file in [
        ("Kli", os.path.join(asset_path, 'IMAGE\IMG_KLI.png')),
        ("Ono", os.path.join(asset_path, 'IMAGE\IMG_ONO.png')),
        ("Hro", os.path.join(asset_path, 'IMAGE\IMG_HRO.png')),
        ("Nre", os.path.join(asset_path, 'IMAGE\IMG_NRE.png')),
        ("Qdi", os.path.join(asset_path, 'IMAGE\IMG_QDI.png'))
    ]
}
sprite_image = {
    key: pygame.image.load(file).convert_alpha() for key, file in [
        (f"C_BA_{color_dict[1]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEORANGE.png')),
        (f"C_BA_{color_dict[4]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEYELLOW.png')),
        (f"C_BA_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEWHITE.png')),
        (f"P_BA_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBARRAGEGREEN.png')),
        (f"P_BA_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBARRAGEWHITE.png')),
        (f"C_BR_{color_dict[1]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKORANGE.png')),
        (f"C_BR_{color_dict[4]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKYELLOW.png')),
        (f"C_BR_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKWHITE.png')),
        (f"P_BR_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBRICKGREEN.png')),
        (f"P_BR_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBRICKWHITE.png')),
        (f"R_BR_{color_dict[3]}", os.path.join(asset_path, f'IMAGE\IMG_RECTANGLEBRICKPURPLE.png')),
        (f"R_BR_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_RECTANGLEBRICKWHITE.png')),
        (f"R_IT_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_ITEMGREEN.png')),
        (f"R_IT_{color_dict[5]}", os.path.join(asset_path, f'IMAGE\IMG_ITEMBLUE.png')),
        (f"R_IT_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_ITEMWHITE.png')),
        ("KLI_BULLET", os.path.join(asset_path, f'IMAGE\IMG_KLIBULLET.png')),
        ("KLI_BOMB", os.path.join(asset_path, f'IMAGE\IMG_KLIBOMB.png')),
        ("DEC", os.path.join(asset_path, f'IMAGE\IMG_DECISIONPOINT.png')),
    ]
}


background = picture["GAME_BG"]
second_background = picture[stage]


char = None
text = None


main_char = char_dict.get(5)()
decision_point = char_dict.get(6)()


plane_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
barrage_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()


last_time = pygame.time.get_ticks()
fps_text = last_time


def divide(dividend: float, divisor: float, default: float) -> float:
    return dividend / divisor if divisor != 0 else default