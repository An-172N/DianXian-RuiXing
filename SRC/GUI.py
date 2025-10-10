import pygame as pyg

import TYPE


class GUI:
    def __init__(th, proc):
        th.proc = proc

        th.bg = pyg.image.load('AST\IMG_GAMEBG.png').convert_alpha()

        th.last_time = pyg.time.get_ticks()
        th.fps_txt = th.last_time

        th.arr = TYPE.Arrange(th.proc)

    def show_situ(th):
        curr_time = pyg.time.get_ticks()
        if curr_time - th.last_time >= 500:
            th.fps_txt = f"{th.proc('get', 'main', 'clk').get_fps():.0f} FPS"

            th.last_time = curr_time

        sc = f"分　{th.proc('get', 'pln', 'sc'):9d}"
        sh = (f"形　{th.proc('get', 'pln', 'spt'):02d} , "
              f"{th.proc('get', 'pln', 'ttl_spt'):02d}")
        fl = f"闪　{th.proc('get', 'pln', 'plyr'):02d}"
        comb = (f"连　{th.proc('get', 'item', 'comb'):02d} , "
                f"{th.proc('get', 'blt', 'fusil_cnt'):02d}")

        th.arr.situ(sc,
                    sh,
                    fl,
                    comb,
                    th.fps_txt)
        
    def pau_menu(th):
        th.arr.half_menu("休息ing",
                         "ESC 休息好了",
                         "Q 不玩了")
        
    def ld_menu(th):
        stg = (f"Stage {th.proc('get', 'stg', 'stg')} - "
               f"{th.proc('get', 'stg', 'lv')} !!")

        th.arr.half_menu("这一关是————",
                         stg,
                         "START!!!!")
        
    def talk_menu(th):
        txt = th.proc("get", "stg", "txt")
        
        human = (txt[f"{th.proc('get', 'stg', 'txt_pt')}"]
                 [f"{th.proc('get', 'stg', 'txt_num')}"]
                 ["human"])
        info = (txt[f"{th.proc('get', 'stg', 'txt_pt')}"]
                [f"{th.proc('get', 'stg', 'txt_num')}"]
                ["info"])
        sw = (txt[f"{th.proc('get', 'stg', 'txt_pt')}"]
              [f"{th.proc('get', 'stg', 'txt_num')}"]
              ["sw"])
        
        th.proc("sw", "main", "talk",
                sw)

        th.arr.half_menu(human,
                         info,
                         "")
        
    def summ_menu(th):
        stg = (f"Stage {th.proc('get', 'stg', 'stg')} - "
               f"{th.proc('get', 'stg', 'lv')} Cleaer!")
        pt = (f"得点 {th.proc('get', 'pln', 'ttl_spt')} * 512 "
              f"= {th.proc('get', 'pln', 'ttl_spt') * 512}")
        hurt = (f"无伤 {th.proc('get', 'pln', 'no_hurt')} * 4096 "
                f"= {th.proc('get', 'pln', 'no_hurt') * 4096}")

        th.arr.half_menu(stg,
                         pt,
                         hurt)
        
    def start_menu(th):
        th.arr.full_menu(tit="点线锐山行 ~ Thunder Out of the Mountain",
                         ctl1="Z 开始",
                         ctl2="Q 退出",
                         oth="Copyright (c) 2025 An_172N")
        
    def sav_menu(th):
        dt = f"今天是：{th.proc('func', 'main', 'dt')(True)}"
        sc = f"得到了 {th.proc('get', 'pln', 'sc')} 分"
        name = f"由 {th.proc('get', 'sav', 'name')} 助记"

        th.arr.full_menu(tit="抚形日志",
                         txt1=dt,
                         txt2=sc,
                         ctl1="Ent 记录",
                         ctl2="ESC 不了",
                         oth=name)

    def blit(th):
        th.proc("get", "main", "scr").fill(th.proc("get", "main", "clr")[7])
        th.proc("get", "main", "scr").blit(th.proc("get", "stg", "bg"), (120, 15))

        th.proc("get", "main", "blt_grp").draw(th.proc("get", "main", "scr"))
        if th.proc("get", "pln", "is_visitable"):
            th.proc("get", "main", "pln_grp").draw(th.proc("get", "main", "scr"))
        th.proc("get", "main", "brc_grp").draw(th.proc("get", "main", "scr"))
        th.proc("get", "main", "item_grp").draw(th.proc("get", "main", "scr"))
        th.proc("get", "main", "ptcl_grp").draw(th.proc("get", "main", "scr"))
        th.proc("get", "main", "brg_grp").draw(th.proc("get", "main", "scr"))

        if th.proc('get', 'main', 'run'):
            if th.proc('get', 'main', 'pau'):
                th.pau_menu()
            elif not th.proc('get', 'main', 'lv_ld'):
                th.ld_menu()
            elif th.proc('get', 'main', 'talk'):
                th.talk_menu()
            elif th.proc('get', 'main', 'summ'):
                th.summ_menu()
            elif th.proc('get', 'main', 'sav'):
                th.sav_menu()
        else:
            th.start_menu()

        th.proc("get", "main", "scr").blit(th.bg, (0, 0))

        th.show_situ()

        pyg.display.flip()