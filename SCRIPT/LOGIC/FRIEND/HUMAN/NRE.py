import random as rand
import math
import os

import pygame as pyg

import SCRIPT.DICT
import VARIABLE
import FUNC

from ..BASE import Base


class Nre(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 448
        th.clr = SCRIPT.DICT.clr_dict[3]
        th.shape = 1
        th.curr_ang = 0

        th.bomb = StraightThunder(th.clr)

        th.orig_image = pyg.image.load(os.path.join(VARIABLE.asset_path, 'IMG_NRE.png')).convert_alpha()
        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False

        th.tar_x = 292
        th.tar_y = 60
        th.ctr = 0

    def update(th) -> None:
        th.ctr += 1

        if th.ctr % 120 == 0:
            th.tar_x = rand.choice([150, 220, 292, 365, 435])

            th.bomb.bomb_cnt = 0
            th.bomb.bullet_cnt = 0
            th.bomb.ctr = 0
            th.is_free = not th.is_free

        dir = pyg.math.Vector2(th.tar_x - th.rect.centerx, 0)
        current_pos = pyg.math.Vector2(th.rect.centerx, th.rect.centery)
        target_pos = pyg.math.Vector2(th.tar_x, 60)

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
    def __init__(th, clr):
        th.clr = clr

        th.ctr = 0
        th.bomb_cnt = 0
        th.bullet_cnt = 0

    def free(th) -> None:
        th.ctr += 1

        if th.ctr % 1 == 0 and th.bomb_cnt < 24:
            start_pos = (rand.randint(80, 500), 0, 0)
            end_pos = (rand.randint(100, 490), 360, 0)
        
            dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
            distance = math.hypot(dpos[0], dpos[1])
                
            spr = Base((2, distance, 0), (255, 255, 255), 1)
            spr.spd = 0
            spr.rect.center = (start_pos[0] + dpos[0] / 2, start_pos[1] + dpos[1] / 2)
            spr.curr_ang = math.degrees(math.atan2(-dpos[0], -dpos[1]))
            spr.update()
            VARIABLE.brg_grp.add(spr)

            th.bomb_cnt += 1

    def fire(th) -> None:
        if th.bullet_cnt < 1:
            char_pos = VARIABLE.main_char.rect.center

            for i in range(char_pos[0] - 30, char_pos[0] + 31, 20):
                end_pos = (i, 360, 0)
                start_pos = (i, 0, 0)

                dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
                distance = math.hypot(dpos[0], dpos[1])

                spr = Base((2, distance, 0), (255, 255, 255), 1)
                spr.spd = 0
                spr.rect.center = (start_pos[0] + dpos[0] / 2, start_pos[1] + dpos[1] / 2)
                spr.curr_ang = 0
                spr.update()
                VARIABLE.brg_grp.add(spr)

            th.bullet_cnt += 1