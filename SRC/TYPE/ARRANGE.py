import pygame as pyg


class Arrange:
    def __init__(th, own):
        th.own = own

    def draw_rect(th, wid, hei, bd, clr, pos):
        surface = pyg.Surface((wid, hei), pyg.SRCALPHA)

        pyg.draw.rect(surface,
                      clr,
                      surface.get_rect(),
                      bd)

        th.own.scr.blit(surface, pos)

    def txt_func(th, txt, pos):
        th.own.scr.blit(th.own.fnt.render(f"{txt}",
                                          False,
                                          th.own.clr_dict[6]),
                        pos)

    def full_menu(th, tit="", txt1="", txt2="", txt3="", ctl1="", ctl2="", oth=""):
        th.draw_rect(345, 330, 0,
                     th.own.clr_dict[7],
                     (120, 15))

        th.txt_func(tit, (128, 25))

        th.txt_func(txt1, (128, 75))
        th.txt_func(txt2, (128, 100))
        th.txt_func(txt3, (128, 125))
        
        th.txt_func(ctl1, (390, 235))
        th.txt_func(ctl2, (390, 285))
        
        th.txt_func(oth, (128, 320))

    def half_menu(th, tit, txt1, txt2):
        th.draw_rect(345, 85, 0,
                     th.own.clr_dict[7],
                     (120, 260))

        th.txt_func(tit, (125, 268))

        th.txt_func(txt1, (125, 293))
        th.txt_func(txt2, (125, 318))

    def situ(th, txt1, txt2, txt3, txt4, fps):
        th.txt_func(txt1, (8, 25))

        th.txt_func(txt2, (8, 270))
        th.txt_func(txt3, (8, 295))
        th.txt_func(txt4, (8, 320))

        th.txt_func(fps, (405, 343))