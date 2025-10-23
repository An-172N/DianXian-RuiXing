import pygame as pyg

import DICT
from FUNC import Tool
from FUNC import Save


class GUI:
    def __init__(th, own):
        th.own = own

        th.bg = pyg.image.load('AST\IMG_GAMEBG.png').convert_alpha()

        th.last_time = pyg.time.get_ticks()
        th.fps_txt = th.last_time


    def show_situ(th):
        curr_time = pyg.time.get_ticks()
        if curr_time - th.last_time >= 500:
            th.fps_txt = f"{th.own.clk.get_fps():.0f} FPS"

            th.last_time = curr_time

        sc = f"分　{th.own.pln_mgr.sc:9d}"
        sh = (f"形　{th.own.blt_mgr.spt:02d} , "
              f"{th.own.blt_mgr.ttl_spt:02d}")
        fl = f"闪　{th.own.pln_mgr.plyr:02d}"
        comb = f"连　{th.own.item_mgr.comb:02d}"

        situ(th.own.scr,
             th.own.fnt,
             sc,
             sh,
             fl,
             comb,
             th.fps_txt)
        
    def pau_menu(th):
        half_menu(th.own.scr,
                  th.own.fnt,
                  "休息ing",
                  "ESC 休息好了",
                  "Q 不玩了")
        
    def ld_menu(th):
        stg = (f"Stage {th.own.stg_mgr.stg} - "
               f"{th.own.stg_mgr.lv} !!")

        half_menu(th.own.scr,
                  th.own.fnt,
                  "这一关是————",
                  stg,
                  "START!!!!")
        
    def talk_menu(th):
        txt = th.own.stg_mgr.txt
        
        human = (txt[f"{th.own.stg_mgr.txt_pt}"]
                 [f"{th.own.stg_mgr.txt_num}"]
                 ["human"])
        info = (txt[f"{th.own.stg_mgr.txt_pt}"]
                [f"{th.own.stg_mgr.txt_num}"]
                ["info"])
        sw = (txt[f"{th.own.stg_mgr.txt_pt}"]
              [f"{th.own.stg_mgr.txt_num}"]
              ["sw"])
        
        th.own.talk = sw

        half_menu(th.own.scr,
                  th.own.fnt,
                  human,
                  info,
                  "")
        
    def summ_menu(th):
        stg = (f"Stage {th.own.stg_mgr.stg} - "
               f"{th.own.stg_mgr.lv} Cleaer!")
        pt = (f"得点 {th.own.blt_mgr.ttl_spt} * 512 "
              f"= {th.own.blt_mgr.ttl_spt * 512}")
        hurt = (f"无伤 {th.own.pln_mgr.no_hurt} * 4096 "
                f"= {th.own.pln_mgr.no_hurt * 4096}")

        half_menu(th.own.scr,
                  th.own.fnt,
                  stg,
                  pt,
                  hurt)
        
    def start_menu(th):
        full_menu(th.own.scr,
                  th.own.fnt,
                  tit="点线锐山行 ~ Thunder Out of the Mountain",
                  ctl1="Z 开始",
                  ctl2="Q 退出",
                  oth="Copyright (c) 2025 An_172N")
        
    def sav_menu(th):
        dt = f"今天是：{Tool.get_dt(True)}"
        sc = f"得到了 {th.own.pln_mgr.sc} 分"
        name = f"由 {Save.name} 助记"

        full_menu(th.own.scr,
                  th.own.fnt,
                  tit="抚形日志",
                  txt1=dt,
                  txt2=sc,
                  ctl1="Ent 记录",
                  ctl2="ESC 不了",
                  oth=name)

    def blit(th):
        th.own.scr.fill(DICT.clr_dict[7])
        th.own.scr.blit(th.own.stg_mgr.bg, (120, 15))

        th.own.blt_grp.draw(th.own.scr)
        if th.own.pln_mgr.is_visitable:
            th.own.pln_grp.draw(th.own.scr)
        th.own.brc_grp.draw(th.own.scr)
        th.own.item_grp.draw(th.own.scr)
        th.own.ptcl_grp.draw(th.own.scr)
        th.own.brg_grp.draw(th.own.scr)

        if th.own.run:
            if th.own.pau:
                th.pau_menu()
            elif not th.own.lv_ld:
                th.ld_menu()
            elif th.own.talk:
                th.talk_menu()
            elif th.own.summ:
                th.summ_menu()
            elif th.own.sav:
                th.sav_menu()
        else:
            th.start_menu()

        th.own.scr.blit(th.bg, (0, 0))

        th.show_situ()

        pyg.display.flip()


def full_menu(sur, fnt, tit="",
              txt1="", txt2="", txt3="",
              ctl1="", ctl2="",
              oth=""):
    txt_type = [
        {"txt": tit, "pos": (128, 25)},
        {"txt": txt1, "pos": (128, 75)},
        {"txt": txt2, "pos": (128, 100)},
        {"txt": txt3, "pos": (128, 125)},
        {"txt": ctl1, "pos": (390, 235)},
        {"txt": ctl2, "pos": (390, 285)},
        {"txt": oth, "pos": (128, 320)}
    ]

    Tool.draw_rect(sur,
                   (0, 0, 0),
                   (345, 330, 0),
                   (120, 15))
    
    for txt_info in txt_type:
        Tool.txt_func(sur, (255, 255, 255), fnt,
                      txt_info["txt"], txt_info["pos"])

def half_menu(sur, fnt, tit, txt1, txt2):
    txt_type = [
        {"txt": tit, "pos": (125, 268)},
        {"txt": txt1, "pos": (125, 293)},
        {"txt": txt2, "pos": (125, 318)}
    ]

    Tool.draw_rect(sur,
                   (0, 0, 0),
                   (345, 85, 0),
                   (120, 260))
    
    for txt_info in txt_type:
        Tool.txt_func(sur, (255, 255, 255), fnt,
                      txt_info["txt"], txt_info["pos"])

def situ(sur, fnt, txt1, txt2, txt3, txt4, fps):
    txt_type = [
        {"txt": txt1, "pos": (8, 25)},
        {"txt": txt2, "pos": (8, 270)},
        {"txt": txt3, "pos": (8, 295)},
        {"txt": txt4, "pos": (8, 320)},
        {"txt": fps, "pos": (405, 343)}
    ]

    for txt_info in txt_type:
        Tool.txt_func(sur, (255, 255, 255), fnt,
                      txt_info["txt"], txt_info["pos"])