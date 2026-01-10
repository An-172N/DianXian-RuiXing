# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import random
import math

import pygame

import SCRIPT.GLOBAL as GLOBAL
import SCRIPT.FUNC as FUNC


class Qdi(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 192
        th.color = GLOBAL.color_dict[4]
        th.shape = 2
        th.current_angle = 0

        th.original_image = GLOBAL.char_image["Qdi"]
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False
        th.choice = None

        th.target_x = 292
        th.target_y = 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 1:
            for _ in range(48):
                x = random.randint(120, 465)
                y = random.randint(15, 250)
                pos = (x, y)
                sprite = GLOBAL.char_dict[7](color=th.color, shape=2, type="barrage")
                sprite.speed = 4
                sprite.rect.center = pos
                sprite.current_angle = random.randint(0, 360)
                GLOBAL.barrage_group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 6 and th.bullet_timer % 2 == 0:
            char = GLOBAL.main_char
            sprite = GLOBAL.char_dict[7](color=th.color, shape=2, type="barrage")
            sprite.speed = 3.5
            sprite.rect.center = (random.randint(120, 465), random.randint(15, 255))
            x1 = char.rect.centerx
            x2 = sprite.rect.centerx
            y1 = char.rect.centery
            y2 = sprite.rect.centery
            two_pt = FUNC.delta((x1, y1), (x2, y2))
            sprite.current_angle = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
            GLOBAL.barrage_group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 150 == 0:
            th.target_x = random.choice([150, 220, 292, 365, 435])
            th.bullet_counter = 0
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])

        th.rect.center = (th.target_x, th.target_y)

        th.fire() if not th.is_free else th.choice()