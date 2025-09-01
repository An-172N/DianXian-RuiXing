import pygame as pyg


class Stage1:
    def __init__(th, scr):
        th.scr = scr

        th.image = pyg.image.load('ASTS/IMG_STAGE1BG.png').convert_alpha()
        th.image.set_alpha(175)

    def blit(th):
        th.scr.blit(th.image, (120, 15))