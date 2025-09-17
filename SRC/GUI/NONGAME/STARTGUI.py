import pygame as pyg


class StartGUI:
    def __init__(th, own):
        th.own = own

        th.title = pyg.image.load('AST\IMG_TITLE.png').convert_alpha()

    def start_draw(th):
        text1 = th.own.fnt.render("Z 开始", False, (255, 255, 255))
        text2 = th.own.fnt.render("C 选关", False, (255, 255, 255))
        text3 = th.own.fnt.render("Q 退出", False, (255, 255, 255))

        th.own.scr.blit(th.draw_rect(), (120, 15))
        th.own.scr.blit(text1, (390, 185))
        th.own.scr.blit(text2, (390, 235))
        th.own.scr.blit(text3, (390, 285))
    
    def draw_rect(th):
        surface = pyg.Surface((345, 330), pyg.SRCALPHA)

        pyg.draw.rect(surface, (0, 0, 0), surface.get_rect(), 0)

        return surface
    
    def blit(th):
        th.start_draw()

        # th.own.scr.blit(th.title, (120, 15))