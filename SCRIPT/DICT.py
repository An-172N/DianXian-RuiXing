import sys
import os

import pygame as pyg

from SCRIPT.LOGIC.FRIEND.HUMAN.ONO import Ono
from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import Kli
from SCRIPT.LOGIC.FRIEND.HUMAN.HRO import Hro
from SCRIPT.LOGIC.FRIEND.HUMAN.NRE import Nre
from SCRIPT.LOGIC.FRIEND.HUMAN.QDI import Qdi

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.LOGIC


asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')

color_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    4: (251, 234, 18),
    5: (45, 194, 229),
    6: (255, 255, 255),
    7: (0, 0, 0)
}

char_dict = {
    1: Ono,
    2: Hro,
    3: Nre,
    4: Qdi,
    5: Kli
}

key_dict = {
    "down": {
        "game": {
            pyg.K_RIGHT: lambda: setattr(VARIABLE, "move_right",
                                         True),
            pyg.K_LEFT: lambda: setattr(VARIABLE, "move_left",
                                        True),
            pyg.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow",
                                          True),
            pyg.K_z: lambda : setattr(VARIABLE, "can_shoot",
                                      False),
            pyg.K_x: lambda : SCRIPT.LOGIC.BulletMgr.single_bomb(),
            pyg.K_ESCAPE: lambda: setattr(VARIABLE, "pause",
                                          True)
        },
        "talk": {
            pyg.K_z: lambda : setattr(VARIABLE, "text_number",
                                      VARIABLE.text_number + 1),
            pyg.K_x: lambda : setattr(VARIABLE, "talk",
                                      False)
        },
        "pause": {
            pyg.K_ESCAPE: lambda : setattr(VARIABLE, "pause",
                                           False),
            pyg.K_q: lambda : setattr(VARIABLE, "is_reset",
                                      True)
        },
        "start": {
            pyg.K_z: lambda: (setattr(VARIABLE, "run",
                                         True),
                              SCRIPT.LOGIC.StageMgr.next_level(),
                              SCRIPT.LOGIC.StageMgr.level_logic()),
            pyg.K_q: lambda: sys.exit()
        },
        "over": {
            pyg.K_RETURN: lambda: (SCRIPT.LOGIC.Key.save_file(),
                                   setattr(VARIABLE, "is_reset",
                                   True)),
            pyg.K_ESCAPE: lambda: setattr(VARIABLE, "is_reset",
                                          True),
            pyg.K_BACKSPACE: lambda: setattr(VARIABLE, "name",
                                             VARIABLE.name[:-1])
        }
    },
    "up": {
        "game": {
            pyg.K_RIGHT: lambda: setattr(VARIABLE, "move_right",
                                         False),
            pyg.K_LEFT: lambda: setattr(VARIABLE, "move_left",
                                        False),
            pyg.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow",
                                          False),
            pyg.K_z: lambda: setattr(VARIABLE, "can_shoot",
                                     True)
        }
    }
}