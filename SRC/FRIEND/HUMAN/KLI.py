import pygame as pyg


class Kli(pyg.sprite.Sprite):
    def __init__(th, proc):
        super().__init__()
        th.proc = proc

        th.clr = th.proc("get", "main", "clr")[5]

        th.orig_image = pyg.image.load('AST\IMG_KLI.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

    def update(th):
        th.proc("func", "pln", "turn_side")()
        th.proc("func", "pln", "mv_pln")()

        th.proc("func", "pln", "invinc")()