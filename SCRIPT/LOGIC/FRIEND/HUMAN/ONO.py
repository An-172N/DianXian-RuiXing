import random as rand
import itertools
import math
import os

import pygame as pyg

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


class Ono(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 192
        th.color = DICT.color_dict[1]
        th.shape = 2
        th.current_angle = 0

        th.bomb = AutFroDiffuse(th.color)

        th.original_image = pyg.image.load(os.path.join(DICT.asset_path, 'IMG_ONO.png')).convert_alpha()
        th.image = th.original_image.subsurface(
            (
                0, 0,
                12, 26
            )
        )
        th.rect = th.image.get_rect()

        th.is_free = False
        th.choice = None

        th.target_x = 292
        th.target_y = 60
        th.timer = 0

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = rand.choice([150, 220, 292, 365, 435])

            th.bomb.bullet_cnt = 0
            th.bomb.dl = 0
            th.is_free = not th.is_free
            th.choice = rand.choice([th.bomb.fire, th.bomb.free])

        dir = pyg.math.Vector2(th.target_x - th.rect.centerx, 0)
        current_pos = pyg.math.Vector2(th.rect.centerx, th.rect.centery)
        target_pos = pyg.math.Vector2(th.target_x, 60)

        delta_vec = target_pos - current_pos
        distance = delta_vec.length()

        if distance < 4:
            th.rect.center = target_pos
        else:
            if distance > 0:
                dir.normalize_ip()

            new_pos = current_pos + dir * 4
            th.rect.center = new_pos

        if not th.is_free:
            th.bomb.fire(th.rect)
        else:
            th.choice(th.rect)


class AutFroDiffuse:
    def __init__(th, color):
        th.color = color

        th.bullet_cnt = 0
        th.timer = 0
        th.dl = 0

    def free(th, rect) -> None:
        th.timer += 1

        if (
            th.timer % 1 == 0 and
            th.bullet_cnt < 12
        ):
            th.dl += 6

            for i, j in itertools.product(
                range(0 + th.dl, 360 + th.dl, 180),
                range(0 + th.dl, 360 + th.dl, 90)
            ):
                x = rect.centerx + 32 * math.cos(math.radians(i))
                y = rect.centery + 32 * math.sin(math.radians(i))
                pos = (x, y)
                sprite = Base(
                    (9, 9, 0),
                    th.color,
                    2
                )
                sprite.speed = 3.5
                sprite.rect.center = pos
                sprite.current_angle = j
                VARIABLE.barrage_group.add(sprite)

            th.bullet_cnt += 1

    def fire(th, rect) -> None:
        if th.bullet_cnt < 1:
            pos = rect.center
            for i in range(0, 360, 15):
                sprite = Base(
                    (9, 9, 0),
                    th.color,
                    2
                )
                sprite.speed = 4
                sprite.rect.center = pos
                sprite.current_angle = i
                VARIABLE.barrage_group.add(sprite)

            th.bullet_cnt += 1