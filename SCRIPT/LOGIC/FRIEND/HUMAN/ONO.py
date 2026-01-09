# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import random
import itertools
import math

import pygame

import SCRIPT.GLOBAL as GLOBAL


class Ono(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 192
        th.color = GLOBAL.color_dict[1]
        th.shape = 2
        th.current_angle = 0

        th.original_image = GLOBAL.char_image["Ono"]
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False
        th.choice = None

        th.target_x = 292
        th.target_y = 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 1 == 0 and th.bullet_counter < 12:
            th.bullet_delay += 6

            for i, j in itertools.product(
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 180),
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 90)
            ):
                x = th.rect.centerx + 32 * math.cos(math.radians(i))
                y = th.rect.centery + 32 * math.sin(math.radians(i))
                pos = (x, y)
                sprite = GLOBAL.char_dict[7](color=th.color, shape=2, type="barrage")
                sprite.speed = 3.5
                sprite.rect.center = pos
                sprite.current_angle = j
                GLOBAL.barrage_group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            pos = th.rect.center
            for i in range(0, 360, 15):
                sprite = GLOBAL.char_dict[7](color=th.color, shape=2, type="barrage")
                sprite.speed = 4
                sprite.rect.center = pos
                sprite.current_angle = i
                GLOBAL.barrage_group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = random.choice([150, 220, 292, 365, 435])

            th.bullet_counter = 0
            th.bullet_delay = 0
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])

        GLOBAL.char_dict[7].vector(th, 4)

        th.fire() if not th.is_free else th.choice()