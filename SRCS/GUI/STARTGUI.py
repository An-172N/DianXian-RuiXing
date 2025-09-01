import pygame as pyg


class StartGUI:
    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.fnt = fnt
        th.clk = clk

    def start_text(th):
        return th.fnt.render("Z 开始", False, (255, 255, 255))
    
    def exit_text(th):
        return th.fnt.render("Q 退出", False, (255, 255, 255))

    def blit(th):
        th.scr.fill((0, 0, 0))
        
        th.scr.blit(th.start_text(), (th.scr.get_width() // 2, 100))
        th.scr.blit(th.exit_text(), (th.scr.get_width() // 2, 150))
        
        pyg.display.flip()