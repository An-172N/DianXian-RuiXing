import sys
import os

import pygame

from SCRIPT.LOGIC.FRIEND.HUMAN.ONO import Ono
from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import Kli
from SCRIPT.LOGIC.FRIEND.HUMAN.HRO import Hro
from SCRIPT.LOGIC.FRIEND.HUMAN.NRE import Nre
from SCRIPT.LOGIC.FRIEND.HUMAN.QDI import Qdi
from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import DecisionPoint
from SCRIPT.LOGIC.FRIEND.BASE import Base

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
    5: Kli,
    6: DecisionPoint,
    7: Base
}

keydown_game_dict = {
    pygame.K_RIGHT: lambda: setattr(VARIABLE, "move_right", True),
    pygame.K_LEFT: lambda: setattr(VARIABLE, "move_left", True),
    pygame.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow", True),
    pygame.K_z: lambda : setattr(VARIABLE, "can_shoot", False),
    pygame.K_x: lambda : LOGIC.BulletMgr.single_bomb(),
    pygame.K_ESCAPE: lambda: setattr(VARIABLE, "pause", True)
}

keydown_talk_dict = {
    pygame.K_z: lambda : setattr(VARIABLE, "text_number", VARIABLE.text_number + 1),
    pygame.K_x: lambda : setattr(VARIABLE, "talk", False)
}

keydown_pause_dict = {
    pygame.K_ESCAPE: lambda : setattr(VARIABLE, "pause", False),
    pygame.K_q: lambda : (
        VARIABLE.reset1(),
        VARIABLE.reset2()
    )
}

keydown_start_dict = {
    pygame.K_z: lambda: (
        setattr(VARIABLE, "run", True),
        LOGIC.StageMgr.next_level(),
        LOGIC.StageMgr.level_logic()
    ),
    pygame.K_q: lambda: sys.exit()
}

keydown_over_dict = {
    pygame.K_RETURN: lambda: (
        LOGIC.Key.save_file(),
        VARIABLE.reset1(),
        VARIABLE.reset2()
    ),
    pygame.K_ESCAPE: lambda: (
        VARIABLE.reset1(),
        VARIABLE.reset2()
    ),
    pygame.K_BACKSPACE: lambda: setattr(VARIABLE, "name", VARIABLE.name[:-1])
}

keyup_game_dict = {
    pygame.K_RIGHT: lambda: setattr(VARIABLE, "move_right", False),
    pygame.K_LEFT: lambda: setattr(VARIABLE, "move_left", False),
    pygame.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow", False),
    pygame.K_z: lambda: setattr(VARIABLE, "can_shoot", True)
}