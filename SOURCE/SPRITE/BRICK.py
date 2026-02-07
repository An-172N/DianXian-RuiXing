# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import os

import pygame

import PRELOAD
from LOGIC import Tool


class Brick(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    brick_dict = {
        f"C_BR_{(255, 128, 0)}": PRELOAD.brick_image.subsurface((0, 0, 15, 15)),
        f"C_BR_{(251, 234, 18)}": PRELOAD.brick_image.subsurface((45, 0, 15, 15)),
        f"C_BR_{(255, 255, 255)}": Tool.draw_circle((0, 0, 15, 15), 2, (255, 255, 255)).convert_alpha(),
        f"T_BR_{(0, 255, 0)}": PRELOAD.brick_image.subsurface((15, 0, 15, 15)),
        f"T_BR_{(255, 255, 255)}": PRELOAD.brick_image.subsurface((60, 0, 15, 15)),
        f"R_BR_{(128, 0, 128)}": PRELOAD.brick_image.subsurface((30, 0, 15, 15)),
        f"R_BR_{(255, 255, 255)}": Tool.draw_rectangle((15, 15), 2, (255, 255, 255)).convert_alpha()
    }

    def __init__(th, type: str, hp: int, color: tuple, pos: tuple):
        super().__init__()

        th.type = type
        th.color = color
        th.hp = hp

        th.have_power = False
        th.have_flash = False
        th.is_die = False

        th.image = th.get_type(type)
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def get_type(th, type: int) -> pygame.Surface:
        brick_dict = {
            0: lambda: Brick.brick_dict[f"T_BR_{th.color}"],
            1: lambda: Brick.brick_dict[f"R_BR_{th.color}"],
            2: lambda: Brick.brick_dict[f"C_BR_{th.color}"]
        }

        return brick_dict.get(type)()


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