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
    

def draw_rect(sur, wid, hei, bd, pos):
    surface = pyg.Surface((wid, hei), pyg.SRCALPHA)

    pyg.draw.rect(surface,
                  (0, 0, 0),
                  surface.get_rect(),
                  bd)

    sur.blit(surface, pos)


def txt_func(sur, fnt, txt, pos):
    sur.blit(fnt.render(f"{txt}",
                        False,
                        (255, 255, 255)),
             pos)