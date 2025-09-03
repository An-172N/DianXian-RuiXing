import pygame as pyg


class StartGUI:
    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.fnt = fnt
        th.clk = clk

        th.title = pyg.image.load('ASTS\IMG_TITLE.png').convert_alpha()

    def start_text(th):
        return th.fnt.render("Z 开始", False, (255, 255, 255))
    
    def choose_stg_text(th):
        return th.fnt.render("C 选关", False, (255, 255, 255))
    
    def exit_text(th):
        return th.fnt.render("Q 退出", False, (255, 255, 255))
    
    def rect(th):
        surface = pyg.Surface((100, 200), pyg.SRCALPHA)

        pyg.draw.rect(surface, (255, 255, 255), surface.get_rect(), 4)

        return surface

    def blit(th):
        th.scr.fill((0, 0, 0))
        
        th.scr.blit(th.title, (0, 0))
        th.scr.blit(th.rect(), (380, 160))

        th.scr.blit(th.start_text(), (405, 200))
        th.scr.blit(th.choose_stg_text(), (405, 250))
        th.scr.blit(th.exit_text(), (405, 300))
        
        pyg.display.flip()