import sys

import pygame as pyg

from SCRIPT.LOGIC.FRIEND import Ono
from SCRIPT.LOGIC.FRIEND import Kli
from SCRIPT.LOGIC.FRIEND import Hro
from SCRIPT.LOGIC.FRIEND import Nre

import VARIABLE
import SCRIPT.LOGIC


clr_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    5: (45, 194, 229),
    6: (255, 255, 255),
    7: (0, 0, 0)
}

char_dict = {
    1: Ono,
    2: Hro,
    3: Nre,
    4: Kli
}

key_dict = {
    "down": {
        "game": {
            pyg.K_RIGHT: lambda: setattr(VARIABLE, "mv_right",
                                         True),
            pyg.K_LEFT: lambda: setattr(VARIABLE, "mv_left",
                                        True),
            pyg.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow",
                                          True),
            pyg.K_z: lambda : SCRIPT.LOGIC.BulletMgr.spwn_blt(),
            pyg.K_x: lambda : SCRIPT.LOGIC.BulletMgr.single_bomb(),
            pyg.K_ESCAPE: lambda: setattr(VARIABLE, "pau",
                                          True)
        },
        "talk": {
            pyg.K_z: lambda : setattr(VARIABLE, "txt_num",
                                      VARIABLE.txt_num + 1),
            pyg.K_x: lambda : setattr(VARIABLE, "talk",
                                      False)
        },
        "pau": {
            pyg.K_ESCAPE: lambda : setattr(VARIABLE, "pau",
                                           False),
            pyg.K_q: lambda : setattr(VARIABLE, "is_rst",
                                      True)
        },
        "start": {
            pyg.K_z: lambda: (setattr(VARIABLE, "run",
                                         True),
                              SCRIPT.LOGIC.StageMgr.next_lv(),
                              SCRIPT.LOGIC.StageMgr.lv_lgc()),
            pyg.K_q: lambda: sys.exit()
        },
        "over": {
            pyg.K_RETURN: lambda: (SCRIPT.LOGIC.Key.sav_file(),
                                   setattr(VARIABLE, "is_rst",
                                   True)),
            pyg.K_ESCAPE: lambda: setattr(VARIABLE, "is_rst",
                                          True),
            pyg.K_BACKSPACE: lambda: setattr(VARIABLE, "name",
                                             VARIABLE.name[:-1])
        }
    },
    "up": {
        "game": {
            pyg.K_RIGHT: lambda: setattr(VARIABLE, "mv_right",
                                         False),
            pyg.K_LEFT: lambda: setattr(VARIABLE, "mv_left",
                                        False),
            pyg.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow",
                                          False),
            pyg.K_z: lambda: (SCRIPT.LOGIC.BulletMgr.spwn_blt(),
                              setattr(VARIABLE, "can_shoot",
                                      True))
        }
    }
}