# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from io import BytesIO
from pkgutil import get_data


import pygame as pg


from LOGIC.GRAPHIC import *
from LOGIC.CALCULATE import *


window = pg.Rect(120, 15, 345, 330)
effective = pg.Rect(105, 0, 375, 360)
brick_ready = []


color_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    4: (251, 234, 18),
    5: (45, 194, 229),
    6: (255, 255, 255),
    7: (128, 128, 128),
    8: (0, 0, 0),
    9: (32, 0, 128)
}


asset = lambda path: get_data(__name__, path)
font = pg.font.Font(BytesIO(asset(r'ASSET\FONT\UNI3500.otf')), 15)
icon = pg.display.set_icon(pg.image.load(BytesIO(asset(r'ASSET\IMAGE\ICON.png'))))


sound_cache = {
    i: pg.mixer.Sound(BytesIO(asset(rf'ASSET\FLAC\{i.upper()}.flac'))) for i in ('pick', 'fire', 'charge', 'tick')
}


char_image = pg.image.load(BytesIO(asset(r'ASSET\IMAGE\CHAR.png'))).convert_alpha()
basic_image = pg.image.load(BytesIO(asset(r'ASSET\IMAGE\BASIC.png'))).convert_alpha()
picture = {
    **{i: pg.image.load(BytesIO(asset(rf'ASSET\IMAGE\STAGE{i}BG.png'))).convert() for i in range(1, 5)},
    5: pg.Surface((345, 330)).convert(),
    6: pg.image.load(BytesIO(asset(r'ASSET\IMAGE\GAMEBG.png'))).convert_alpha(),
    7: pg.Surface((480, 360)).convert()
}


barrage_cache = {
    **{(2, color_dict[i]): Draw.circle((0, 0, 8, 8), 0, color_dict[i]).convert_alpha() for i in (1, 4, 6)},
    (0, color_dict[2]): (surface := basic_image.subsurface(75, 7, 8, 8).copy(), surface.fill(color_dict[2], special_flags=pg.BLEND_RGBA_MULT))[0],
    (0, color_dict[6]): basic_image.subsurface(75, 7, 8, 8)
}


brick_cache = {
    **{(i, color_dict[j]): basic_image.subsurface(k, 0, 15, 15) for i, j, k in ((2, 1, 0), (0, 2, 15), (1, 3, 30), (2, 4, 45), (0, 6, 60))},
    (2, color_dict[6]): Draw.circle((0, 0, 15, 15), 2, color_dict[6]).convert_alpha(),
    (1, color_dict[6]): Draw.rectangle((15, 15), 2, color_dict[6]).convert_alpha()
}


bullet = Draw.rectangle((15, 15), 0, color_dict[5]).convert()
bullet_cache = {
    "bullet": bullet.subsurface(0, 0, 2, 15).convert_alpha(),
    "bullet-cross": bullet.subsurface(2, 0, 2, 15).convert_alpha(),
    "bomb": bullet
}


line_cache = {
    (length, angle, color): pg.transform.rotate(Draw.rectangle((2, length), 0, color).convert_alpha(), angle)
    for length in (64, 128, 192)
    for angle in range(0, 180, 10)
    for color in (color_dict[5], color_dict[9])
}


item_cache = {i: Draw.rectangle((9, 9), 2, color_dict[j]).convert() for i, j in (("flash", 2), ("power", 5), ("fire", 6))}


particle_cache = {
    (9, color_dict[5]): Draw.rectangle((9, 9), 0, color_dict[5]).convert(),
    (3, color_dict[3]): Draw.rectangle((3, 3), 0, color_dict[3]).convert(),
    **{(3 * i, color_dict[6]): Draw.rectangle((3 * i, 3 * i), 0, color_dict[6]).convert() for i in range(1, 5)},
    **{(2, color_dict[i]): Draw.rectangle((2, 2), 0, color_dict[i]).convert() for i in range(1, 7)}
}


difficulty = [0.17 + (fibonacci(0, 1, i) / 100) for i in range(4, 8)]