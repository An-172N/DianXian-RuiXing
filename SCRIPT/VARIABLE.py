import os

import pygame

import SCRIPT.DICT as DICT
import FUNC

from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import DecPt


window = pygame.Rect(
    (
        120, 15,
        345, 330
    )
)
effective = pygame.Rect(
    (
        105, 0,
        375, 360
    )
)
plane_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
barrage_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
run = False
pause = False
summary = False
talk = False
save = False
level_load = False
is_reset = False

background = pygame.image.load(os.path.join(DICT.asset_path, 'IMG_GAMEBG.png')).convert_alpha()
last_time = pygame.time.get_ticks()
fps_text = last_time

name = ''

s_power = 0
shoot_cnt = 0
can_shoot = True

item_spawn_timer = 0
comboo_timer = 90
combo = 0

player = 4
no_hurt = 0
score = 0
cooldown_time = 0
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
main_char = DICT.char_dict.get(5)()
d_pt = DecPt()

text_number = 0
text_part = 0
timer = 0
stage = 1
level = 0
picture_list = [
    (1, os.path.join(DICT.asset_path, 'IMG_STAGE1BG.png')),
    (2, os.path.join(DICT.asset_path, 'IMG_STAGE2BG.png')),
    (3, os.path.join(DICT.asset_path, 'IMG_STAGE3BG.png')),
    (4, os.path.join(DICT.asset_path, 'IMG_STAGE4BG.png')),
]
picture = FUNC.Process.load_files(picture_list, lambda f: pygame.image.load(f).convert_alpha())
second_background = picture[stage]
second_background.set_alpha(159)
char = None
text = None


def cal_s_power() -> str:
    return f"{FUNC.Calculate.divide(stage_total_s_power, total_spawn_s_power, 0) * 100:.2f} %"