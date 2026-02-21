# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import io
import pkgutil


import pygame


import LOGIC


window = pygame.Rect(120, 15, 345, 330)
effective = pygame.Rect(105, 0, 375, 360)


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


asset = lambda path: pkgutil.get_data(__name__, path)
font = pygame.font.Font(io.BytesIO(asset(r'ASSET\FONT\FONT_UNI3500.otf')), 15)
icon = pygame.display.set_icon(pygame.image.load(io.BytesIO(asset(r'ASSET\ICON.ico'))))


char_image = pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_CHAR.png'))).convert_alpha()
brick_image = pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_BRICK.png'))).convert_alpha()
barrage_image = pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_BARRAGE.png'))).convert_alpha()
picture = {
    **{i: pygame.image.load(io.BytesIO(asset(rf'ASSET\IMAGE\IMG_STAGE{i}BG.png'))).convert() for i in range(1, 5)},
    5: LOGIC.Draw.rectangle((345, 330), 0, color_dict[8]).convert(),
    6: pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_GAMEBG.png'))).convert_alpha()
}


new_barrage = barrage_image.copy()
new_barrage.fill(color_dict[2], special_flags=pygame.BLEND_RGBA_MULT)
barrage_cache = {
    f"{2}_{color_dict[1]}": LOGIC.Draw.circle((0, 0, 9, 9), 0, color_dict[1]).convert_alpha(),
    f"{2}_{color_dict[4]}": LOGIC.Draw.circle((0, 0, 9, 9), 0, color_dict[4]).convert_alpha(),
    f"{2}_{color_dict[6]}": LOGIC.Draw.circle((0, 0, 9, 9), 0, color_dict[6]).convert_alpha(),
    f"{0}_{color_dict[2]}": new_barrage,
    f"{0}_{color_dict[6]}": barrage_image
}


brick_cache = {
    f"{2}_{color_dict[1]}": brick_image.subsurface((0, 0, 15, 15)),
    f"{2}_{color_dict[4]}": brick_image.subsurface((45, 0, 15, 15)),
    f"{2}_{color_dict[6]}": LOGIC.Draw.circle((0, 0, 15, 15), 2, color_dict[6]).convert_alpha(),
    f"{0}_{color_dict[2]}": brick_image.subsurface((15, 0, 15, 15)),
    f"{0}_{color_dict[6]}": brick_image.subsurface((60, 0, 15, 15)),
    f"{1}_{color_dict[3]}": brick_image.subsurface((30, 0, 15, 15)),
    f"{1}_{color_dict[6]}": LOGIC.Draw.rectangle((15, 15), 2, color_dict[6]).convert_alpha()
}


bullet = LOGIC.Draw.rectangle((2, 15), 0, color_dict[5]).convert_alpha()
bullet_cache = {
    "bullet": bullet,
    "bullet-cross": bullet,
    "bomb": LOGIC.Draw.rectangle((15, 15), 0, color_dict[5]).convert()
}


item_cache = {
    "flash": LOGIC.Draw.rectangle((9, 9), 2, color_dict[2]).convert_alpha(),
    "power": LOGIC.Draw.rectangle((9, 9), 2, color_dict[5]).convert_alpha(),
    "fire": LOGIC.Draw.rectangle((9, 9), 2, color_dict[6]).convert_alpha()
}


line_cache = {
    (length, angle, color): pygame.transform.rotate(LOGIC.Draw.rectangle((3, 495) if length == 500 else (2, length), 0, color).convert_alpha(), angle)
    for length in [48, 96, 192, 500]
    for angle in range(0, 180, 9)
    for color in ([color_dict[6], color_dict[3]] if length == 500 else [color_dict[5], color_dict[9]])
}


particle_cache = {
    f"{(9, 9)}_{color_dict[5]}": LOGIC.Draw.rectangle((9, 9), 0, color_dict[5]).convert(),
    **{f"{(3 * i, 3 * i)}_{color_dict[6]}": LOGIC.Draw.rectangle((3 * i, 3 * i), 0, color_dict[6]).convert() for i in range(1, 5)},
    **{f"{(2, 2)}_{color_dict[i]}": LOGIC.Draw.rectangle((2, 2), 0, color_dict[i]).convert() for i in range(1, 7)}
}


text_cache = {
    **{f"{2 ** i}_{color_dict[6]}": font.render(f"+ {2 ** i}", False, color_dict[6]).convert_alpha() for i in range(1, 15)},
    **{f"{2 ** i}_{color_dict[7]}": font.render(f"+ {2 ** i}", False, color_dict[7]).convert_alpha() for i in range(1, 15)},
    f"extend_{color_dict[6]}": font.render("Extend", False, color_dict[6]).convert_alpha(),
    f"extend_{color_dict[2]}": font.render("Extend", False, color_dict[2]).convert_alpha()
}


barrage_rate = [0.17 + (LOGIC.Calculate.fibonacci(0, 1, i) / 100) for i in range(4, 8)]