# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame as pg


from PRELOAD import picture


is_run = False
is_pause = False
is_summary = False
is_talk = False
is_save = False
is_level_load = False


pop_time = 0


name = ''


power = 0
shoot_count = 0


is_shoot = True


item_spawn_time = 0
combo_time = 120
combo = 0


flash = 3
no_flash = 0
score = 0
cooldown_time = 0
use_flash = 0
total_power = 0
game_total_power = 0


is_move_right = False
is_move_left = False
is_fast = False
is_visitable = True
is_divide = False
is_collide = True


text_number = 0
text_part = 0
stage = 1
level = 1


backdrop = picture[6]
second_backdrop = picture[stage]


char = None
text = None
major = None
decision_point = None


plane_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
brick_group = pg.sprite.Group()
item_group = pg.sprite.Group()
barrage_group = pg.sprite.Group()
particle_group = pg.sprite.Group()
text_group = pg.sprite.Group()


last_time = pg.time.get_ticks()
fps_text = last_time


def calculate_item_rate(number: int, condition: bool, critical: tuple) -> str:
    return f"{(number / (critical[0] if condition else critical[1])) * 100:.2f} %"


def score_summary(power: int, unflash: int, combo: int, collection: tuple) -> int:
    return power * collection[0] + unflash * collection[1] + ((collection[2] ** combo) if combo > 0 else 0)