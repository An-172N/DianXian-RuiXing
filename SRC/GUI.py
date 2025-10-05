import pygame as pyg

import TYPE


class GUI:
    def __init__(th, own):
        th.own = own

        th.bg = pyg.image.load('AST\IMG_GAMEBG.png').convert_alpha()

        th.last_time = pyg.time.get_ticks()
        th.fps_txt = th.last_time

        th.arr = TYPE.Arrange(th.own)

    def show_situ(th):
        curr_time = pyg.time.get_ticks()
        if curr_time - th.last_time >= 500:
            th.fps_txt = f"{th.own.clk.get_fps():.0f} FPS"

            th.last_time = curr_time

        sc = f"分　{th.own.sc_mgr.sc_cnt:9d}"
        sh = f"形　{th.own.pln_mgr.s_pt:02d} , {th.own.pln_mgr.ttl_s_pt:02d}"
        fl = f"闪　{th.own.pln_mgr.plyr:02d}"
        comb = f"连　{th.own.item_mgr.comb:02d} , {th.own.blt_mgr.fusil_cnt:02d}"

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
        stg = f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv} !!"

        th.arr.half_menu("这一关是————",
                         stg,
                         "START!!!!")
        
    def talk_menu(th):
        txt = th.own.stg_mgr.rt_txt()

        th.arr.half_menu(txt[0],
                         txt[1],
                         "")
        
        th.own.talk = txt[2]
        
    def summ_menu(th):
        stg = f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv} Cleaer!"
        pt = f"得点 {th.own.pln_mgr.ttl_s_pt} * 512 = {th.own.sc_mgr.get_pow()}"
        hurt = f"无伤 {th.own.pln_mgr.no_hurt_cnt} * 4096 = {th.own.sc_mgr.no_hurt()}"

        th.arr.half_menu(stg,
                         pt,
                         hurt)
        
    def start_menu(th):
        th.arr.full_menu(tit="点线锐山行 ~ Thunder Out of the Mountain",
                         ctl1="Z 开始",
                         ctl2="Q 退出",
                         oth="Copyright (c) 2025 An_172N")
        
    def sav_menu(th):
        dt = f"今天是：{th.own.datetime(True)}"
        sc = f"得到了 {th.own.sc_mgr.sc_cnt} 分"
        name = f"由 {th.own.sav_mgr.name} 助记"

        th.arr.full_menu(tit="抚形日志",
                         txt1=dt,
                         txt2=sc,
                         ctl1="Ent 记录",
                         ctl2="ESC 不了",
                         oth=name)

    def blit(th):
        th.own.scr.fill(th.own.clr_dict[7])
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

        th.own.clk.tick(60)
        pyg.display.flip()