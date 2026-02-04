# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import itertools
import math

import pygame

from SCRIPT import SPRITE, char_image
from LOGIC import Tool, FUNC


class Ono(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group):
        super().__init__()

        th.group = group
        th.particle_group = particle_group

        th.hp = 192
        th.color = (255, 128, 0)

        th.image = char_image.subsurface((24, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False
        th.is_die = False
        th.can_shoot = False
        th.have_power = True
        th.have_flash = False

        th.point = None
        th.choice = None

        th.rect.center = (292, 60)
        th.target_x, th.target_y = 292, 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0
        th.particle_counter = 0

    def free(th) -> None:
        radians = math.radians
        barrage = SPRITE.Barrage.Barrage
        th.bullet_timer += 1

        if th.bullet_timer % 1 == 0 and th.bullet_counter < 8:
            th.bullet_delay += 6

            for i, j in itertools.product(
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 180),
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 90)
            ):
                pos = (th.rect.centerx + 32 * math.cos(radians(i)),th.rect.centery + 32 * math.sin(radians(i)))
                sprite = barrage(2, 3.5, th.color, j, pos)
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        barrage = SPRITE.Barrage.Barrage

        if th.bullet_counter < 1:
            for i in range(0, 360, 15):
                sprite = barrage(2, 4, th.color, i, th.rect.center)
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        radians = math.radians
        sin = math.sin
        cos = math.cos
        barrage = SPRITE.Barrage.Barrage
        th.timer += 1

        if th.timer % 120 == 0:
            rands = random.randint(0, 360)
            th.target_x, th.target_y = 292 + 50 * cos(radians(rands)), 110 + 50 * sin(radians(rands))

            th.bullet_counter = 0
            th.bullet_delay = 0
            th.particle_counter = 0
            th.can_shoot = True
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])
        if th.timer % 120 >= 99 and th.particle_counter <= 0:
            for i in range(0, 360, 15):
                pos = (th.rect.centerx + 64 * cos(radians(i)), th.rect.centery + 64 * sin(radians(i)))
                two_point = FUNC.add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                atan2 = math.atan2(-two_point[0], -two_point[1])
                current_angle = math.degrees(atan2)

                sprite = barrage(2, 4, (255, 255, 255), current_angle, pos)

                th.particle_group.add(sprite)

            th.particle_counter += 1
            th.point = SPRITE.Rect.Rect((2, 2), 0, (0, 0, 0), th.rect.center)

        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)

        th.rect.center = Tool.vector(th.rect.center, (th.target_x, th.target_y), 4)[0]

        if th.can_shoot:
            th.fire() if not th.is_free else th.choice()