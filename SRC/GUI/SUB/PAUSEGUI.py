class PauseGUI:
    def __init__(th, own): # 初始化暂停界面
        th.own = own

    def bg_draw(th): # 绘制通用矩形
        th.own.scr.blit(th.own.draw_rect(345, 85, 0,
                                         (0, 0, 0)),
                        (120, 260))
    
    def pau_txt(th, tit, txt1, txt2): # 暂停界面绘制函数
        th.own.scr.blit(th.own.txt_func(tit),
                        (125, 268))
        th.own.scr.blit(th.own.txt_func(txt1),
                        (125, 293))
        th.own.scr.blit(th.own.txt_func(txt2),
                        (125, 318))
    
    def wait_txt(th): # 准备开始界面
        stg = f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv}!!"

        th.own.scr.blit(th.own.txt_func(f"这一关是————"),
                        (125, 268)) # 默认显示标题
        if th.own.sl_gen.cnt >= 30: # 计数器超过30后显示目前关卡
            th.own.scr.blit(th.own.txt_func(stg),
                            (125, 293))
        if th.own.sl_gen.cnt >= 60: # 超过60则提示开始！
            th.own.scr.blit(th.own.txt_func(f"START!!!"),
                            (125, 318))

    def talk_txt(th):
        th.own.scr.blit(th.own.txt_func(th.own.stg_mgr.rt_txt()),
                        (205, 268))

    def blit(th): # 绘制逻辑
        if not th.own.sl_gen.lv_ld:
            th.bg_draw()

            th.wait_txt()
        elif th.own.stg_mgr.pau:
            th.bg_draw()

            th.pau_txt("休息ing", "ESC 休息好了", "Q 不玩了")

            if th.own.stg_mgr.ru_sure:
                th.bg_draw()

                th.pau_txt("不玩了吗？", "Y 不玩了", "N aa，按错了")
        elif th.own.stg_mgr.summ:
            clr = f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv} Cleaer! （Z 下一关）"
            s_pt = f"得点 {th.own.pln_mgr.ttl_s_pt} * 256 = {th.own.sc_mgr.get_pow()}"
            no_h = f"无伤 {th.own.pln_mgr.no_hurt_cnt} * 4096 = {th.own.sc_mgr.no_hurt()}"

            th.bg_draw()
            
            th.pau_txt(clr, s_pt, no_h)
        elif th.own.stg_mgr.talk:
            th.bg_draw()

            th.talk_txt()

            if th.own.stg_mgr.txt_num >= len(th.own.stg_mgr.txt):
                th.own.stg_mgr.talk = False
                th.own.stg_mgr.txt_num = 0