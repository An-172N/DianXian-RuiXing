import pygame as pyg


class Ono(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()
        th.hp = 48
        th.clr = (255, 128, 0)
        th.shape = 2

        th.orig_image = pyg.image.load('ASTS\IMG_ONO.png').convert_alpha()

        th.image = th.orig_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()