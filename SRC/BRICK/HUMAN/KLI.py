import pygame as pyg


class Kli(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()
        th.pln_spd_mod = 0
        th.pln_spd = th.char_spd()

        th.orig_image = pyg.image.load('AST\IMG_KLI.png').convert_alpha()

        th.image = th.orig_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

    def char_spd(th):
        if th.pln_spd_mod == 0:
            return 4
        else:
            return 1