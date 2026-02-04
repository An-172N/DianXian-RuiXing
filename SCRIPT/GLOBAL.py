# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import os

import pygame

from SCRIPT import HUMAN, SPRITE
from LOGIC import FUNC, Tool


asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')
font = pygame.font.Font(os.path.join(asset_path, 'FONT\FONT_GNUUNIFONT.otf'), 15)
icon = pygame.display.set_icon(pygame.image.load(os.path.join(asset_path, '..\ICON.ico')))


color_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    4: (251, 234, 18),
    5: (45, 194, 229)
}


barrage_rate = [0.17 + (FUNC.fibonacci(0, 1, i) / 100) for i in range(4, 8)]


window = pygame.Rect(120, 15, 345, 330)
effective = pygame.Rect(70, -50, 410, 410)


is_run = False
is_pause = False
is_summary = False
is_talk = False
is_save = False
is_level_load = False
is_blit = False


name = ''


power = 0
shoot_counter = 0


is_shoot = True


item_spawn_timer = 0
combo_timer = 120
combo = 0


flash = 3
no_flash = 0
score = 0
cooldown_timer = 0
use_flash = 0
total_power = 0
stage_total_power = 0


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
    1: pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_STAGE1BG.png')).convert_alpha(),
    2: pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_STAGE2BG.png')).convert_alpha(),
    3: pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_STAGE3BG.png')).convert_alpha(),
    4: pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_STAGE4BG.png')).convert_alpha(),
    "GAME_BG": pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_GAMEBG.png')).convert_alpha(),
    "MENU_BG": Tool.draw_rectangle((345, 330), 0, (0, 0, 0))
}


background = picture["GAME_BG"]
second_background = Tool.change_background(picture[stage], 128)


char = None
text = None


plane_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
barrage_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()


main_char = HUMAN.Kli(bullet_group, particle_group)
decision_point = SPRITE.Rect.Rect((2, 2), 0, (128, 128, 128))


last_time = pygame.time.get_ticks()
fps_text = last_time