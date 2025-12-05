import datetime as dt

import pygame as pyg

import SCRIPT.DRAW
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.SPRITE import ITEM


def show_situ(scr, fnt, clk) -> None:
    curr_time = pyg.time.get_ticks()
    if curr_time - VARIABLE.last_time >= 500:
        VARIABLE.fps_txt = f"{clk.get_fps():.0f} FPS"

        VARIABLE.last_time = curr_time

    sc = f"分　{VARIABLE.sc:9d}"
    sh = (f"形　{VARIABLE.s_power:02d} , "
          f"{VARIABLE.ttl_s_power:02d}")
    fl = f"闪　{VARIABLE.player:02d}"
    comb = (f"连　{VARIABLE.comb:02d} , "
            f"{VARIABLE.shoot_cnt:02d}")

    situ(scr,
         fnt,
         sc,
         sh,
         fl,
         comb,
         VARIABLE.fps_txt)


def pau_menu(scr, fnt) -> None:
    half_menu(scr,
              fnt,
              "休息ing",
              "ESC 休息好了",
              "Q 不玩了")


def ld_menu(scr, fnt) -> None:
    stg = (f"Stage {VARIABLE.stage} - "
           f"{VARIABLE.level} !!")

    half_menu(scr,
              fnt,
              "这一关是————",
              stg,
              "START!!!!")


def talk_menu(scr, fnt) -> None:
    txt = VARIABLE.txt
        
    human = (txt[f"{VARIABLE.txt_pt}"]
             [f"{VARIABLE.txt_num}"]
             ["human"])
    info = (txt[f"{VARIABLE.txt_pt}"]
            [f"{VARIABLE.txt_num}"]
            ["info"])
    info2 = (txt[f"{VARIABLE.txt_pt}"]
            [f"{VARIABLE.txt_num}"]
            ["info2"])
    sw = (txt[f"{VARIABLE.txt_pt}"]
          [f"{VARIABLE.txt_num}"]
          ["sw"])
        
    VARIABLE.talk = sw

    half_menu(scr,
              fnt,
              human,
              info,
              info2)


def summ_menu(scr, fnt) -> None:
    stg = (f"Stage {VARIABLE.stage} - "
           f"{VARIABLE.level} Cleaer!")
    pt = (f"得点 {VARIABLE.ttl_s_power} * 512 "
          f"= {VARIABLE.ttl_s_power * 512}")
    hurt = (f"无伤 {VARIABLE.no_hurt} * 4096 "
            f"= {VARIABLE.no_hurt * 4096}")

    half_menu(scr,
              fnt,
              stg,
              pt,
              hurt)


def start_menu(scr, fnt) -> None:
    full_menu(scr,
              fnt,
              tit="锐行 ~ Thunder Out of the Mountain",
              ctl1="Z 开始",
              ctl2="Q 退出",
              oth="Copyright (c) 2025 An_172N")


def sav_menu(scr, fnt) -> None:
    tm = f"今天是：{dt.datetime.now().strftime('%Y-%m-%d')}"
    sc = f"得到了 {VARIABLE.sc} 分"
    stg = f"最远达到的地方是 {VARIABLE.stage} - {VARIABLE.level}"
    s_power = f"拾形点率为 {ITEM.cal_s_power()}"
    sflash = f"使用了 {VARIABLE.sflash} 次形闪"
    name = f"由 {VARIABLE.name} 助记"

    full_menu(scr,
              fnt,
              tit=f"抚形日志",
              txt1=tm,
              txt2=sc,
              txt3= stg,
              txt4= s_power,
              txt5 = sflash,
              ctl1="Ent 记录",
              ctl2="ESC 不了",
              oth=name)


def full_menu(sur, fnt, tit="",
              txt1="", txt2="", txt3="", txt4="", txt5="",
              ctl1="", ctl2="",
              oth="") -> None:
    txt_type = [
        {"txt": tit, "pos": (128, 25)},
        {"txt": txt1, "pos": (128, 75)},
        {"txt": txt2, "pos": (128, 100)},
        {"txt": txt3, "pos": (128, 125)},
        {"txt": txt4, "pos": (128, 150)},
        {"txt": txt5, "pos": (128, 175)},
        {"txt": ctl1, "pos": (390, 235)},
        {"txt": ctl2, "pos": (390, 285)},
        {"txt": oth, "pos": (128, 320)}
    ]

    sur.blit(SCRIPT.DRAW.ShapeDraw(345, 330, 0, (0, 0, 0)).rect(),
             (120, 15))
    
    for txt_info in txt_type:
        txt = fnt.render(f"{txt_info['txt']}", False, (255, 255, 255))
        sur.blit(txt, txt_info["pos"])


def half_menu(sur, fnt, tit, txt1, txt2) -> None:
    txt_type = [
        {"txt": tit, "pos": (125, 268)},
        {"txt": txt1, "pos": (125, 293)},
        {"txt": txt2, "pos": (125, 318)}
    ]

    sur.blit(SCRIPT.DRAW.ShapeDraw(345, 85, 0, (0, 0, 0)).rect(),
             (120, 260))
    
    for txt_info in txt_type:
        txt = fnt.render(f"{txt_info['txt']}", False, (255, 255, 255))
        sur.blit(txt, txt_info["pos"])


def situ(sur, fnt, txt1, txt2, txt3, txt4, fps) -> None:
    txt_type = [
        {"txt": txt1, "pos": (8, 25)},
        {"txt": txt2, "pos": (8, 270)},
        {"txt": txt3, "pos": (8, 295)},
        {"txt": txt4, "pos": (8, 320)},
        {"txt": fps, "pos": (405, 343)}
    ]
    
    for txt_info in txt_type:
        txt = fnt.render(f"{txt_info['txt']}", False, (255, 255, 255))
        sur.blit(txt, txt_info["pos"])