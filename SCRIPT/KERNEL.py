import itertools
import sys

import pygame as pyg

import SCRIPT.LOGIC
import SCRIPT.DICT
import VARIABLE
import SCRIPT.RESET


class Game:
    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.clk = clk
        th.fnt = fnt

        th.pln_mgr = SCRIPT.LOGIC.PlaneMgr
        th.stg_mgr = SCRIPT.LOGIC.StageMgr
        th.blt_mgr = SCRIPT.LOGIC.BulletMgr
        th.item_mgr = SCRIPT.LOGIC.ItemMgr
        th.key_mgr = SCRIPT.LOGIC.Key
        th.gui = SCRIPT.LOGIC.GUI

    def update(th) -> None:
        if (VARIABLE.run and
            not VARIABLE.sav and
            not VARIABLE.pau):
            if (not VARIABLE.summ and
                not VARIABLE.talk and
                VARIABLE.level_ld):
                if VARIABLE.is_sdivide:
                    VARIABLE.main_char.bomb.free()

                th.pln_mgr.turn_side()
                th.pln_mgr.mv_pln()
                th.pln_mgr.invinc()
            
                VARIABLE.blt_grp.update()
                VARIABLE.brg_grp.update()
                VARIABLE.item_grp.update()
                VARIABLE.ptcl_grp.update()
                VARIABLE.brc_grp.update()

                [spr.kill() for spr in VARIABLE.blt_grp
                 if not VARIABLE.eff.collidepoint(spr.rect.center)]
                [spr.kill() for spr in VARIABLE.brg_grp
                 if not VARIABLE.eff.collidepoint(spr.rect.center)]
                [spr.kill() for spr in VARIABLE.item_grp
                 if not VARIABLE.eff.collidepoint(spr.rect.center)]
                [spr.kill() for spr in VARIABLE.ptcl_grp
                 if not VARIABLE.win.collidepoint(spr.rect.center)]

                for brg in VARIABLE.brg_grp:
                    if (pyg.sprite.collide_mask(brg, VARIABLE.d_pt)
                        and brg.clr != (255, 255, 255)):
                            th.pln_mgr.coll_brg(brg)
                coll2 = itertools.product(VARIABLE.blt_grp, VARIABLE.brc_grp)
                for src, tar in coll2:
                    if src.rect.colliderect(tar.rect):
                        th.blt_mgr.blt_coll(src, tar)
                coll3 = itertools.product(VARIABLE.item_grp, VARIABLE.pln_grp)
                for src, tar in coll3:
                    if src.rect.colliderect(tar.rect):
                        th.item_mgr.item_coll(src, tar)

            th.item_mgr.comb_ctr()

            th.stg_mgr.lv_proc()

        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                sys.exit()
            elif evt.type == pyg.KEYUP:
                if VARIABLE.run:
                    if evt.key in SCRIPT.DICT.key_dict["up"]["game"]:
                        SCRIPT.DICT.key_dict["up"]["game"][evt.key]()
            elif evt.type == pyg.KEYDOWN:
                if not VARIABLE.run:
                    if evt.key in SCRIPT.DICT.key_dict["down"]["start"]:
                        SCRIPT.DICT.key_dict["down"]["start"][evt.key]()
                else:
                    if VARIABLE.sav:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["over"]:
                            SCRIPT.DICT.key_dict["down"]["over"][evt.key]()
                        else:
                            VARIABLE.name += evt.unicode
                    elif VARIABLE.pau:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["pau"]:
                            SCRIPT.DICT.key_dict["down"]["pau"][evt.key]()
                    elif VARIABLE.talk:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["talk"]:
                            SCRIPT.DICT.key_dict["down"]["talk"][evt.key]()
                    elif not VARIABLE.summ and VARIABLE.level_ld:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["game"]:
                            SCRIPT.DICT.key_dict["down"]["game"][evt.key]()

        if VARIABLE.is_rst:
            SCRIPT.RESET.rst1()
            SCRIPT.RESET.rst2()
            VARIABLE.is_rst = False

        th.scr.fill(SCRIPT.DICT.clr_dict[7])
        th.scr.blit(VARIABLE.sec_bg, (120, 15))

        VARIABLE.blt_grp.draw(th.scr)
        if VARIABLE.is_visitable:
            VARIABLE.pln_grp.draw(th.scr)
        VARIABLE.brc_grp.draw(th.scr)
        VARIABLE.item_grp.draw(th.scr)
        VARIABLE.ptcl_grp.draw(th.scr)
        VARIABLE.brg_grp.draw(th.scr)

        if VARIABLE.run:
            if VARIABLE.pau:
                th.gui.pau_menu(th.scr, th.fnt)
            elif not VARIABLE.level_ld:
                th.gui.ld_menu(th.scr, th.fnt)
            elif VARIABLE.talk:
                th.gui.talk_menu(th.scr, th.fnt)
            elif VARIABLE.summ:
                th.gui.summ_menu(th.scr, th.fnt)
            elif VARIABLE.sav:
                th.gui.sav_menu(th.scr, th.fnt)
        else:
            th.gui.start_menu(th.scr, th.fnt)

        th.scr.blit(VARIABLE.bg, (0, 0))

        th.gui.show_situ(th.scr, th.fnt, th.clk)

        pyg.display.flip()