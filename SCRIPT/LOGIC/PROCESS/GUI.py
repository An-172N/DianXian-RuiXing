import datetime

import pygame

import SCRIPT.GLOBAL as GLOBAL


def show_situ(screen, font, clock) -> None:
    current_time = pygame.time.get_ticks()
    if current_time - GLOBAL.last_time >= 500:
        GLOBAL.fps_text = f"{clock.get_fps():.1f} FPS"
        GLOBAL.last_time = current_time

    score = f"分　{GLOBAL.score:9d}"
    power = (
        f"形　{GLOBAL.s_power:02d} , "
        f"{GLOBAL.total_s_power:02d}"
    )
    flash = f"闪　{GLOBAL.player:02d}"
    combo = (
        f"连　{GLOBAL.combo:02d} , "
        f"{GLOBAL.shoot_counter:02d}"
    )

    situ(
        screen, font,
        score,
        power,
        flash,
        combo,
        GLOBAL.fps_text
    )


def pause_menu(screen, font) -> None:
    half_menu(
        screen, font,
        "休息ing",
        "ESC 休息好了",
        "Q 不玩了"
    )


def load_menu(screen, font) -> None:
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    stage = (
        f"Stage {stage_text} - "
        f"{GLOBAL.level} !!"
    )

    half_menu(
        screen, font,
        "这一关是————",
        stage,
        "START!!!!"
    )


def talk_menu(screen, font) -> None:
    text = GLOBAL.text
        
    human = (
        text[f"{GLOBAL.text_part}"]
        [f"{GLOBAL.text_number}"]
        ["human"]
    )
    info = (
        text[f"{GLOBAL.text_part}"]
        [f"{GLOBAL.text_number}"]
        ["info"]
    )
    info2 = (
        text[f"{GLOBAL.text_part}"]
        [f"{GLOBAL.text_number}"]
        ["info2"]
    )
    sw = (
        text[f"{GLOBAL.text_part}"]
        [f"{GLOBAL.text_number}"]
        ["sw"]
    )
        
    GLOBAL.talk = sw

    half_menu(
        screen, font,
        human,
        info,
        info2
    )


def summary_menu(screen, font) -> None:
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    stage = (
        f"Stage {stage_text} - "
        f"{GLOBAL.level} Cleaer!"
    )
    point = (
        f"得点 {GLOBAL.total_s_power} * 512 "
        f"= {GLOBAL.total_s_power * 512}"
    )
    hurt = (
        f"无伤 {GLOBAL.no_hurt} * 4096 "
        f"= {GLOBAL.no_hurt * 4096}"
    )

    half_menu(
        screen, font,
        stage,
        point,
        hurt
    )


def start_menu(screen, font) -> None:
    full_menu(
        screen, font,
        title="锐行 ~ Thunder Out of the Mountain",
        key1="Z 开始", key2="Q 退出",
        other="Copyright (c) 2025 An_172N"
    )


def save_menu(screen, font) -> None:
    stage_text = GLOBAL.stage if GLOBAL.stage <= 3 else f'Extra'

    tm = f"今天是：{datetime.datetime.now().strftime('%Y-%m-%d')}"
    score = f"得到了 {GLOBAL.score} 分"
    stage = f"最远达到的地方是 {stage_text} - {GLOBAL.level}"
    s_power = f"拾形点率为 {GLOBAL.cal_s_power()}"
    s_flash = f"使用了 {GLOBAL.s_flash} 次形闪"
    name = f"由 {GLOBAL.name} 助记"

    full_menu(
        screen, font,
        title=f"抚形日志",
        text1=tm, text2=score, text3= stage, text4= s_power, text5 = s_flash,
        key1="Ent 记录", key2="ESC 不了", other=name
    )


def full_menu(
    surface, font,
    title="",
    text1="", text2="", text3="", text4="", text5="",
    key1="", key2="",
    other=""
) -> None:
    text_type = [
        {"text": title, "pos": (8, 10)},
        {"text": text1, "pos": (8, 60)},
        {"text": text2, "pos": (8, 85)},
        {"text": text3, "pos": (8, 110)},
        {"text": text4, "pos": (8, 135)},
        {"text": text5, "pos": (8, 160)},
        {"text": key1, "pos": (270, 220)},
        {"text": key2, "pos": (270, 270)},
        {"text": other, "pos": (8, 305)}
    ]

    menu_surface = GLOBAL.picture["MENU_BG"]
    if not GLOBAL.is_blit:
        menu_surface.fill((0, 0, 0))

        for text_info in text_type:
            text = font.render(f"{text_info['text']}", False, GLOBAL.color_dict[6])
            menu_surface.blit(text, text_info["pos"])

        GLOBAL.is_blit = True

    surface.blit(
        menu_surface,
        (120, 15)
    )


def half_menu(surface, font, title, text1, text2) -> None:
    text_type = [
        {"text": title, "pos": (8, 8)},
        {"text": text1, "pos": (8, 33)},
        {"text": text2, "pos": (8, 58)}
    ]

    menu_surface = GLOBAL.picture["MENU_BG"].subsurface(
        (
            0, 0,
            345, 85
        )
    )
    if not GLOBAL.is_blit:
        menu_surface.fill((0, 0, 0))

        for text_info in text_type:
            text = font.render(f"{text_info['text']}", False, GLOBAL.color_dict[6])
            menu_surface.blit(text, text_info["pos"])

        GLOBAL.is_blit = True

    surface.blit(
        menu_surface,
        (120, 260)
    )


def situ(surface, font, text1, text2, text3, text4, fps) -> None:
    text_type = [
        {"text": text1, "pos": (8, 25)},
        {"text": text2, "pos": (8, 270)},
        {"text": text3, "pos": (8, 295)},
        {"text": text4, "pos": (8, 320)},
        {"text": fps, "pos": (395, 343)}
    ]
    
    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, GLOBAL.color_dict[6])
        surface.blit(text, text_info["pos"])


def menu_display(screen, font) -> None:
    if not GLOBAL.run:
        start_menu(screen, font)
    elif GLOBAL.pause:
        pause_menu(screen, font)
    elif not GLOBAL.level_load:
        load_menu(screen, font)
    elif GLOBAL.talk:
        talk_menu(screen, font)
    elif GLOBAL.summary:
        summary_menu(screen, font)
    elif GLOBAL.save:
        save_menu(screen, font)


def window_display(screen) -> None:
    screen.fill(GLOBAL.color_dict[7])
    screen.blit(GLOBAL.second_background, (120, 15))

    GLOBAL.bullet_group.draw(screen)
    if GLOBAL.is_visitable:
        GLOBAL.plane_group.draw(screen)
    GLOBAL.brick_group.draw(screen)
    GLOBAL.item_group.draw(screen)
    GLOBAL.particle_group.draw(screen)
    GLOBAL.barrage_group.draw(screen)


def font_display(screen, font, clock) -> None:
    screen.blit(GLOBAL.background, (0, 0))
    show_situ(screen, font, clock)