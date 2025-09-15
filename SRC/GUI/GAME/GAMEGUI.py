import pygame as pyg
import datetime as dt


class GameGUI:
    def __init__(th, own): # 文本类初始化
        th.own = own
        # 先初始化帧数显示
        th.last_upd_time = pyg.time.get_ticks()
        th.fps_text = th.own.fnt.render(f"{th.last_upd_time}",
                                        False,
                                        (255, 255, 255))
        # 游戏主背景
        th.bg = pyg.image.load('AST\IMG_GAMEBG.png').convert_alpha()

    def show_situ(th, cnt, state_name, digit, other): # 信息显示函数
        situ = cnt
        text = th.own.fnt.render(f"{state_name}{situ:{digit}}{other}",
                                 False,
                                 (255, 255, 255))

        return text

    def show_time(th): # 显示时间
        hou = dt.datetime.now().hour
        min = dt.datetime.now().minute
        sec = dt.datetime.now().second

        text = th.own.fnt.render(f"TIME {hou:02d}:{min:02d}:{sec:02d}",
                                 False,
                                 (255, 255, 255))
        
        return text

    def show_fps(th): # 显示帧数
        curr_time = pyg.time.get_ticks()

        if curr_time - th.last_upd_time >= 500: # 每隔0.5秒更新一次
            get_fps = th.own.clk.get_fps()
            th.fps_text = th.own.fnt.render(f"{get_fps:.0f} FPS",
                                            False,
                                            (255, 255, 255))
            th.last_upd_time = curr_time

    def mask(th): # 遮罩
        # 设置游戏窗口范围为透明
        th.bg.set_clip(th.own.win)
        th.bg.fill((0, 0, 0, 0))

    def blit(th):
        # 绘制逻辑
        th.own.scr.fill((0, 0, 0)) # 黑色为底
        # 绘制副背景
        th.own.stg_bg = th.own.stg_mgr.get_stg().blit()
        # 绘制精灵
        th.own.blt_grp.draw(th.own.scr)
        if th.own.pln_mgr.is_visitable:
            th.own.pln_grp.draw(th.own.scr)
        th.own.brc_grp.draw(th.own.scr)
        th.own.item_grp.draw(th.own.scr)
        th.own.ptcl_grp.draw(th.own.scr)
        th.own.brg_grp.draw(th.own.scr)
        # 绘制暂停界面和主背景
        th.own.pau_gui.blit()
        th.own.scr.blit(th.bg, (0, 0))
        # 绘制文字
        th.own.scr.blit(th.show_situ(th.own.sc_mgr.sc_cnt,
                                     "分　",
                                     '9d',
                                     ''),
                        (8, 25))
        th.own.scr.blit(th.show_situ(th.own.pln_mgr.s_pt,
                                     "形　",
                                     '02d',
                                     f' , {th.own.pln_mgr.ttl_s_pt:02d}'),
                        (8, 270))
        th.own.scr.blit(th.show_situ(th.own.pln_mgr.plyr,
                                     "残　",
                                     '02d',
                                     ''),
                        (8, 295))
        th.own.scr.blit(th.show_situ(th.own.item_mgr.comb,
                                     "连　",
                                     '02d',
                                     f' , {th.own.blt_mgr.fusil_cnt:02d}'),
                        (8, 320))
        th.own.scr.blit(th.show_time(), (280, 344))
        th.own.scr.blit(th.fps_text, (405, 344))

        pyg.display.flip()