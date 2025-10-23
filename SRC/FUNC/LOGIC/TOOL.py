import datetime as dt

import pygame as pyg


def op_file(write, file, str=None):
    if write:
        with open(file, 'w') as f:
            return f.write(str)
    else:
        with open(file, 'r') as f:
            return f.read()


def get_dt(date):
    if date:
        return dt.datetime.now().strftime('%Y-%m-%d')
    else:
        return dt.datetime.now().strftime("%H:%M:%S")
    

def draw_rect(sur, clr, val, pos):
    surface = pyg.Surface((val[0], val[1]), pyg.SRCALPHA)

    pyg.draw.rect(surface,
                  clr,
                  surface.get_rect(),
                  val[2])

    sur.blit(surface, pos)


def txt_func(sur, clr, fnt, txt, pos):
    sur.blit(fnt.render(f"{txt}",
                        False,
                        clr),
             pos)