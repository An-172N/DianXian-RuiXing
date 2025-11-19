import random as rand
import math

import pygame as pyg

import DICT
import FUNC
from ..BASE import Base


class Nre(pyg.sprite.Sprite):
    def __init__(th, own):
        super().__init__()
        th.stg_mgr = own

        th.hp = 384
        th.clr = DICT.clr_dict[3]
        th.shape = 1
        th.curr_ang = 0

        th.bomb = StraightThunder(th)

        th.orig_image = pyg.image.load('AST\IMG_NRE.png').convert_alpha()
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
            th.bomb.ctr = 0
            th.bomb.blt_ctr = 0
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
            pos = FUNC.Calculate.delta_tuple((th.rect.centerx,th.rect.centery, 0), (-(unit_direction[0] * 4), -(unit_direction[1] * 4), 0))
            th.rect.center = pos[:-1]

        if not th.is_free:
            th.bomb.fire()
        else:
            th.bomb.free()


class StraightThunder:
    def __init__(th, own):
        th.char = own

        th.ctr = 0
        th.bomb_cnt = 0
        th.bullet_cnt = 0
        th.blt_ctr = 0

    def free(th):
        th.ctr += 1

        if th.ctr % 1 == 0 and th.bomb_cnt < 1:
            for _ in range(16):
                start_pos = (rand.randint(100, 480), 0, 0)
                end_pos = (rand.randint(100, 490), 360, 0)
        
                dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
                distance = math.hypot(dpos[0], dpos[1])
                
                spr = Base((2, distance, 0), (255, 255, 255), 1)
                spr.spd = 0
                spr.rect.center = (start_pos[0] + dpos[0] / 2, start_pos[1] + dpos[1] / 2)
                spr.curr_ang = math.degrees(math.atan2(-dpos[0], -dpos[1]))
                spr.update()
                th.char.stg_mgr.own.brg_grp.add(spr)

            th.bomb_cnt += 1

        if th.ctr >= 45:
            for i in th.char.stg_mgr.own.brg_grp:
                i.clr = DICT.clr_dict[3]
                temp_surface = pyg.Surface(i.image.get_size(), pyg.SRCALPHA)
                temp_surface.fill(i.clr)

                i.image.blit(temp_surface, (0, 0), special_flags=pyg.BLEND_RGBA_MIN)
        if th.ctr >= 90:
            for i in th.char.stg_mgr.own.brg_grp:
                i.kill()

    def fire(th):
        th.blt_ctr += 1

        if th.bullet_cnt < 1:
            char_pos = th.char.stg_mgr.own.pln_mgr.char.rect.center

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
                th.char.stg_mgr.own.brg_grp.add(spr)

            th.bullet_cnt += 1

        if th.blt_ctr >= 45:
            for i in th.char.stg_mgr.own.brg_grp:
                i.clr = DICT.clr_dict[3]
                temp_surface = pyg.Surface(i.image.get_size(), pyg.SRCALPHA)
                temp_surface.fill(i.clr)

                i.image.blit(temp_surface, (0, 0), special_flags=pyg.BLEND_RGBA_MIN)
        if th.blt_ctr >= 90:
            for i in th.char.stg_mgr.own.brg_grp:
                i.kill()