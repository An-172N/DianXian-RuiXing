import sys
import os

import pygame

from SCRIPT.LOGIC.FRIEND.HUMAN.ONO import Ono
from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import Kli
from SCRIPT.LOGIC.FRIEND.HUMAN.HRO import Hro
from SCRIPT.LOGIC.FRIEND.HUMAN.NRE import Nre
from SCRIPT.LOGIC.FRIEND.HUMAN.QDI import Qdi

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.LOGIC as LOGIC


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
            pygame.K_RIGHT: lambda: setattr(VARIABLE, "move_right",
                                         True),
            pygame.K_LEFT: lambda: setattr(VARIABLE, "move_left",
                                        True),
            pygame.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow",
                                          True),
            pygame.K_z: lambda : setattr(VARIABLE, "can_shoot",
                                      False),
            pygame.K_x: lambda : LOGIC.BulletMgr.single_bomb(),
            pygame.K_ESCAPE: lambda: setattr(VARIABLE, "pause",
                                          True)
        },
        "talk": {
            pygame.K_z: lambda : setattr(VARIABLE, "text_number",
                                      VARIABLE.text_number + 1),
            pygame.K_x: lambda : setattr(VARIABLE, "talk",
                                      False)
        },
        "pause": {
            pygame.K_ESCAPE: lambda : setattr(VARIABLE, "pause",
                                           False),
            pygame.K_q: lambda : setattr(VARIABLE, "is_reset",
                                      True)
        },
        "start": {
            pygame.K_z: lambda: (setattr(VARIABLE, "run",
                                         True),
                              LOGIC.StageMgr.next_level(),
                              LOGIC.StageMgr.level_logic()),
            pygame.K_q: lambda: sys.exit()
        },
        "over": {
            pygame.K_RETURN: lambda: (LOGIC.Key.save_file(),
                                   setattr(VARIABLE, "is_reset",
                                   True)),
            pygame.K_ESCAPE: lambda: setattr(VARIABLE, "is_reset",
                                          True),
            pygame.K_BACKSPACE: lambda: setattr(VARIABLE, "name",
                                             VARIABLE.name[:-1])
        }
    },
    "up": {
        "game": {
            pygame.K_RIGHT: lambda: setattr(VARIABLE, "move_right",
                                         False),
            pygame.K_LEFT: lambda: setattr(VARIABLE, "move_left",
                                        False),
            pygame.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow",
                                          False),
            pygame.K_z: lambda: setattr(VARIABLE, "can_shoot",
                                     True)
        }
    }
}