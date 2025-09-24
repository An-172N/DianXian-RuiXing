import pygame as pyg


class MainChar(pyg.sprite.Sprite):
    def __init__(th, name, pic):
        super().__init__()
        th.name = name

        th.orig_image = pyg.image.load(pic).convert_alpha()

        th.image = th.orig_image.subsurface((0, 0,
                                             12, 26))
        th.rect = th.image.get_rect()