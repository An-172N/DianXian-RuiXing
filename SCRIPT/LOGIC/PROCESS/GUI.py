import datetime

import pygame

import SCRIPT.DRAW as DRAW
import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE


def show_situ(screen, font, clock) -> None:
    current_time = pygame.time.get_ticks()
    if current_time - VARIABLE.last_time >= 500:
        VARIABLE.fps_text = f"{clock.get_fps():.0f} FPS"
        VARIABLE.last_time = current_time

    score = f"分　{VARIABLE.score:9d}"
    power = (
        f"形　{VARIABLE.s_power:02d} , "
        f"{VARIABLE.total_s_power:02d}"
    )
    flash = f"闪　{VARIABLE.player:02d}"
    combo = (
        f"连　{VARIABLE.combo:02d} , "
        f"{VARIABLE.shoot_cnt:02d}"
    )

    situ(
        screen, font,
        score,
        power,
        flash,
        combo,
        VARIABLE.fps_text
    )


def pause_menu(screen, font) -> None:
    half_menu(
        screen, font,
        "休息ing",
        "ESC 休息好了",
        "Q 不玩了"
    )


def load_menu(screen, font) -> None:
    stage_text = VARIABLE.stage if VARIABLE.stage <= 3 else f'Extra'

    stage = (
        f"Stage {stage_text} - "
        f"{VARIABLE.level} !!"
    )

    half_menu(
        screen, font,
        "这一关是————",
        stage,
        "START!!!!"
    )


def talk_menu(screen, font) -> None:
    text = VARIABLE.text
        
    human = (
        text[f"{VARIABLE.text_part}"]
        [f"{VARIABLE.text_number}"]
        ["human"]
    )
    info = (
        text[f"{VARIABLE.text_part}"]
        [f"{VARIABLE.text_number}"]
        ["info"]
    )
    info2 = (
        text[f"{VARIABLE.text_part}"]
        [f"{VARIABLE.text_number}"]
        ["info2"]
    )
    sw = (
        text[f"{VARIABLE.text_part}"]
        [f"{VARIABLE.text_number}"]
        ["sw"]
    )
        
    VARIABLE.talk = sw

    half_menu(
        screen, font,
        human,
        info,
        info2
    )


def summary_menu(screen, font) -> None:
    stage_text = VARIABLE.stage if VARIABLE.stage <= 3 else f'Extra'

    stage = (
        f"Stage {stage_text} - "
        f"{VARIABLE.level} Cleaer!"
    )
    point = (
        f"得点 {VARIABLE.total_s_power} * 512 "
        f"= {VARIABLE.total_s_power * 512}"
    )
    hurt = (
        f"无伤 {VARIABLE.no_hurt} * 4096 "
        f"= {VARIABLE.no_hurt * 4096}"
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
    stage_text = VARIABLE.stage if VARIABLE.stage <= 3 else f'Extra'

    tm = f"今天是：{datetime.datetime.now().strftime('%Y-%m-%d')}"
    score = f"得到了 {VARIABLE.score} 分"
    stage = f"最远达到的地方是 {stage_text} - {VARIABLE.level}"
    s_power = f"拾形点率为 {VARIABLE.cal_s_power()}"
    s_flash = f"使用了 {VARIABLE.s_flash} 次形闪"
    name = f"由 {VARIABLE.name} 助记"

    full_menu(
        screen, font,
        title=f"抚形日志",
        text1=tm, text2=score, text3= stage, text4= s_power, text5 = s_flash,
        key1="Ent 记录", key2="ESC 不了", other=name
    )


def full_menu(
    sur, font,
    title="",
    text1="", text2="", text3="", text4="", text5="",
    key1="", key2="",
    other=""
) -> None:
    text_type = [
        {"text": title, "pos": (128, 25)},
        {"text": text1, "pos": (128, 75)},
        {"text": text2, "pos": (128, 100)},
        {"text": text3, "pos": (128, 125)},
        {"text": text4, "pos": (128, 150)},
        {"text": text5, "pos": (128, 175)},
        {"text": key1, "pos": (390, 235)},
        {"text": key2, "pos": (390, 285)},
        {"text": other, "pos": (128, 320)}
    ]

    sur.blit(
        DRAW.ShapeDraw(345, 330, 0, DICT.color_dict[7]).rect(),
        (120, 15)
    )
    
    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, DICT.color_dict[6])
        sur.blit(text, text_info["pos"])


def half_menu(sur, font, title, text1, text2) -> None:
    text_type = [
        {"text": title, "pos": (125, 268)},
        {"text": text1, "pos": (125, 293)},
        {"text": text2, "pos": (125, 318)}
    ]

    sur.blit(
        DRAW.ShapeDraw(345, 85, 0, DICT.color_dict[7]).rect(),
        (120, 260)
    )
    
    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, DICT.color_dict[6])
        sur.blit(text, text_info["pos"])


def situ(sur, font, text1, text2, text3, text4, fps) -> None:
    text_type = [
        {"text": text1, "pos": (8, 25)},
        {"text": text2, "pos": (8, 270)},
        {"text": text3, "pos": (8, 295)},
        {"text": text4, "pos": (8, 320)},
        {"text": fps, "pos": (405, 343)}
    ]
    
    for text_info in text_type:
        text = font.render(f"{text_info['text']}", False, DICT.color_dict[6])
        sur.blit(text, text_info["pos"])