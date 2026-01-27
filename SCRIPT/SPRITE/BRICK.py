# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import os

import pygame

from SCRIPT import brick_image
from LOGIC import Rect


class Brick(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    brick_dict = {
        f"C_BR_{(255, 128, 0)}": brick_image.subsurface((0, 0, 15, 15)),
        f"C_BR_{(251, 234, 18)}": brick_image.subsurface((45, 0, 15, 15)),
        f"C_BR_{(255, 255, 255)}": brick_image.subsurface((60, 0, 15, 15)),
        f"T_BR_{(0, 255, 0)}": brick_image.subsurface((15, 0, 15, 15)),
        f"T_BR_{(255, 255, 255)}": brick_image.subsurface((75, 0, 15, 15)),
        f"R_BR_{(128, 0, 128)}": brick_image.subsurface((30, 0, 15, 15)),
        f"R_BR_{(255, 255, 255)}": Rect.Rect((15, 15), 2, (255, 255, 255)).image
    }

    def __init__(th, type: str, hp: int, color: tuple, pos: tuple):
        super().__init__()

        th.type = type
        th.color = color
        th.hp = hp

        th.have_power = False
        th.have_flash = False
        th.is_die = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)
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

    return None