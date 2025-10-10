import pygame as pyg
import random as rand

import TOOL
import BRICK


class Ono(pyg.sprite.Sprite):
    def __init__(th, proc):
        super().__init__()
        th.proc = proc

        th.hp = 96
        th.clr = th.proc("get", "main", "clr")[1]
        th.shape = 2
        th.curr_ang = 0

        th.bomb = BRICK.AutFroDiffuse(th.proc)

        th.is_free = False

        th.orig_image = pyg.image.load('AST\IMG_ONO.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()

        th.tar_x = 292
        th.tar_y = 60
        th.ctr = 0

    def update(th):
        th.ctr += 1

        if th.ctr % 180 == 0:
            th.tar_x = rand.choice([150, 292, 435])

            th.bomb.bomb_cnt = 0
            th.bomb.dl = 0
            th.is_free = not th.is_free

        TOOL.vec(th, th.tar_x, 60, 4)

        if not th.is_free:
            th.bomb.fire()
        else:
            th.bomb.free()