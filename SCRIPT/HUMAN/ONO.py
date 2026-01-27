# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import itertools
import math

import pygame

from SCRIPT import SPRITE, char_image
from LOGIC import Tool


class Ono(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group):
        super().__init__()

        th.group = group

        th.hp = 192
        th.color = (255, 128, 0)

        th.image = char_image.subsurface((24, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False
        th.is_die = False
        th.have_power = True
        th.have_flash = False
        th.choice = None

        th.rect.center = (292, 60)
        th.target_x = 292
        th.target_y = 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 1 == 0 and th.bullet_counter < 8:
            th.bullet_delay += 6

            for i, j in itertools.product(
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 180),
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 90)
            ):
                x = th.rect.centerx + 32 * math.cos(math.radians(i))
                y = th.rect.centery + 32 * math.sin(math.radians(i))
                sprite = SPRITE.Barrage.Barrage(2, 3.5, th.color, j, (x, y))
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            for i in range(0, 360, 15):
                sprite = SPRITE.Barrage.Barrage(2, 4, th.color, i, th.rect.center)
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            rands = random.randint(0, 360)
            th.target_x = 292 + 50 * math.cos(math.radians(rands))
            th.target_y = 110 + 50 * math.sin(math.radians(rands))

            th.bullet_counter = 0
            th.bullet_delay = 0
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])

        th.rect.center = Tool.vector(th.rect.center, (th.target_x, th.target_y), 4)[0]

        th.fire() if not th.is_free else th.choice()