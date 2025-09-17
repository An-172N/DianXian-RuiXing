import pygame as pyg

from BRICK.BASE.BASESHAPE import BaseShape

class PauseGUI:
    def __init__(th, own): # 初始化暂停界面
        th.own = own

    def draw_rect(th): # 绘制通用矩形
        surface = pyg.Surface((345, 85), pyg.SRCALPHA)

        pyg.draw.rect(surface, (0, 0, 0),
                      surface.get_rect(),
                      0)

        return surface
    
    def pau_draw(th, title, text1, text2): # 暂停界面绘制函数
        title_t = th.own.fnt.render(f"{title}",
                                    False,
                                    (255, 255, 255))
        fst_text = th.own.fnt.render(f"{text1}",
                                     False,
                                     (255, 255, 255))
        sec_text = th.own.fnt.render(f"{text2}",
                                     False,
                                     (255, 255, 255))

        th.own.scr.blit(th.draw_rect(), (120, 260))
        th.own.scr.blit(title_t, (125, 268))
        th.own.scr.blit(fst_text, (125, 293))
        th.own.scr.blit(sec_text, (125, 318))
    
    def wait_draw(th): # 准备开始界面
        title = th.own.fnt.render(f"这一关是————",
                                  False,
                                  (255, 255, 255))
        text1 = th.own.fnt.render(f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv}!!",
                                  False,
                                  (255, 255, 255))
        text2 = th.own.fnt.render(f"START!!!",
                                  False,
                                  (255, 255, 255))

        th.own.scr.blit(th.draw_rect(), (120, 260))
        th.own.scr.blit(title, (125, 268)) # 默认显示标题
        if th.own.sl_gen.cnt >= 30: # 计数器超过30后显示目前关卡
            th.own.scr.blit(text1, (125, 293))
        if th.own.sl_gen.cnt >= 60: # 超过60则提示开始！
            th.own.scr.blit(text2, (125, 318))

    def talk_draw(th):
        text = th.own.fnt.render(th.own.stg_mgr.rt_text(),
                                 False,
                                 (255, 255, 255))

        th.own.scr.blit(th.draw_rect(), (120, 260))
        th.own.scr.blit(text, (205, 268))

    def blit(th): # 绘制逻辑
        if not th.own.sl_gen.lv_ld:
            th.wait_draw()
        elif th.own.stg_mgr.pau:
            th.pau_draw("休息ing", "ESC 休息好了", "Q 不玩了")

            if th.own.stg_mgr.ru_sure:
                th.pau_draw("不玩了吗？", "Y 不玩了", "N aa，按错了")
        elif th.own.stg_mgr.summ:
            th.pau_draw(f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv} Cleaer! （Z 下一关）",
                        f"得点 {th.own.pln_mgr.ttl_s_pt} * 256 = {th.own.sc_mgr.get_pow()}",
                        f"无伤 {th.own.pln_mgr.no_hurt_cnt} * 4096 = {th.own.sc_mgr.no_hurt()}")
        elif th.own.stg_mgr.talk:
            th.talk_draw()

            if th.own.stg_mgr.talk_text >= len(th.own.stg_mgr.curr_stg.text()):
                th.own.stg_mgr.talk = False
                th.own.stg_mgr.talk_text = 0