# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import datetime

import pygame

import PRELOAD
from LOGIC import Tool, Item
from SCRIPT import GLOBAL


def show_situation(screen: pygame.Surface, font: pygame.font.Font, clock: pygame.time.Clock) -> None:
    GLOBAL.fps_text, GLOBAL.last_time = Tool.update_fps(GLOBAL.fps_text, GLOBAL.last_time, 0, 500, clock)

    text = [
        f"分　{GLOBAL.score:9d}",
        f"形　{GLOBAL.power:02d} , {GLOBAL.total_power:02d}",
        f"闪　{GLOBAL.flash:02d}",
        f"连　{GLOBAL.combo:02d} , {GLOBAL.shoot_counter:02d}"
    ]

    situation(screen, font, text, GLOBAL.fps_text)


def pause_menu(screen: pygame.Surface, font: pygame.font.Font) -> None:
    title = "休息ing"
    text = ["ESC 休息好了", "Q 不玩了"]

    half_menu(screen, font, title, text)


def load_menu(screen: pygame.Surface, font: pygame.font.Font) -> None:
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    title = "这一关是————"
    text = [f"Stage {stage_text} - {GLOBAL.level} !!", "START!!!!"]

    half_menu(screen, font, title, text)


def talk_menu(screen: pygame.Surface, font: pygame.font.Font) -> None:
    try:
        human = GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["human"]
        text = [
            GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["info"],
            GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["info2"]
        ]

        half_menu(screen, font, human, text)
    except KeyError:
        GLOBAL.is_talk = False


def summary_menu(screen: pygame.Surface, font: pygame.font.Font) -> None:
    combo = 2 ** GLOBAL.combo

    stage = f"Stage {GLOBAL.stage if GLOBAL.stage <= 3 else 'Extra'} - {GLOBAL.level} Cleaer!Hit Z Key."
    text = [
        f"得点 {GLOBAL.total_power} * 512 + {combo} = {GLOBAL.total_power * 512 + combo}",
        f"无闪 {GLOBAL.no_flash} * 4096 = {GLOBAL.no_flash * 4096}"
    ]

    half_menu(screen, font, stage, text)


def start_menu(screen: pygame.Surface, font: pygame.font.Font) -> None:
    title = "锐行 ~ Thunder Out of the Mountain"
    other = "(C)opyright 2026 An_172N"
    text = ['Ver 1.0.6', '', '', '', '']
    key = ["Z 开始", "Q 退出"]

    full_menu(screen, font, title, text, key, other)


def save_menu(screen: pygame.Surface, font: pygame.font.Font) -> None:
    title = "抚形日志"
    name = f"由 {GLOBAL.name} 助记"
    text = [
        f"今天是：{datetime.datetime.now().strftime('%Y-%m-%d')}",
        f"得到了 {GLOBAL.score} 分",
        f"最远到达的地方是 {GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level} 站",
        f"拾形点率为 {Item.calculate_item_rate(GLOBAL.stage_total_power, GLOBAL.stage <= 3, (153, 61))}",
        f"使用了 {GLOBAL.use_flash} 次形闪"
    ]
    key = ["Ent 记录", "ESC 不了"]

    full_menu(screen, font, title, text, key, name)


def full_menu(surface: pygame.Surface, font: pygame.font.Font, title: str, text: list, key: list, other: str) -> None:
    text_type = [
        {"text": title, "pos": (8, 10)},
        {"text": text[0], "pos": (8, 60)},
        {"text": text[1], "pos": (8, 85)},
        {"text": text[2], "pos": (8, 110)},
        {"text": text[3], "pos": (8, 135)},
        {"text": text[4], "pos": (8, 160)},
        {"text": key[0], "pos": (270, 220)},
        {"text": key[1], "pos": (270, 270)},
        {"text": other, "pos": (8, 305)}
    ]

    menu_surface = PRELOAD.picture[5]

    if not GLOBAL.is_blit:
        menu_surface.fill(PRELOAD.color_dict[8])

        for text_info in text_type:
            text = font.render(f"{text_info['text']}", False, PRELOAD.color_dict[6]).convert_alpha()
            menu_surface.blit(text, text_info["pos"])

        GLOBAL.is_blit = True

    surface.blit(menu_surface, (120, 15))


def half_menu(surface: pygame.Surface, font: pygame.font.Font, title: str, text: list) -> None:
    text_type = [
        {"text": title, "pos": (8, 8)},
        {"text": text[0], "pos": (8, 33)},
        {"text": text[1], "pos": (8, 58)}
    ]

    menu_surface = PRELOAD.picture[5].subsurface((0, 0, 345, 85))

    if not GLOBAL.is_blit:
        menu_surface.fill(PRELOAD.color_dict[8])

        for text_info in text_type:
            text = font.render(f"{text_info['text']}", False, PRELOAD.color_dict[6]).convert_alpha()
            menu_surface.blit(text, text_info["pos"])

        GLOBAL.is_blit = True

    surface.blit(menu_surface, (120, 15))


def situation(surface: pygame.Surface, font: pygame.font.Font, text: list, fps: str) -> None:
    text_type = [
        {"text": text[0], "pos": (8, 25)},
        {"text": text[1], "pos": (8, 270)},
        {"text": text[2], "pos": (8, 295)},
        {"text": text[3], "pos": (8, 320)},
        {"text": fps, "pos": (405, 343)}
    ]
    
    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, PRELOAD.color_dict[6])
        surface.blit(text, text_info["pos"])


def display(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    screen.blit(GLOBAL.second_background, (120, 15))

    GLOBAL.bullet_group.draw(screen)
    if GLOBAL.is_visitable:
        GLOBAL.plane_group.draw(screen)
    GLOBAL.brick_group.draw(screen)
    GLOBAL.item_group.draw(screen)
    GLOBAL.particle_group.draw(screen)
    GLOBAL.barrage_group.draw(screen)
    GLOBAL.text_group.draw(screen)

    if not GLOBAL.is_run:
        start_menu(screen, PRELOAD.font)
    elif GLOBAL.is_pause:
        pause_menu(screen, PRELOAD.font)
    elif not GLOBAL.is_level_load:
        load_menu(screen, PRELOAD.font)
    elif GLOBAL.is_talk:
        talk_menu(screen, PRELOAD.font)
    elif GLOBAL.is_summary:
        summary_menu(screen, PRELOAD.font)
    elif GLOBAL.is_save:
        save_menu(screen, PRELOAD.font)

    screen.blit(GLOBAL.background, (0, 0))
    show_situation(screen, PRELOAD.font, clock)