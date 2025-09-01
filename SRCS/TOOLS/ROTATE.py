import pygame as pyg


def rot(spr):
    if not hasattr(spr, 'orig_image'):
        spr.orig_image = spr.image.copy()

    spr.image = pyg.transform.rotate(spr.orig_image, spr.curr_ang)
    spr.rect = spr.image.get_rect(center=spr.rect.center)