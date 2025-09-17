import pygame as pyg

from BRICK.HUMAN.ONO import Ono

from LOGIC.PROCESS.MOVE import mv


class Stage1:
    def __init__(th, own):
        th.stg_mgr = own

        th.char = Ono()

        th.image = pyg.image.load('AST/IMG_STAGE1BG.png').convert_alpha()
        th.image.set_alpha(175)

    def blit(th):
        th.stg_mgr.own.scr.blit(th.image, (120, 15))

    def text(th):
        text_dict = {
            0: f"测试1",
            1: f"测试2",
            2: f"测试3"
        }

        return text_dict
    
    def mv_char(th):
        mv(th.char, -4)