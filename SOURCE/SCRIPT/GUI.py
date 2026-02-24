# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from datetime import datetime


import pygame as pg


from PRELOAD import picture, color_dict, font
from LOGIC.CALCULATE import update_fps
from SCRIPT import GLOBAL


def situation(screen: pg.Surface, clock: pg.time.Clock) -> None:
    GLOBAL.fps_text, GLOBAL.last_time = update_fps(GLOBAL.fps_text, GLOBAL.last_time, 0, 500, clock)

    text = [
        f"分　{GLOBAL.score:9d}",
        f"形　{GLOBAL.power:02d} , {GLOBAL.total_power:02d}",
        f"闪　{GLOBAL.flash:02d}",
        f"连　{GLOBAL.combo:02d} , {GLOBAL.shoot_count:02d}"
    ]

    ui(screen, text, GLOBAL.fps_text)


def pause(screen: pg.Surface) -> None:
    title = "休息ing"
    text = ["ESC 休息好了", "Q 不玩了"]

    return half_menu(screen, title, text)


def load(screen: pg.Surface) -> None:
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    title = "这一关是————"
    text = [f"Stage {stage_text} - {GLOBAL.level} !!", "START!!!!"]

    return half_menu(screen, title, text, (0, 60, 120, 180))


def talk(screen: pg.Surface) -> None:
    try:
        human = GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["char"]
        text = [
            GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["1"],
            GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"]["2"] if "2" in GLOBAL.text[f"{GLOBAL.text_part}"][f"{GLOBAL.text_number}"] else ''
        ]

        return half_menu(screen, human, text, (0, 6, 12, 12))
    except KeyError:
        GLOBAL.is_talk = False


def summary(screen: pg.Surface) -> None:
    stage = f"Stage {GLOBAL.stage if GLOBAL.stage <= 3 else 'Extra'} - {GLOBAL.level} Cleaer!Hit Z Key."
    text = [
        f"得点 {GLOBAL.total_power} * 512 = {GLOBAL.total_power * 512}",
        f"无闪 {GLOBAL.no_flash} * 4096 = {GLOBAL.no_flash * 4096}"
    ]

    return half_menu(screen, stage, text)


def start(screen: pg.Surface) -> None:
    title = "锐行 ~ Thunder Out of the Mountain"
    other = "(C)opyright 2026 An_172N"
    text = ['Ver 1.0.7', '', '', '', '']
    key = ["Z 开玩", "Q 退了"]

    return full_menu(screen, title, text, key, other)


def save(screen: pg.Surface) -> None:
    title = "抚形日志"
    name = f"由 {GLOBAL.name} 助记"
    text = [
        f"今天是：{datetime.now().strftime('%Y-%m-%d')}",
        f"得到了 {GLOBAL.score} 分",
        f"最远到达的地方是 {GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'} - {GLOBAL.level} 站",
        f"拾形点率为 {GLOBAL.calculate_item_rate(GLOBAL.game_total_power, GLOBAL.stage <= 3, (153, 61))}",
        f"使用了 {GLOBAL.use_flash} 次形闪"
    ]
    key = ["Ent 记录", "ESC 不了"]

    return full_menu(screen, title, text, key, name)


def full_menu(surface: pg.Surface, title: str, text: list, key: list, other: str, interval: tuple=(0, 30, 60, 60)) -> None:
    group = [
        [
            {"text": title, "pos": (8, 10)},
            {"text": other, "pos": (8, 305)}
        ],
        [
            {"text": text[0], "pos": (8, 60)},
            {"text": text[1], "pos": (8, 85)},
            {"text": text[2], "pos": (8, 110)},
            {"text": text[3], "pos": (8, 135)},
            {"text": text[4], "pos": (8, 160)}
        ],
        [
            {"text": key[0], "pos": (270, 220)},
            {"text": key[1], "pos": (270, 270)}
        ]
    ]

    (backdrop := picture[5], backdrop.fill(color_dict[8]))[0]

    menu, GLOBAL.pop_time = pop_animate(backdrop, font, group, GLOBAL.pop_time, interval)

    surface.blit(menu, (120, 15))


def half_menu(surface: pg.Surface, title: str, text: list, interval: tuple=(0, 30, 60, 60)) -> None:
    group = [
        [{"text": title, "pos": (8, 8)}],
        [{"text": text[0], "pos": (8, 33)}],
        [{"text": text[1], "pos": (8, 58)}]
    ]

    (backdrop := picture[5].subsurface((0, 0, 345, 85)), backdrop.fill(color_dict[8]))[0]

    menu, GLOBAL.pop_time = pop_animate(backdrop, font, group, GLOBAL.pop_time, interval)

    surface.blit(menu, (120, 15))


def ui(surface: pg.Surface, text: list, fps: str) -> None:
    text_type = [
        {"text": text[0], "pos": (8, 25)},
        {"text": text[1], "pos": (8, 270)},
        {"text": text[2], "pos": (8, 295)},
        {"text": text[3], "pos": (8, 320)},
        {"text": fps, "pos": (405, 343)}
    ]

    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, color_dict[6])

        surface.blit(text, text_info["pos"])


def pop_animate(surface: pg.Surface, font: pg.font.Font, group: list, timer: int, interval: tuple, color: tuple=(255, 255, 255)) -> tuple:
    def for_text(timer: int, interval: int, gather: list) -> None:
        if timer >= interval:
            for i in gather:
                text = font.render(i["text"], False, color).convert_alpha()

                surface.blit(text, i["pos"])

    for_text(timer, interval[0], group[0])
    for_text(timer, interval[1], group[1])
    for_text(timer, interval[2], group[2])

    if timer < interval[3]:
        timer += 1

    return surface, timer


def display(screen: pg.Surface, clock: pg.time.Clock) -> None:
    screen.blit(GLOBAL.second_backdrop, (120, 15))

    GLOBAL.bullet_group.draw(screen)
    if GLOBAL.is_visitable:
        GLOBAL.plane_group.draw(screen)
    GLOBAL.brick_group.draw(screen)
    GLOBAL.item_group.draw(screen)
    GLOBAL.particle_group.draw(screen)
    GLOBAL.barrage_group.draw(screen)
    GLOBAL.text_group.draw(screen)

    if not GLOBAL.is_run:
        start(screen)
    elif GLOBAL.is_pause:
        pause(screen)
    elif not GLOBAL.is_level_load:
        load(screen)
    elif GLOBAL.is_talk:
        talk(screen)
    elif GLOBAL.is_summary:
        summary(screen)
    elif GLOBAL.is_save:
        save(screen)

    screen.blit(GLOBAL.backdrop, (0, 0))
    situation(screen, clock)

    pg.display.flip()