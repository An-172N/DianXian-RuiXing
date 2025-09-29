class PauseGUI:
    def __init__(th, own):
        th.own = own

    def pau(th):
        th.own.draw_rect(345, 85, 0,
                             (0, 0, 0),
                             (120, 260))
        th.own.txt_func("休息ing",
                        (125, 268))
        th.own.txt_func("ESC 休息好了",
                        (125, 293))
        th.own.txt_func("Q 不玩了",
                        (125, 318))
        
    def ld(th):
        stg = f"Stage {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv} !!"

        th.own.draw_rect(345, 85, 0,
                         (0, 0, 0),
                         (120, 260))
        th.own.txt_func("这一关是————",
                        (125, 268))
        if th.own.sl_gen.ctr >= 30:
            th.own.txt_func(stg,
                            (125, 293))
        if th.own.sl_gen.ctr >= 60:
            th.own.txt_func("START!!!!",
                            (125, 318))
        
    def summ(th):
        stg_mgr = th.own.stg_mgr
        pln_mgr = th.own.pln_mgr
        sc_mgr = th.own.sc_mgr

        stg = f"Stage {stg_mgr.stg} - {stg_mgr.lv} Cleaer! （Z 下一关）"
        pt = f"得点 {pln_mgr.ttl_s_pt} * 512 = {sc_mgr.get_pow()}"
        hurt = f"无伤 {pln_mgr.no_hurt_cnt} * 4096 = {sc_mgr.no_hurt()}"
            
        th.own.draw_rect(345, 85, 0,
                         (0, 0, 0),
                         (120, 260))
        th.own.txt_func(stg,
                        (125, 268))
        th.own.txt_func(pt,
                        (125, 293))
        th.own.txt_func(hurt,
                        (125, 318))
        
    def talk(th):
        txt = th.own.stg_mgr.rt_txt()

        th.own.draw_rect(345, 85, 0,
                         (0, 0, 0),
                         (120, 260))
        th.own.txt_func(txt[0],
                        (125, 268))
        th.own.txt_func(txt[1],
                            (125, 293))
        th.own.txt_func("",
                        (125, 318))

    def arr(th):
        if th.own.stg_mgr.pau:
            th.pau()
        elif not th.own.sl_gen.lv_ld:
            th.ld()
        elif th.own.stg_mgr.summ:
            th.summ()
        elif th.own.stg_mgr.talk:
            try:
                th.talk()
            except KeyError:
                th.own.stg_mgr.talk = False