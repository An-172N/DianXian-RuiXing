import random as rand
import math
import os

import pygame as pyg

import SCRIPT.DICT
import SCRIPT.VARIABLE as VARIABLE
import FUNC

from SCRIPT.LOGIC.FRIEND.BASE import Base


class Nre(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 256
        th.color = SCRIPT.DICT.color_dict[3]
        th.shape = 1
        th.current_angle = 0

        th.bomb = StraightThunder(th.color)

        th.original_image = pyg.image.load(os.path.join(SCRIPT.DICT.asset_path, 'IMG_NRE.png')).convert_alpha()
        th.image = th.original_image.subsurface(
            (
                0, 0,
                12, 26
            )
        )
        th.rect = th.image.get_rect()

        th.is_free = False

        th.target_x = 292
        th.target_y = 60
        th.timer = 0

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = rand.choice([150, 220, 292, 365, 435])

            th.bomb.bomb_cnt = 0
            th.bomb.bullet_cnt = 0
            th.bomb.timer = 0
            th.is_free = not th.is_free

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
            th.bomb.fire()
        else:
            th.bomb.free()


class StraightThunder:
    def __init__(th, color):
        th.color = color

        th.timer = 0
        th.bomb_cnt = 0
        th.bullet_cnt = 0

    def free(th) -> None:
        th.timer += 1

        if th.timer % 1 == 0 and th.bomb_cnt < 12:
            start_pos = (rand.randint(80, 500), 0, 0)
            end_pos = (rand.randint(100, 490), 360, 0)

            dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
            distance = math.hypot(dpos[0], dpos[1])

            sprite = Base(
                (2, distance, 0),
                (255, 255, 255),
                1
            )
            sprite.speed = 0
            x = start_pos[0] + dpos[0] / 2
            y = start_pos[1] + dpos[1] / 2
            sprite.rect.center = (x, y)
            sprite.current_angle = math.degrees(math.atan2(-dpos[0], -dpos[1]))
            sprite.update()
            VARIABLE.barrage_group.add(sprite)

            th.bomb_cnt += 1

    def fire(th) -> None:
        if th.bullet_cnt < 1:
            char_pos = VARIABLE.main_char.rect.center

            for i in range(char_pos[0] - 30, char_pos[0] + 31, 20):
                end_pos = (i, 360, 0)
                start_pos = (i, 0, 0)

                dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
                distance = math.hypot(dpos[0], dpos[1])

                sprite = Base(
                    (2, distance, 0),
                    (255, 255, 255),
                    1
                )
                sprite.speed = 0
                x = start_pos[0] + dpos[0] / 2
                y = start_pos[1] + dpos[1] / 2
                sprite.rect.center = (x, y)
                sprite.current_angle = 0
                sprite.update()
                VARIABLE.barrage_group.add(sprite)

            th.bullet_cnt += 1