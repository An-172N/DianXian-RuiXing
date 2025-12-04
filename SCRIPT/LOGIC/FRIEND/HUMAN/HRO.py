import random as rand
import math
import os

import pygame as pyg

import SCRIPT.DICT
import VARIABLE
import FUNC

from ..BASE import Base


class Hro(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 448
        th.clr = SCRIPT.DICT.clr_dict[2]
        th.shape = 0
        th.curr_ang = 0

        th.bomb = PolyX(th.clr)

        th.orig_image = pyg.image.load(os.path.join(VARIABLE.asset_path, 'IMG_HRO.png')).convert_alpha()
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
            th.bomb.dl = 0
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
            th.bomb.fire(th.rect)
        else:
            th.bomb.free(140, 140, 140, 140)
            th.bomb.free(-140, 140, -140, 140)


class PolyX:
    def __init__(th, clr):
        th.clr = clr

        th.bomb_cnt = 0
        th.bullet_cnt = 0
        th.ctr = 0
        th.dl = 0

    def free(th, dx1, dx2, dy1, dy2) -> None:
        th.ctr += 1
        th.dl -= 3

        if th.ctr % 1 == 0 and th.bomb_cnt < 48:
            start_pos = pyg.math.Vector2(292 + dx1, 100 - dx2)
            end_pos = pyg.math.Vector2(292 - dy1, 100 + dy2)

            delta_pos = end_pos - start_pos
            distance = delta_pos.length()

            if distance > 0:
                delta_pos.normalize_ip()

            current_step = th.bomb_cnt * 10
            current_pos = start_pos + delta_pos * current_step
                
            for j in range(45, 136, 90):
                spr = Base((9, 9, 0), th.clr, 0)
                spr.spd = 4
                spr.rect.center = (current_pos.x, current_pos.y)
                spr.curr_ang = math.degrees(math.atan2(-delta_pos.x, -delta_pos.y)) + j + th.dl
                VARIABLE.brg_grp.add(spr)
        
            th.bomb_cnt += 1

    def fire(th, rect) -> None:
        th.ctr += 1

        if th.ctr % 8 == 0 and th.bullet_cnt < 3:
            pos = rect.center
            char_pos = VARIABLE.main_char.rect.center
            for i in range(-30, 31, 30):
                spr = Base((9, 9, 0), th.clr, 0)
                spr.spd = 4
                spr.rect.center = pos
                two_pt = FUNC.Calculate.delta_tuple((char_pos[0], char_pos[1], 0), (pos[0], pos[1], 0))
                spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1])) + i
                VARIABLE.brg_grp.add(spr)

            th.bullet_cnt += 1