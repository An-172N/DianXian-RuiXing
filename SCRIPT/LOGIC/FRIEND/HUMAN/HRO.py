import random as rand
import math

import pygame as pyg

import SCRIPT.DICT
import SCRIPT.VARIABLE
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

        th.orig_image = pyg.image.load('ASSET\IMG_HRO.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False

        th.tar_x = 292
        th.tar_y = 60
        th.ctr = 0

    def update(th):
        th.ctr += 1

        if th.ctr % 120 == 0:
            th.tar_x = rand.choice([150, 220, 292, 365, 435])

            th.bomb.bomb_cnt = 0
            th.bomb.bullet_cnt = 0
            th.bomb.dl = 0
            th.is_free = not th.is_free

        dir = (
                th.tar_x - th.rect.centerx,
                0
            )
        tar_pos = (th.tar_x, 60)
        two_pt = (tar_pos[0] - th.rect.centerx,
                  tar_pos[1] - th.rect.centery)
        dis = math.hypot(two_pt[0], two_pt[1])

        if dis < 4:
            th.rect.center = tar_pos
        else:
            if dis > 0:
                unit_direction = (dir[0] / dis,
                                  dir[1] / dis)
            pos = FUNC.Calculate.delta_tuple((th.rect.centerx, th.rect.centery, 0), (-(unit_direction[0] * 4), -(unit_direction[1] * 4), 0))
            th.rect.center = pos[:-1]

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

    def free(th, dx1, dx2, dy1, dy2):
        th.ctr += 1
        th.dl -= 3

        if th.ctr % 1 == 0 and th.bomb_cnt < 48:
            start_pos = (292 + dx1, 100 - dx2, 0)
            end_pos = (292 - dy1, 100 + dy2, 0)
        
            dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
            distance = math.hypot(dpos[0], dpos[1])
        
            if distance > 0:
                unit_dx = dpos[0] / distance
                unit_dy = dpos[1] / distance

            current_step = (th.bomb_cnt * 10)
            current_pos = FUNC.Calculate.delta_tuple(start_pos, (-(unit_dx * current_step), -(unit_dy * current_step), 0))
                
            for j in range(45, 136, 90):
                spr = Base((9, 9, 0), th.clr, 0)
                spr.spd = 4
                spr.rect.center = (current_pos[0], current_pos[1])
                spr.curr_ang = math.degrees(math.atan2(-dpos[0], -dpos[1])) + j + th.dl
                SCRIPT.VARIABLE.brg_grp.add(spr)
        
            th.bomb_cnt += 1

    def fire(th, rect):
        th.ctr += 1

        if th.ctr % 8 == 0 and th.bullet_cnt < 3:
            pos = rect.center
            char_pos = SCRIPT.VARIABLE.main_char.rect.center
            for i in range(-30, 31, 30):
                spr = Base((9, 9, 0), th.clr, 0)
                spr.spd = 4
                spr.rect.center = pos
                two_pt = FUNC.Calculate.delta_tuple((char_pos[0], char_pos[1], 0), (pos[0], pos[1], 0))
                spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1])) + i
                SCRIPT.VARIABLE.brg_grp.add(spr)

            th.bullet_cnt += 1