# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import os


import pygame as pg


from LOGIC.FILE import *
from SCRIPT.HUMAN import Kli


class One:
    def __init__(th):
        th.plane_group = pg.sprite.Group()
        th.bullet_group = pg.sprite.Group()
        th.brick_group = pg.sprite.Group()
        th.item_group = pg.sprite.Group()
        th.barrage_group = pg.sprite.Group()
        th.particle_group = pg.sprite.Group()

        th.is_pause = False
        th.is_summary = False
        th.is_talk = False
        th.is_save = False
        th.is_check = False
        th.is_level_load = False
        th.is_exit = False

        th.major = Kli(th.bullet_group, th.particle_group, th.plane_group)
        th.char = None
        th.text = None

        th.item_spawn_timer = 0
        th.total_point = 0
        th.combo_timer = 120
        th.combo = 0
        th.text_number = 0
        th.text_part = 0
        th.pop_timer = 0


class Two:
    def __init__(th):
        th.is_run = False

        th.power = 0
        th.flash = 3
        th.unflash = 1
        th.score = 0
        th.flashed = 0
        th.game_total_point = 0
        th.stage = 1
        th.level = 1
        th.wait_load_timer = 0

        th.remaining_brick = []


class Log:
    def __init__(th):
        th.name = ''

        th.log = None

        th.json_files = get(f'{os.environ["USERPROFILE"]}/Saved Games/DX00')
        th.index = 0
        th.total_files = len(th.json_files)


def calculate_item_rate(number: int, condition: bool, critical: tuple) -> str:
    return f"{(number / (critical[0] if condition else critical[1])) * 100:.2f} %"


def score_summary(total_point: int, power: int, unflash: int, combo: int, numbers: tuple) -> int:
    return total_point * 512 + unflash * 4096 + ((2 ** combo) if combo > 0 else 0) + ((numbers[0] * 16384) if numbers[1] == 6 else 0) + ((int(power / 32 * 8192)) if numbers[1] == 6 else 0)


def combo_counter(timer: int, count: int, score: int, bonus: int, end: int) -> tuple:
    timer -= 1

    if timer <= 0:
        if count > 0:
            score += bonus
        count = 0
        timer = end

    return timer, count, score