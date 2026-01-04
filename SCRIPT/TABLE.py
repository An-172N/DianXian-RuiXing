import sys
import os

import pygame

from SCRIPT.LOGIC.FRIEND.HUMAN.ONO import Ono
from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import Kli
from SCRIPT.LOGIC.FRIEND.HUMAN.HRO import Hro
from SCRIPT.LOGIC.FRIEND.HUMAN.NRE import Nre
from SCRIPT.LOGIC.FRIEND.HUMAN.QDI import Qdi
from SCRIPT.LOGIC.FRIEND.HUMAN.KLI import DecisionPoint
from SCRIPT.LOGIC.FRIEND.SPRITE.BASE import Base

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.LOGIC as LOGIC
import SCRIPT.FUNC as FUNC


asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')

plane_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
barrage_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

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
    pygame.K_ESCAPE: lambda: (
        setattr(VARIABLE, "pause", True),
        setattr(VARIABLE, "is_blit", False)
    )
}

keydown_talk_dict = {
    pygame.K_z: lambda : (
        setattr(VARIABLE, "text_number", VARIABLE.text_number + 1),
        setattr(VARIABLE, "is_blit", False)
    ),
    pygame.K_x: lambda : setattr(VARIABLE, "talk", False)
}

keydown_pause_dict = {
    pygame.K_ESCAPE: lambda : setattr(VARIABLE, "pause", False),
    pygame.K_q: lambda : (
        VARIABLE.reset1(),
        VARIABLE.reset2(),
        setattr(VARIABLE, "is_blit", False)
    )
}

keydown_start_dict = {
    pygame.K_z: lambda: (
        setattr(VARIABLE, "run", True),
        setattr(VARIABLE, "is_blit", False),
        LOGIC.StageMgr.next_level(),
        LOGIC.StageMgr.level_logic()
    ),
    pygame.K_q: lambda: sys.exit()
}

keydown_over_dict = {
    pygame.K_RETURN: lambda: (
        LOGIC.Key.save_file(),
        VARIABLE.reset1(),
        VARIABLE.reset2(),
        setattr(VARIABLE, "is_blit", False)
    ),
    pygame.K_ESCAPE: lambda: (
        VARIABLE.reset1(),
        VARIABLE.reset2(),
        setattr(VARIABLE, "is_blit", False)
    ),
    pygame.K_BACKSPACE: lambda: (
        setattr(VARIABLE, "name", VARIABLE.name[:-1]),
        setattr(VARIABLE, "is_blit", False)
    )
}

keyup_game_dict = {
    pygame.K_RIGHT: lambda: setattr(VARIABLE, "move_right", False),
    pygame.K_LEFT: lambda: setattr(VARIABLE, "move_left", False),
    pygame.K_LSHIFT: lambda: setattr(VARIABLE, "is_slow", False),
    pygame.K_z: lambda: setattr(VARIABLE, "can_shoot", True)
}

fibonacci_list = [
    FUNC.Calculate.fibonacci(0, 1, i)[1] / 100
    for i in range(1, 5)
]

picture_list = [
    (1, os.path.join(asset_path, 'IMAGE\IMG_STAGE1BG.png')),
    (2, os.path.join(asset_path, 'IMAGE\IMG_STAGE2BG.png')),
    (3, os.path.join(asset_path, 'IMAGE\IMG_STAGE3BG.png')),
    (4, os.path.join(asset_path, 'IMAGE\IMG_STAGE4BG.png')),
    ("GAME_BG", os.path.join(asset_path, 'IMAGE\IMG_GAMEBG.png')),
    ("MENU_BG", os.path.join(asset_path, 'IMAGE\IMG_MENU.png'))
]

char_image_list = [
    ("Kli", os.path.join(asset_path, 'IMAGE\IMG_KLI.png')),
    ("Ono", os.path.join(asset_path, 'IMAGE\IMG_ONO.png')),
    ("Hro", os.path.join(asset_path, 'IMAGE\IMG_HRO.png')),
    ("Nre", os.path.join(asset_path, 'IMAGE\IMG_NRE.png')),
    ("Qdi", os.path.join(asset_path, 'IMAGE\IMG_QDI.png'))
]

sprite_image_list = [
    (f"C_BA_{color_dict[1]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEORANGE.png')),
    (f"C_BA_{color_dict[4]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEYELLOW.png')),
    (f"C_BA_{color_dict[6]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEWHITE.png')),
    (f"P_BA_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBARRAGEGREEN.png')),
    (f"P_BA_{color_dict[6]}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBARRAGEWHITE.png')),
    (f"C_BR_{color_dict[1]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKORANGE.png')),
    (f"C_BR_{color_dict[4]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKYELLOW.png')),
    (f"C_BR_{color_dict[6]}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBRICKWHITE.png')),
    (f"P_BR_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBRICKGREEN.png')),
    (f"P_BR_{color_dict[6]}", os.path.join(asset_path, f'IMAGE\IMG_POLYGONBRICKWHITE.png')),
    (f"R_BR_{color_dict[3]}", os.path.join(asset_path, f'IMAGE\IMG_RECTANGLEBRICKPURPLE.png')),
    (f"R_BR_{color_dict[6]}", os.path.join(asset_path, f'IMAGE\IMG_RECTANGLEBRICKWHITE.png')),
    (f"R_IT_{color_dict[2]}", os.path.join(asset_path, f'IMAGE\IMG_ITEMGREEN.png')),
    (f"R_IT_{color_dict[5]}", os.path.join(asset_path, f'IMAGE\IMG_ITEMBLUE.png')),
    (f"R_IT_{color_dict[6]}", os.path.join(asset_path, f'IMAGE\IMG_ITEMWHITE.png')),
    ("KLI_BULLET", os.path.join(asset_path, f'IMAGE\IMG_KLIBULLET.png')),
    ("KLI_BOMB", os.path.join(asset_path, f'IMAGE\IMG_KLIBOMB.png')),
    ("DEC", os.path.join(asset_path, f'IMAGE\IMG_DECISIONPOINT.png')),
]