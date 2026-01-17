# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import os

import pygame

from SCRIPT import LOGIC, FUNC


asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')
font = pygame.font.Font(os.path.join(asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)
icon = pygame.display.set_icon(pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_ICON.png')))


color_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    4: (251, 234, 18),
    5: (45, 194, 229)
}


fibonacci_list = [FUNC.fibonacci(0, 1, i) / 100 for i in range(3, 7)]


window = pygame.Rect((120, 15, 345, 330))
effective = pygame.Rect(105, -50, 375, 410)


is_run = False
is_pause = False
is_summary = False
is_talk = False
is_save = False
is_level_load = False
is_blit = False


name = ''


s_power = 0
shoot_counter = 0


is_shoot = True


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


is_move_right = False
is_move_left = False
is_fast = False
is_visitable = True
is_s_divide = False
is_collide = True


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
        (f"T_BA_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_TRIANGLEBARRAGEGREEN.png')),
        (f"T_BA_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_TRIANGLEBARRAGEWHITE.png')),
        (f"C_BR_{color_dict[1]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKORANGE.png')),
        (f"C_BR_{color_dict[4]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKYELLOW.png')),
        (f"C_BR_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKWHITE.png')),
        (f"T_BR_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_TRIANGLEBRICKGREEN.png')),
        (f"T_BR_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_TRIANGLEBRICKWHITE.png')),
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
second_background.set_alpha(191)


char = None
text = None


main_char = LOGIC.Kli()
decision_point = LOGIC.DecisionPoint()


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