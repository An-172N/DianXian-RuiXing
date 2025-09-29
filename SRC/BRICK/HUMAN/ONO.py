import pygame as pyg

from LOGIC.TOOL import mv


class Ono(pyg.sprite.Sprite):
    def __init__(th, own):
        super().__init__()
        th.stg_mgr = own

        th.hp = 96
        th.clr = (255, 128, 0)
        th.shape = 2
        th.curr_ang = 0

        th.orig_image = pyg.image.load('AST\IMG_ONO.png').convert_alpha()

        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()

    def update(th):
        if th.stg_mgr.lv == 6:
            mv(th, 3)