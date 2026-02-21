# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import random, sample


import pygame


from PRELOAD import brick_cache, color_dict
from LOGIC.SPRITE import Base


class Brick(Base):
    __slots__ = ('color', 'hp', 'have_power', 'have_flash', 'is_die')

    def __init__(th, form: str, hp: int, color: tuple, pos: tuple, image: pygame.Surface):
        super().__init__(form, image, pos=pos)

        th.color = color
        th.hp = hp

        th.have_power = False
        th.have_flash = False
        th.is_die = False

    def add_power(th) -> None:
        th.have_power = True

    def add_flash(th) -> None:
        th.have_flash = True

    def death(th) -> None:
        th.is_die = True


def load_brick(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple, group: pygame.sprite.Group) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if random() >= rate else color_dict[6]
            brick = Brick(shape, hp, c, (size[0] + i * interval[0], size[1] + row * interval[1]), brick_cache[f"{shape}_{c}"])

            group.add(brick)


def choose_brick(group: pygame.sprite.Group, stage_level: tuple, basic_power: int, basic_flash: int) -> None:
    brick_list = list(group)
    choose_power = sample(range(len(brick_list)), basic_power + stage_level[0] + stage_level[1])
    choose_flash = sample(range(len(brick_list)), basic_flash)

    for i in choose_power:
        brick_list[i].add_power()
    for j in choose_flash:
        brick_list[j].add_flash()


def boss_lose(part: int) -> tuple:
    part += 1
    number = 0
    is_talk = True
    animate_timer = 0

    return part, number, is_talk, animate_timer