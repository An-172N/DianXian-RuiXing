import pygame as pyg


class StartGUI:
    def __init__(th, own):
        th.own = own

        th.title = pyg.image.load('AST\IMG_TITLE.png').convert_alpha()

    def bg_draw(th):
        th.own.scr.blit(th.own.draw_rect(345, 330, 0,
                                         (0, 0, 0)),
                        (120, 15))
        
        # th.own.scr.blit(th.title, (120, 15))

    def start_txt(th):
        th.own.scr.blit(th.own.txt_func("Z 开始"),
                        (390, 235))
        th.own.scr.blit(th.own.txt_func("Q 退出"),
                        (390, 285))
        th.own.scr.blit(th.own.txt_func("Copyright (c) 2025 An_172N"),
                        (128, 295))
        th.own.scr.blit(th.own.txt_func("源（GPL3.0）神，启动（开源）！"),
                        (128, 320))

    def blit(th):
        th.bg_draw()

        th.start_txt()