import argparse
import sys
import os

import pygame as pyg

import SCRIPT.LOGIC
import SCRIPT.DICT
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.RESET


class Game:
    def __init__(th, scr):
        pyg.display.set_icon(pyg.image.load(os.path.join(SCRIPT.RESET.asset_path, 'IMG_ICON.png')))

        th.scr = scr
        th.clk = pyg.time.Clock()
        th.fnt = pyg.font.Font(os.path.join(SCRIPT.RESET.asset_path, 'FNT\FNT_GNUUNIFONT.otf'), 15)

        th.pln_mgr = SCRIPT.LOGIC.PlaneMgr
        th.stg_mgr = SCRIPT.LOGIC.StageMgr
        th.blt_mgr = SCRIPT.LOGIC.BulletMgr
        th.item_mgr = SCRIPT.LOGIC.ItemMgr
        th.key_mgr = SCRIPT.LOGIC.Key
        th.gui = SCRIPT.LOGIC.GUI

        th.option()

    def option(th) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--stage',
            type=int,
            default=1
        )
        parser.add_argument(
            '--level',
            type=int,
            default=0
        )
        parser.add_argument(
            '--player',
            type=int,
            default=4
        )
        parser.add_argument(
            '--s_power',
            type=int,
            default=0
        )
        args = parser.parse_args()
        VARIABLE.stage = args.stage
        VARIABLE.level = args.level
        VARIABLE.player = args.player
        VARIABLE.s_power = args.s_power

    @staticmethod
    def remove_sprite(sprite_group, effective_range) -> None:
        [spr.kill() for spr in sprite_group
         if not effective_range.collidepoint(spr.rect.center)]

    def update(th) -> None:
        while True:
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
                    th.item_mgr.item_spwn_regular()
                    th.blt_mgr.spwn_blt()
            
                    VARIABLE.blt_grp.update()
                    VARIABLE.brg_grp.update()
                    VARIABLE.item_grp.update()
                    VARIABLE.ptcl_grp.update()
                    VARIABLE.brc_grp.update()

                    th.remove_sprite(VARIABLE.blt_grp, VARIABLE.eff)
                    th.remove_sprite(VARIABLE.brg_grp, VARIABLE.eff)
                    th.remove_sprite(VARIABLE.item_grp, VARIABLE.eff)
                    th.remove_sprite(VARIABLE.ptcl_grp, VARIABLE.win)

                    coll1 = pyg.sprite.spritecollide(VARIABLE.d_pt, VARIABLE.brg_grp, False, pyg.sprite.collide_mask)
                    for brg in coll1:
                        if brg.clr != (255, 255, 255):
                            th.pln_mgr.coll_brg(brg)
                    coll2 = pyg.sprite.groupcollide(VARIABLE.blt_grp, VARIABLE.brc_grp, False, False)
                    for blt, hit_brcs in coll2.items():
                        for brc in hit_brcs:
                            th.blt_mgr.blt_coll(blt, brc)
                    coll3 = pyg.sprite.spritecollide(VARIABLE.main_char, VARIABLE.item_grp, False)
                    for item in coll3:
                        th.blt_mgr.item_coll(item)

                th.item_mgr.comb_ctr()

                th.stg_mgr.lv_proc()

            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    sys.exit()
                elif evt.type == pyg.KEYUP:
                    if (VARIABLE.run
                        and evt.key in SCRIPT.DICT.key_dict["up"]["game"]):
                        SCRIPT.DICT.key_dict["up"]["game"][evt.key]()
                elif evt.type == pyg.KEYDOWN:
                    if (not VARIABLE.run
                        and evt.key in SCRIPT.DICT.key_dict["down"]["start"]):
                        SCRIPT.DICT.key_dict["down"]["start"][evt.key]()
                    elif VARIABLE.sav:
                        if evt.key in SCRIPT.DICT.key_dict["down"]["over"]:
                            SCRIPT.DICT.key_dict["down"]["over"][evt.key]()
                        else:
                            VARIABLE.name += evt.unicode
                    elif (VARIABLE.pau
                          and evt.key in SCRIPT.DICT.key_dict["down"]["pau"]):
                        SCRIPT.DICT.key_dict["down"]["pau"][evt.key]()
                    elif (VARIABLE.talk
                          and evt.key in SCRIPT.DICT.key_dict["down"]["talk"]):
                        SCRIPT.DICT.key_dict["down"]["talk"][evt.key]()
                    elif (not VARIABLE.summ
                          and VARIABLE.level_ld
                          and evt.key in SCRIPT.DICT.key_dict["down"]["game"]):
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

            if not VARIABLE.run:
                th.gui.start_menu(th.scr, th.fnt)
            elif VARIABLE.pau:
                th.gui.pau_menu(th.scr, th.fnt)
            elif not VARIABLE.level_ld:
                th.gui.ld_menu(th.scr, th.fnt)
            elif VARIABLE.talk:
                th.gui.talk_menu(th.scr, th.fnt)
            elif VARIABLE.summ:
                th.gui.summ_menu(th.scr, th.fnt)
            elif VARIABLE.sav:
                th.gui.sav_menu(th.scr, th.fnt)

            th.scr.blit(VARIABLE.bg, (0, 0))

            th.gui.show_situ(th.scr, th.fnt, th.clk)

            pyg.display.flip()

            th.clk.tick(60)