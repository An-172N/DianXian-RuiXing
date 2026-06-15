# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from io import BytesIO
from pkgutil import get_data


import pygame as pg


from LOGIC import *


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


title = {
    1: "水边的秋霜店 ~ Sweet Reservoir",
    2: "X 在树林 ~ Hypnotized",
    3: "午夜行至最高峰 ~ Thunder Studio",
    4: "享受禁饮 ~ Point's Hideaway"
}


asset = lambda path: get_data(__name__, path)
get_stage = lambda stage: stage if stage < 3 else 'Final' if stage == 3 else 'Extra'
font = pg.font.Font(BytesIO(asset(r'ASSET\FONT\UNI3500.otf')), 15)
screen = pg.display.set_mode((480, 360), pg.FULLSCREEN|pg.SCALED, vsync=1)


sound_cache = {
    'pick': pg.mixer.Sound(BytesIO(asset(rf'ASSET\FLAC\PICK.flac'))),
    'fire': pg.mixer.Sound(BytesIO(asset(rf'ASSET\FLAC\FIRE.flac'))),
    'charge': pg.mixer.Sound(BytesIO(asset(rf'ASSET\FLAC\CHARGE.flac'))),
    'tick': pg.mixer.Sound(BytesIO(asset(rf'ASSET\FLAC\TICK.flac')))
}


char_image = pg.image.load(BytesIO(asset(r'ASSET\IMAGE\CHAR.png'))).convert_alpha()
basic_image = pg.image.load(BytesIO(asset(r'ASSET\IMAGE\BASIC.png'))).convert_alpha()
blue_rect = draw_rectangle((15, 15), 0, color_dict[5]).convert()
white_rect = draw_rectangle((12, 12), 0, color_dict[6]).convert()
picture = {
    1: pg.image.load(BytesIO(asset(rf'ASSET\IMAGE\STAGE1BG.png'))).convert(),
    2: pg.image.load(BytesIO(asset(rf'ASSET\IMAGE\STAGE2BG.png'))).convert(),
    3: pg.image.load(BytesIO(asset(rf'ASSET\IMAGE\STAGE3BG.png'))).convert(),
    4: pg.image.load(BytesIO(asset(rf'ASSET\IMAGE\STAGE4BG.png'))).convert(),
    5: pg.Surface((345, 330)).convert(),
    6: pg.image.load(BytesIO(asset(r'ASSET\IMAGE\GAMEBG.png'))).convert_alpha(),
    7: pg.Surface((480, 360)).convert()
}


barrage_cache = {
    (2, color_dict[6]): draw_circle((0, 0, 8, 8), 0, color_dict[6]).convert_alpha(),
    (0, color_dict[6]): basic_image.subsurface(75, 7, 8, 8),
    (0, color_dict[6]): basic_image.subsurface(75, 7, 8, 8)
}


brick_cache = {
    (2, color_dict[1]): basic_image.subsurface(0, 0, 15, 15),
    (0, color_dict[2]): basic_image.subsurface(15, 0, 15, 15),
    (1, color_dict[3]): basic_image.subsurface(30, 0, 15, 15),
    (2, color_dict[4]): basic_image.subsurface(45, 0, 15, 15),
    (0, color_dict[6]): basic_image.subsurface(60, 0, 15, 15),
    (2, color_dict[6]): draw_circle((0, 0, 15, 15), 2, color_dict[6]).convert_alpha(),
    (1, color_dict[6]): draw_rectangle((15, 15), 2, color_dict[6]).convert_alpha()
}


bullet_cache = {
    "bullet": blue_rect.subsurface(0, 0, 2, 15).convert_alpha(),
    "bomb": blue_rect
}


line_cache = {
    (length, angle, color): pg.transform.rotate(draw_rectangle((2, length), 0, color).convert_alpha(), angle)
    for length in (48, 96, 160)
    for angle in range(0, 180, 15)
    for color in (color_dict[5], color_dict[9])
}


item_cache = {
    "flash": draw_rectangle((9, 9), 2, color_dict[2]).convert(),
    "power": draw_rectangle((9, 9), 2, color_dict[5]).convert(),
    "fire": draw_rectangle((9, 9), 2, color_dict[6]).convert()
}


particle_cache = {
    (2, color_dict[1]): draw_rectangle((2, 2), 0, color_dict[1]).convert(),
    (2, color_dict[2]): draw_rectangle((2, 2), 0, color_dict[2]).convert(),
    (2, color_dict[3]): draw_rectangle((2, 2), 0, color_dict[3]).convert(),
    (2, color_dict[4]): draw_rectangle((2, 2), 0, color_dict[4]).convert(),
    (2, color_dict[5]): blue_rect.subsurface(0, 0, 2, 2),
    (9, color_dict[5]): blue_rect.subsurface(0, 0, 9, 9),
    (2, color_dict[6]): white_rect.subsurface(0, 0, 2, 2),
    (3, color_dict[6]): white_rect.subsurface(0, 0, 3, 3),
    (6, color_dict[6]): white_rect.subsurface(0, 0, 6, 6),
    (9, color_dict[6]): white_rect.subsurface(0, 0, 9, 9),
    (12, color_dict[6]): white_rect
}


difficulty = (0.22, 0.25, 0.3, 0.38)


pg.display.set_icon(pg.image.load(BytesIO(asset(r'ASSET\IMAGE\ICON.png'))))