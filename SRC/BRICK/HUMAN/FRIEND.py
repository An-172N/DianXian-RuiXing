import pygame as pyg


class Friend(pyg.sprite.Sprite):
    def __init__(th, name, pic, hp, clr, shape):
        super().__init__()
        th.name = name
        th.hp = hp
        th.clr = clr
        th.shape = shape

        th.curr_ang = 0

        th.orig_image = pyg.image.load(pic).convert_alpha()

        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()