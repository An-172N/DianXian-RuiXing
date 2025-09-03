import pygame as pyg


class Stage1:
    def __init__(th, own, scr):
        th.own = own
        th.scr = scr

        th.image = pyg.image.load('ASTS/IMG_STAGE1BG.png').convert_alpha()
        th.image.set_alpha(175)

    def blit(th):
        th.scr.blit(th.image, (120, 15))

    def text(th):
        text_dict = {
            0: f"我是璃",
            1: f"我是罗",
            2: f"我是诺"
        }

        return text_dict