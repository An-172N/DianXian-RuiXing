# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame as pg


is_run = False
is_pause = False
is_summary = False
is_talk = False
is_save = False
is_level_load = False


pop_time = 0
wait_load_time = 0


name = ''


power = 0


item_spawn_time = 0
combo_time = 120
combo = 0


flash = 3
no_flash = 0
score = 0
use_flash = 0
total_power = 0
game_total_power = 0


text_number = 0
text_part = 0
stage = 1
level = 1


char = None
text = None
major = None


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


def score_summary(total_power: int, power: int, unflash: int, combo: int, numbers: tuple) -> int:
    return total_power * 512 + unflash * 4096 + ((2 ** combo) if combo > 0 else 0) + ((numbers[0] * 16384) if numbers[1] == 6 else 0) + ((int(power / 32 * 8192)) if numbers[1] == 6 else 0)