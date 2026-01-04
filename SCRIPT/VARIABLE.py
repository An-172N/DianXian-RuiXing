import pygame

import SCRIPT.TABLE as TABLE
import SCRIPT.FUNC as FUNC


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

picture = FUNC.Process.load_files(TABLE.picture_list, lambda f: pygame.image.load(f).convert_alpha())
char_image = FUNC.Process.load_files(TABLE.char_image_list, lambda f: pygame.image.load(f).convert_alpha())
sprite_image = FUNC.Process.load_files(TABLE.sprite_image_list, lambda f: pygame.image.load(f).convert_alpha())

background = picture["GAME_BG"]
second_background = picture[stage]

char = None
text = None

main_char = TABLE.char_dict.get(5)()
decision_point = TABLE.char_dict.get(6)()


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

    TABLE.item_group.empty(),
    TABLE.brick_group.empty(),
    TABLE.plane_group.empty(),
    TABLE.bullet_group.empty(),
    TABLE.particle_group.empty(),
    TABLE.barrage_group.empty()

    collide = False
    is_s_divide = False
    cooldown_timer = 0
    main_char = TABLE.char_dict.get(5)()
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