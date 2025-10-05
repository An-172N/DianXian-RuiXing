import pygame as pyg


class Kli(pyg.sprite.Sprite):
    def __init__(th, own, pln_mgr):
        super().__init__()
        th.own = own
        th.pln_mgr = pln_mgr

        th.clr = th.own.clr_dict[5]

        th.orig_image = pyg.image.load('AST\IMG_KLI.png').convert_alpha()
        th.image = th.orig_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

    def update(th):
        th.pln_mgr.turn_side()
        th.pln_mgr.mv_pln()

        th.pln_mgr.invinc()