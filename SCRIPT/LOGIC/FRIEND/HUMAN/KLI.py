import os

import pygame as pyg

import SCRIPT.DICT
import SCRIPT.RESET
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base
from SCRIPT.DRAW import ShapeDraw


class Kli(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.clr = SCRIPT.DICT.clr_dict[5]

        th.bomb = RectRaining()

        th.orig_image = pyg.image.load(os.path.join(SCRIPT.RESET.asset_path, 'IMG_KLI.png')).convert_alpha()
        th.image = th.orig_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()


class DecPt(pyg.sprite.Sprite):
    def __init__(th):
        super().__init__()
        th.orig_image = ShapeDraw(4, 4, 0, (127, 127, 127)).rect()
        th.image = th.orig_image
        th.rect = th.image.get_rect()
        th.mask = pyg.mask.from_surface(th.image)


class RectRaining:
    def __init__(th):
        th.bomb_cnt = 0
        th.ctr = 0

    def free(th) -> None:
        th.ctr += 1

        if (th.ctr >= 30 and
            th.ctr % 1 == 0 and
            th.bomb_cnt < 6):
            for i in range(120, 466, 15):
                spr = Base((15, 15, 0), (45, 194, 229), 1, "blt")
                if not hasattr(spr, "dmg"):
                    spr.dmg = 6
                spr.spd = -24
                spr.rect.center = (i, 0)
                VARIABLE.blt_grp.add(spr)

            th.bomb_cnt += 1

    def fire(th, dx, dy, ang) -> None:
        left = VARIABLE.main_char.rect.left
        top = VARIABLE.main_char.rect.top
        right = VARIABLE.main_char.rect.right
        blt_type = [
            {'x': left - dx,
             'y': top + dy,
             'ang': ang},
            {'x': right + dx,
             'y': top + dy,
             'ang': -ang}
        ]

        for blt_info in blt_type:
            spr = Base((2, 15, 0), (45, 194, 229), 1, "blt")
            if not hasattr(spr, "dmg"):
                spr.dmg = 4
            spr.spd = 16
            spr.rect.center = (blt_info['x'], blt_info['y'])
            spr.curr_ang = blt_info['ang']
            VARIABLE.blt_grp.add(spr)