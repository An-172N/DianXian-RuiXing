# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import os
import sys

import pygame

import SCRIPT.LOGIC as LOGIC
import SCRIPT.FUNC as FUNC

clock = pygame.time.Clock()
asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')
current_module = sys.modules[__name__]
font = pygame.font.Font(os.path.join(asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)
icon = pygame.display.set_icon(pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_ICON.png')))
screen = pygame.display.set_mode((480, 360), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED, vsync=1)


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
    pygame.K_LSHIFT: lambda: setattr(current_module, "is_slow", True),
    pygame.K_z: lambda : setattr(current_module, "can_shoot", False),
    pygame.K_x: lambda : LOGIC.BulletMgr.single_bomb(),
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
        reset1(),
        reset2(),
        group_empty(),
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
        reset1(),
        reset2(),
        group_empty(),
        setattr(current_module, "is_blit", False)
    ),
    pygame.K_ESCAPE: lambda: (
        reset1(),
        reset2(),
        group_empty(),
        setattr(current_module, "is_blit", False)
    ),
    pygame.K_BACKSPACE: lambda: (
        setattr(current_module, "name", name[:-1]),
        setattr(current_module, "is_blit", False)
    )
}


keyup_game_dict = {
    pygame.K_RIGHT: lambda: setattr(current_module, "move_right", False),
    pygame.K_LEFT: lambda: setattr(current_module, "move_left", False),
    pygame.K_LSHIFT: lambda: setattr(current_module, "is_slow", False),
    pygame.K_z: lambda: setattr(current_module, "can_shoot", True)
}


fibonacci_list = [
    FUNC.fibonacci(0, 1, i) / 100
    for i in range(2, 6)
]

picture_list = [
    (1, os.path.join(asset_path, 'IMAGE\IMG_STAGE1BG.png')),
    (2, os.path.join(asset_path, 'IMAGE\IMG_STAGE2BG.png')),
    (3, os.path.join(asset_path, 'IMAGE\IMG_STAGE3BG.png')),
    (4, os.path.join(asset_path, 'IMAGE\IMG_STAGE4BG.png')),
    ("GAME_BG", os.path.join(asset_path, 'IMAGE\IMG_GAMEBG.png')),
    ("MENU_BG", os.path.join(asset_path, 'IMAGE\IMG_MENU.png'))
]

char_image_list = [
    ("Kli", os.path.join(asset_path, 'IMAGE\IMG_KLI.png')),
    ("Ono", os.path.join(asset_path, 'IMAGE\IMG_ONO.png')),
    ("Hro", os.path.join(asset_path, 'IMAGE\IMG_HRO.png')),
    ("Nre", os.path.join(asset_path, 'IMAGE\IMG_NRE.png')),
    ("Qdi", os.path.join(asset_path, 'IMAGE\IMG_QDI.png'))
]

sprite_image_list = [
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


window = pygame.Rect((120, 15, 345, 330))
effective = pygame.Rect((105, 0, 375, 360))


run = False
pause = False
summary = False
talk = False
save = False
level_load = False
is_blit = False


last_time = pygame.time.get_ticks()
fps_text = last_time


name = ''


s_power = 0
shoot_counter = 0


can_shoot = True


item_spawn_timer = 0
combo_timer = 120
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
is_slow = False
is_visitable = True
is_s_divide = False
collide = True


text_number = 0
text_part = 0
wait_level_load_timer = 0
stage = 1
level = 0


picture = FUNC.preload(picture_list, lambda f: pygame.image.load(f).convert_alpha())
char_image = FUNC.preload(char_image_list, lambda f: pygame.image.load(f).convert_alpha())
sprite_image = FUNC.preload(sprite_image_list, lambda f: pygame.image.load(f).convert_alpha())


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

def load_image(file):
    pygame.image.load(file).convert_alpha()


def group_empty() -> None:
    item_group.empty()
    brick_group.empty()
    plane_group.empty()
    bullet_group.empty()
    particle_group.empty()
    barrage_group.empty()


def reset1() -> None:
    global pause, summary, talk, save, level_load
    global collide, is_s_divide, cooldown_timer, total_s_power
    global shoot_counter, can_shoot
    global item_spawn_timer
    global text_number, text_part
    global main_char
    
    pause = False
    summary = False
    talk = False
    save = False
    level_load = False

    collide = False
    is_s_divide = False
    cooldown_timer = 0
    main_char = char_dict.get(5)()
    total_s_power = 0

    shoot_counter = 0
    can_shoot = True

    item_spawn_timer = 0

    text_part = 0
    text_number = 0

def reset2() -> None:
    global stage, level, char
    global no_hurt, player, score, s_flash
    global s_power, can_shoot, combo
    global run

    stage = 1
    level = 0
    char = None

    no_hurt = 0
    player = 4
    score = 0
    s_flash = 0

    s_power = 0
    can_shoot = False

    combo = 0

    run = False


def cal_s_power() -> str:
    return f"{FUNC.divide(stage_total_s_power, total_spawn_s_power, 0) * 100:.2f} %"