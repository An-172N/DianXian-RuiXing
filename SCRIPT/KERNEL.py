import itertools
import sys

import pygame as pyg

import SCRIPT.LOGIC
import SCRIPT.DICT
import SCRIPT.VARIABLE
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

    def update(th):
        if (SCRIPT.VARIABLE.run and
            not SCRIPT.VARIABLE.sav and
            not SCRIPT.VARIABLE.pau):
            if (not SCRIPT.VARIABLE.summ and
                not SCRIPT.VARIABLE.talk and
                SCRIPT.VARIABLE.level_ld):
                if SCRIPT.VARIABLE.is_sdivide:
                    SCRIPT.VARIABLE.main_char.bomb.free()

                th.pln_mgr.turn_side()
                th.pln_mgr.mv_pln()
                th.pln_mgr.invinc()
            
                SCRIPT.VARIABLE.blt_grp.update()
                SCRIPT.VARIABLE.brg_grp.update()
                SCRIPT.VARIABLE.item_grp.update()
                SCRIPT.VARIABLE.ptcl_grp.update()
                SCRIPT.VARIABLE.brc_grp.update()

                [spr.kill() for spr in SCRIPT.VARIABLE.blt_grp
                 if not SCRIPT.VARIABLE.eff.collidepoint(spr.rect.center)]
                [spr.kill() for spr in SCRIPT.VARIABLE.brg_grp
                 if not SCRIPT.VARIABLE.eff.collidepoint(spr.rect.center)]
                [spr.kill() for spr in SCRIPT.VARIABLE.item_grp
                 if not SCRIPT.VARIABLE.eff.collidepoint(spr.rect.center)]
                [spr.kill() for spr in SCRIPT.VARIABLE.ptcl_grp
                 if not SCRIPT.VARIABLE.win.collidepoint(spr.rect.center)]

                for brg in SCRIPT.VARIABLE.brg_grp:
                    if (pyg.sprite.collide_mask(brg, SCRIPT.VARIABLE.d_pt)
                        and brg.clr != (255, 255, 255)):
                            th.pln_mgr.coll_brg(brg)
                coll2 = itertools.product(SCRIPT.VARIABLE.blt_grp, SCRIPT.VARIABLE.brc_grp)
                for src, tar in coll2:
                    if src.rect.colliderect(tar.rect):
                        th.blt_mgr.blt_coll(src, tar)
                coll3 = itertools.product(SCRIPT.VARIABLE.item_grp, SCRIPT.VARIABLE.pln_grp)
                for src, tar in coll3:
                    if src.rect.colliderect(tar.rect):
                        th.item_mgr.item_coll(src, tar)

            th.item_mgr.comb_ctr()

            th.stg_mgr.lv_proc()

        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                sys.exit()
            elif evt.type == pyg.KEYUP:
                if SCRIPT.VARIABLE.run:
                    if evt.key in SCRIPT.DICT.key_dict["up"]["game"]:
                        SCRIPT.DICT.key_dict["up"]["game"][evt.key]()
            elif evt.type == pyg.KEYDOWN:
                if not SCRIPT.VARIABLE.run:
                    if evt.key in SCRIPT.DICT.key_dict["down"]["start"]:
                        SCRIPT.DICT.key_dict["down"]["start"][evt.key]()
                else:
                    if SCRIPT.VARIABLE.sav:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["over"]:
                            SCRIPT.DICT.key_dict["down"]["over"][evt.key]()
                        else:
                            SCRIPT.VARIABLE.name += evt.unicode
                    elif SCRIPT.VARIABLE.pau:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["pau"]:
                            SCRIPT.DICT.key_dict["down"]["pau"][evt.key]()
                    elif SCRIPT.VARIABLE.talk:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["talk"]:
                            SCRIPT.DICT.key_dict["down"]["talk"][evt.key]()
                    elif not SCRIPT.VARIABLE.summ and SCRIPT.VARIABLE.level_ld:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["game"]:
                            SCRIPT.DICT.key_dict["down"]["game"][evt.key]()

        if SCRIPT.VARIABLE.is_rst:
            SCRIPT.RESET.rst1()
            SCRIPT.RESET.rst2()
            SCRIPT.VARIABLE.is_rst = False

        th.scr.fill(SCRIPT.DICT.clr_dict[7])
        th.scr.blit(SCRIPT.VARIABLE.sec_bg, (120, 15))

        SCRIPT.VARIABLE.blt_grp.draw(th.scr)
        if SCRIPT.VARIABLE.is_visitable:
            SCRIPT.VARIABLE.pln_grp.draw(th.scr)
        SCRIPT.VARIABLE.brc_grp.draw(th.scr)
        SCRIPT.VARIABLE.item_grp.draw(th.scr)
        SCRIPT.VARIABLE.ptcl_grp.draw(th.scr)
        SCRIPT.VARIABLE.brg_grp.draw(th.scr)

        if SCRIPT.VARIABLE.run:
            if SCRIPT.VARIABLE.pau:
                th.gui.pau_menu(th.scr, th.fnt)
            elif not SCRIPT.VARIABLE.level_ld:
                th.gui.ld_menu(th.scr, th.fnt)
            elif SCRIPT.VARIABLE.talk:
                th.gui.talk_menu(th.scr, th.fnt)
            elif SCRIPT.VARIABLE.summ:
                th.gui.summ_menu(th.scr, th.fnt)
            elif SCRIPT.VARIABLE.sav:
                th.gui.sav_menu(th.scr, th.fnt)
        else:
            th.gui.start_menu(th.scr, th.fnt)

        th.scr.blit(SCRIPT.VARIABLE.bg, (0, 0))

        th.gui.show_situ(th.scr, th.fnt, th.clk)

        pyg.display.flip()