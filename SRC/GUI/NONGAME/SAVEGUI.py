class SaveGUI:
    def __init__(th, own):
        th.own = own

    def bg_draw(th):
        th.own.scr.blit(th.own.draw_rect(345, 330, 0,
                                         (0, 0, 0)),
                        (120, 15))

    def title_txt(th):
        th.own.scr.blit(th.own.txt_func(f"抚形日志"),
                        (128, 25))
        th.own.scr.blit(th.own.txt_func("Ent 记录"),
                        (390, 235))
        th.own.scr.blit(th.own.txt_func("ESC 不了"),
                        (390, 285))

    def info_txt(th):
        dt = f"今天是：{th.own.date()}"
        sc = f"得到了 {th.own.sc_mgr.sc_cnt} 分"
        stg = f"最远去到 {th.own.stg_mgr.stg} - {th.own.stg_mgr.lv} 站"
        item = f"收形点率是 {th.own.sav_mgr.cnt_item_coll()}"
        name = f"由 {th.own.sav_mgr.name} 助记"

        th.own.scr.blit(th.own.txt_func(dt),
                        (128, 75))
        th.own.scr.blit(th.own.txt_func(sc),
                        (128, 100))
        th.own.scr.blit(th.own.txt_func(stg),
                        (128, 125))
        th.own.scr.blit(th.own.txt_func(item),
                        (128, 150))
        th.own.scr.blit(th.own.txt_func(name),
                        (128, 320))
    
    def blit(th):
        th.bg_draw()

        th.title_txt()
        th.info_txt()