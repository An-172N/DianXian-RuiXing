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
    8: (0, 0, 0)
}


asset = lambda path: pkgutil.get_data(__name__, path)
font = pygame.font.Font(io.BytesIO(asset(r'ASSET\FONT\FONT_UNI3500.otf')), 15)
icon = pygame.display.set_icon(pygame.image.load(io.BytesIO(asset(r'ASSET\ICON.ico'))))


char_image = pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_CHAR.png'))).convert_alpha()
brick_image = pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_BRICK.png'))).convert_alpha()
barrage_image = pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_BARRAGE.png'))).convert_alpha()
picture = {
    1: pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_STAGE1BG.png'))).convert(),
    2: pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_STAGE2BG.png'))).convert(),
    3: pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_STAGE3BG.png'))).convert(),
    4: pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_STAGE4BG.png'))).convert(),
    5: LOGIC.Tool.draw_rectangle((345, 330), 0, color_dict[8]).convert(),
    6: pygame.image.load(io.BytesIO(asset(r'ASSET\IMAGE\IMG_GAMEBG.png'))).convert_alpha()
}


barrage_cache = {
    f"{2}_{color_dict[1]}": LOGIC.Tool.draw_circle((0, 0, 9, 9), 0, color_dict[1]).convert_alpha(),
    f"{2}_{color_dict[4]}": LOGIC.Tool.draw_circle((0, 0, 9, 9), 0, color_dict[4]).convert_alpha(),
    f"{2}_{color_dict[6]}": LOGIC.Tool.draw_circle((0, 0, 9, 9), 0, color_dict[6]).convert_alpha(),
    f"{0}_{color_dict[2]}": barrage_image.subsurface((0, 0, 9, 8)),
    f"{0}_{color_dict[6]}": barrage_image.subsurface((9, 0, 9, 8))
}


brick_cache = {
    f"{2}_{color_dict[1]}": brick_image.subsurface((0, 0, 15, 15)),
    f"{2}_{color_dict[4]}": brick_image.subsurface((45, 0, 15, 15)),
    f"{2}_{color_dict[6]}": LOGIC.Tool.draw_circle((0, 0, 15, 15), 2, color_dict[6]).convert_alpha(),
    f"{0}_{color_dict[2]}": brick_image.subsurface((15, 0, 15, 15)),
    f"{0}_{color_dict[6]}": brick_image.subsurface((60, 0, 15, 15)),
    f"{1}_{color_dict[3]}": brick_image.subsurface((30, 0, 15, 15)),
    f"{1}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((15, 15), 2, color_dict[6]).convert_alpha()
}


bullet = LOGIC.Tool.draw_rectangle((2, 15), 0, color_dict[5]).convert_alpha()
bullet_cache = {
    "bullet": bullet,
    "bullet-cross": bullet,
    "bomb": LOGIC.Tool.draw_rectangle((15, 15), 0, color_dict[5]).convert()
}


item_cache = {
    "flash": LOGIC.Tool.draw_rectangle((9, 9), 2, color_dict[2]).convert_alpha(),
    "power": LOGIC.Tool.draw_rectangle((9, 9), 2, color_dict[5]).convert_alpha(),
    "fire": LOGIC.Tool.draw_rectangle((9, 9), 2, color_dict[6]).convert_alpha()
}


line_cache = {
    32: LOGIC.Tool.draw_rectangle((2, 32), 0, color_dict[5]).convert_alpha(),
    64: LOGIC.Tool.draw_rectangle((2, 64), 0, color_dict[5]).convert_alpha(),
    128: LOGIC.Tool.draw_rectangle((2, 128), 0, color_dict[5]).convert_alpha(),
    256: LOGIC.Tool.draw_rectangle((2, 256), 0, color_dict[5]).convert_alpha(),
    500: LOGIC.Tool.draw_rectangle((3, 478), 0, color_dict[6]).convert_alpha()
}


particle_cache = {
    f"{(9, 9)}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((9, 9), 0, color_dict[6]).convert_alpha(),
    f"{(9, 9)}_{color_dict[5]}": LOGIC.Tool.draw_rectangle((9, 9), 0, color_dict[5]).convert_alpha(),
    f"{(2, 2)}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((2, 2), 0, color_dict[6]).convert_alpha(),
    f"{(2, 2)}_{color_dict[5]}": LOGIC.Tool.draw_rectangle((2, 2), 0, color_dict[5]).convert_alpha(),
    f"{(2, 2)}_{color_dict[1]}": LOGIC.Tool.draw_rectangle((2, 2), 0, color_dict[1]).convert_alpha(),
    f"{(2, 2)}_{color_dict[2]}": LOGIC.Tool.draw_rectangle((2, 2), 0, color_dict[2]).convert_alpha(),
    f"{(2, 2)}_{color_dict[3]}": LOGIC.Tool.draw_rectangle((2, 2), 0, color_dict[3]).convert_alpha(),
    f"{(2, 2)}_{color_dict[4]}": LOGIC.Tool.draw_rectangle((2, 2), 0, color_dict[4]).convert_alpha(),
    f"{(4, 4)}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((4, 4), 0, color_dict[6]).convert(),
    f"{(6, 6)}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((6, 6), 0, color_dict[6]).convert(),
    f"{(10, 10)}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((10, 10), 0, color_dict[6]).convert(),
    f"{(12, 12)}_{color_dict[6]}": LOGIC.Tool.draw_rectangle((12, 12), 0, color_dict[6]).convert()
}


text_cache = {
    **{f"{2 ** i}_{color_dict[6]}": font.render(f"+ {2 ** i}", False, color_dict[6]).convert_alpha() for i in range(1, 15)},
    **{f"{2 ** i}_{color_dict[7]}": font.render(f"+ {2 ** i}", False, color_dict[7]).convert_alpha() for i in range(1, 15)},
    f"extend_{color_dict[6]}": font.render("Extend", False, color_dict[6]).convert_alpha(),
    f"extend_{color_dict[2]}": font.render("Extend", False, color_dict[2]).convert_alpha()
}


barrage_rate = [0.17 + (LOGIC.Tool.fibonacci(0, 1, i) / 100) for i in range(4, 8)]