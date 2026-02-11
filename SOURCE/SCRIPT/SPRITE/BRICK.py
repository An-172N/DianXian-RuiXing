# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random

import pygame

import PRELOAD


class Brick(pygame.sprite.Sprite):
    def __init__(th, type: str, hp: int, color: tuple, pos: tuple):
        super().__init__()

        th.type = type
        th.color = color
        th.hp = hp

        th.have_power = False
        th.have_flash = False
        th.is_die = False

        th.image = PRELOAD.brick_cache[f"{th.type}_{th.color}"]
        th.rect = th.image.get_rect()

        th.rect.center = pos


def load_brick(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple, group: pygame.sprite.Group) -> None:
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if random.random() >= rate else (255, 255, 255)
            brick = Brick(shape, hp, c, (size[0] + i * interval[0], size[1] + row * interval[1]))

            group.add(brick)


def choose_brick(group: pygame.sprite.Group, stage_level: tuple, basic_power: int, basic_flash: int) -> None:
    sample = random.sample
    brick_list = list(group)
    choose_power = sample(range(len(brick_list)), basic_power + stage_level[0] + stage_level[1])
    choose_flash = sample(range(len(brick_list)), basic_flash)
    
    for i in choose_power:
        brick_list[i].have_power = True
    for j in choose_flash:
        brick_list[j].have_flash = True


def boss_lose(part: int, number: int, is_talk: bool, is_blit: bool) -> tuple:
    part += 1
    number = 0

    is_talk = True
    is_blit = False

    return part, number, is_talk, is_blit