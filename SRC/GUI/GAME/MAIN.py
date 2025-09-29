import pygame as pyg


class MainGUI:
    def __init__(th, own):
        th.own = own

        th.last_upd_time = pyg.time.get_ticks()
        th.fps_txt = th.last_upd_time

        th.bg = pyg.image.load('AST\IMG_GAMEBG.png').convert_alpha()
    
    def show_situ(th):
        sc = f"分　{th.own.sc_mgr.sc_cnt:9d}"
        sh = f"形　{th.own.pln_mgr.s_pt:02d} , {th.own.pln_mgr.ttl_s_pt:02d}"
        fl = f"闪　{th.own.pln_mgr.plyr:02d}"
        cmb = f"连　{th.own.item_mgr.comb:02d} , {th.own.blt_mgr.fusil_cnt:02d}"

        th.own.txt_func(sc,
                        (8, 25))
        th.own.txt_func(sh,
                        (8, 270))
        th.own.txt_func(fl,
                        (8, 295))
        th.own.txt_func(cmb,
                        (8, 320))

    def show_time(th):
        tm = f"TIME {th.own.datetime(False)}"

        th.own.txt_func(tm,
                        (280, 344))

    def show_fps(th):
        curr_time = pyg.time.get_ticks()

        if curr_time - th.last_upd_time >= 500:
            get_fps = th.own.clk.get_fps()
            th.fps_txt = f"{get_fps:.0f} FPS"

            th.last_upd_time = curr_time

        th.own.txt_func(th.fps_txt,
                        (405, 344))

    def mask(th):
        th.bg.set_clip(th.own.win)
        th.bg.fill((0, 0, 0, 0))

    def arr(th):
        th.own.scr.fill((0, 0, 0))

        th.own.scr.blit(th.own.stg_mgr.bg, (120, 15))

        th.own.blt_grp.draw(th.own.scr)
        if th.own.pln_mgr.is_visitable:
            th.own.pln_grp.draw(th.own.scr)
        th.own.brc_grp.draw(th.own.scr)
        th.own.item_grp.draw(th.own.scr)
        th.own.ptcl_grp.draw(th.own.scr)
        th.own.brg_grp.draw(th.own.scr)

        th.own.scr.blit(th.bg, (0, 0))

        th.show_situ()
        th.show_time()
        th.show_fps()