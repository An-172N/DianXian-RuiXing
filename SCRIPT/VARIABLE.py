import os

import pygame

import SCRIPT.DICT as DICT
import SCRIPT.FUNC as FUNC


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

picture_list = [
    (1, os.path.join(DICT.asset_path, 'IMAGE\IMG_STAGE1BG.png')),
    (2, os.path.join(DICT.asset_path, 'IMAGE\IMG_STAGE2BG.png')),
    (3, os.path.join(DICT.asset_path, 'IMAGE\IMG_STAGE3BG.png')),
    (4, os.path.join(DICT.asset_path, 'IMAGE\IMG_STAGE4BG.png')),
    ("GAME_BG", os.path.join(DICT.asset_path, 'IMAGE\IMG_GAMEBG.png')),
    ("MENU_BG", os.path.join(DICT.asset_path, 'IMAGE\IMG_MENU.png'))
]
char_image_list = [
    ("Kli", os.path.join(DICT.asset_path, 'IMAGE\IMG_KLI.png')),
    ("Ono", os.path.join(DICT.asset_path, 'IMAGE\IMG_ONO.png')),
    ("Hro", os.path.join(DICT.asset_path, 'IMAGE\IMG_HRO.png')),
    ("Nre", os.path.join(DICT.asset_path, 'IMAGE\IMG_NRE.png')),
    ("Qdi", os.path.join(DICT.asset_path, 'IMAGE\IMG_QDI.png'))
]
sprite_image_list = [
    (f"C_BA_{DICT.color_dict[1]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_CIRCLEBARRAGEORANGE.png')),
    (f"C_BA_{DICT.color_dict[4]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_CIRCLEBARRAGEYELLOW.png')),
    (f"C_BA_{DICT.color_dict[6]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_CIRCLEBARRAGEWHITE.png')),
    (f"P_BA_{DICT.color_dict[2]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_POLYGONBARRAGEGREEN.png')),
    (f"P_BA_{DICT.color_dict[6]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_POLYGONBARRAGEWHITE.png')),
    (f"C_BR_{DICT.color_dict[1]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_CIRCLEBRICKORANGE.png')),
    (f"C_BR_{DICT.color_dict[4]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_CIRCLEBRICKYELLOW.png')),
    (f"C_BR_{DICT.color_dict[6]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_CIRCLEBRICKWHITE.png')),
    (f"P_BR_{DICT.color_dict[2]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_POLYGONBRICKGREEN.png')),
    (f"P_BR_{DICT.color_dict[6]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_POLYGONBRICKWHITE.png')),
    (f"R_BR_{DICT.color_dict[3]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_RECTANGLEBRICKPURPLE.png')),
    (f"R_BR_{DICT.color_dict[6]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_RECTANGLEBRICKWHITE.png')),
    (f"R_IT_{DICT.color_dict[2]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_ITEMGREEN.png')),
    (f"R_IT_{DICT.color_dict[5]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_ITEMBLUE.png')),
    (f"R_IT_{DICT.color_dict[6]}", os.path.join(DICT.asset_path, f'IMAGE\IMG_ITEMWHITE.png')),
    ("KLI_BULLET", os.path.join(DICT.asset_path, f'IMAGE\IMG_KLIBULLET.png')),
    ("KLI_BOMB", os.path.join(DICT.asset_path, f'IMAGE\IMG_KLIBOMB.png')),
    ("DEC", os.path.join(DICT.asset_path, f'IMAGE\IMG_DECISIONPOINT.png')),
]

run = False
pause = False
summary = False
talk = False
save = False
level_load = False

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

text_number = 0
text_part = 0
timer = 0
stage = 1
level = 0

picture = FUNC.Process.load_files(picture_list, lambda f: pygame.image.load(f).convert_alpha())
char_image = FUNC.Process.load_files(char_image_list, lambda f: pygame.image.load(f).convert_alpha())
sprite_image = FUNC.Process.load_files(sprite_image_list, lambda f: pygame.image.load(f).convert_alpha())
background = picture["GAME_BG"]
second_background = picture[stage]

char = None
text = None

main_char = DICT.char_dict.get(5)()
decision_point = DICT.char_dict.get(6)()


def reset1() -> None:
    global pause, summary, talk, save, level_load
    global collide, is_s_divide, cooldown_time, total_s_power
    global shoot_counter, can_shoot
    global item_spawn_timer
    global text_number, text_part
    
    pause = False
    summary = False
    talk = False
    save = False
    level_load = False

    item_group.empty(),
    brick_group.empty(),
    plane_group.empty(),
    bullet_group.empty(),
    particle_group.empty(),
    barrage_group.empty()

    collide = False
    is_s_divide = False
    cooldown_time = 0
    main_char.bomb.bomb_counter = 0
    main_char.bomb.timer = 0
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
    return f"{FUNC.Calculate.divide(stage_total_s_power, total_spawn_s_power, 0) * 100:.2f} %"