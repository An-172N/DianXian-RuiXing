# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import random, sample


import pygame as pg


from PRELOAD import brick_cache, color_dict
from LOGIC.SPRITE import Base


class Brick(Base):
    __slots__ = ('color', 'hp', 'power', 'flash', 'is_die')

    def __init__(th, form: str, hp: int, color: tuple, pos: tuple, image: pg.Surface, group: pg.sprite.Group):
        super().__init__(form, image, group, pos=pos)

        th.color = color
        th.hp = hp
        th.power = False
        th.flash = False
        th.is_die = False


def load_brick(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple, group: pg.sprite.Group):
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if random() >= rate else color_dict[6]

            Brick(shape, hp, c, (size[0] + i * interval[0], size[1] + row * interval[1]), brick_cache[(shape, c)], group)


def choose_brick(group: pg.sprite.Group, numbers: tuple, basic_power: int, basic_flash: int):
    brick_list = list(group)
    choose_power = sample(range(len(brick_list)), basic_power + numbers[0] + numbers[1])
    choose_flash = sample(range(len(brick_list)), basic_flash)

    for i in choose_power:
        brick_list[i].power = True
    for j in choose_flash:
        brick_list[j].flash = True


def boss_lose(part: int) -> tuple:
    part += 1
    number = 0
    is_talk = True
    pop_time = 0

    return part, number, is_talk, pop_time