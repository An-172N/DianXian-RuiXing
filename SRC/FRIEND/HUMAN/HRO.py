import random as rand
import math

import pygame as pyg

import DICT
import FUNC
from ..BASE import Base


class Hro(pyg.sprite.Sprite):
    def __init__(th, own):
        super().__init__()
        th.stg_mgr = own

        th.hp = 384
        th.clr = DICT.clr_dict[2]
        th.shape = 0
        th.curr_ang = 0

        th.bomb = PolyX(th)

        th.orig_image = pyg.image.load('AST\IMG_HRO.png').convert_alpha()
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
            th.rect.center = FUNC.Calculate.delta_position(th.rect.center, (-(unit_direction[0] * 4), -(unit_direction[1] * 4)))

        if not th.is_free:
            th.bomb.fire()
        else:
            th.bomb.free()


class PolyX:
    def __init__(th, own):
        th.char = own

        th.bomb_cnt = 0
        th.bullet_cnt = 0
        th.ctr = 0
        th.dl = 0

    def free(th):
        th.ctr += 1
        th.dl -= 6

        if th.ctr % 1 == 0 and th.bomb_cnt < 24:
            start_pos = (292 + 140, 100 - 140)
            end_pos = (292 - 140, 100 + 140)
        
            dpos = FUNC.Calculate.delta_position(end_pos, start_pos)
            distance = math.hypot(dpos[0], dpos[1])
        
            if distance > 0:
                unit_dx = dpos[0] / distance
                unit_dy = dpos[1] / distance

            current_step = (th.bomb_cnt * 20)
            current_pos = FUNC.Calculate.delta_position(start_pos, (-(unit_dx * current_step), -(unit_dy * current_step)))
                
            for j in range(45, 136, 90):
                spr = Base((9, 9, 0), th.char.clr, 0)
                spr.spd = 4
                spr.rect.center = (current_pos[0], current_pos[1])
                spr.curr_ang = math.degrees(math.atan2(-dpos[0], -dpos[1])) + j + th.dl
                th.char.stg_mgr.own.brg_grp.add(spr)

            start_pos = (292 - 140, 100 - 140)
            end_pos = (292 + 140, 100 + 140)
        
            dpos = FUNC.Calculate.delta_position(end_pos, start_pos)
            distance = math.hypot(dpos[0], dpos[1])
        
            if distance > 0:
                unit_dx = dpos[0] / distance
                unit_dy = dpos[1] / distance

            current_step = (th.bomb_cnt * 20)
            current_pos = FUNC.Calculate.delta_position(start_pos, (-(unit_dx * current_step), -(unit_dy * current_step)))
                
            for j in range(45, 136, 90):
                spr = Base((9, 9, 0), th.char.clr, 0)
                spr.spd = 4
                spr.rect.center = (current_pos[0], current_pos[1])
                spr.curr_ang = math.degrees(math.atan2(-dpos[0], -dpos[1])) + j + th.dl
                th.char.stg_mgr.own.brg_grp.add(spr)
        
            th.bomb_cnt += 1

    def fire(th):
        if th.bullet_cnt < 1:
            pos = th.char.rect.center
            char_pos = th.char.stg_mgr.own.pln_mgr.char.rect.center
            for i in range(-30, 31, 30):
                spr = Base((9, 9, 0), th.char.clr, 0)
                spr.spd = 4
                spr.rect.center = pos
                two_pt = FUNC.Calculate.delta_position(char_pos, pos)
                spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1])) + i
                th.char.stg_mgr.own.brg_grp.add(spr)

            th.bullet_cnt += 1