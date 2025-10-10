import pygame as pyg
import sys
import os

sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRC'))

import KERNEL


pyg.init()
pyg.display.set_caption('DX_RSX')

flg = pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN|pyg.SCALED
scr = pyg.display.set_mode((480, 360),
                           flg,
                           vsync=1)

fnt = pyg.font.Font('AST\FNT_GNUUNIFONT.otf', 15)
clk = pyg.time.Clock()

game = KERNEL.Thunder(scr, fnt, clk)

while True:
    if (game.run and
        not game.sav and
        not game.pau):
        if (not game.summ and
            not game.talk and
            game.lv_ld):
            game.item_mgr.spwn_rglr()

            game.blt_mgr.use_fusil()
            game.blt_mgr.use_bomb()

            game.pln_grp.update()
            game.blt_grp.update()
            game.brg_grp.update()
            game.item_grp.update()
            game.ptcl_grp.update()
            game.brc_grp.update()

            game.coll_mgr.rm_spr(game.blt_grp)
            game.coll_mgr.rm_spr(game.brg_grp)
            game.coll_mgr.rm_spr(game.item_grp)
            game.coll_mgr.rm_spr(game.ptcl_grp)

            game.coll_mgr.chk_coll(game.brg_grp, game.pln_grp,
                                   1, True,
                                   game.pln_mgr.coll_brg)
            game.coll_mgr.chk_coll(game.blt_grp, game.brc_grp,
                                   0, True,
                                   game.blt_mgr.blt_coll)
            game.coll_mgr.chk_coll(game.item_grp, game.pln_grp,
                                   0, True,
                                   game.item_mgr.item_coll)

        game.item_mgr.comb_ctr()

        game.stg_mgr.lv_proc()

    game.evt_mgr.chk_key()

    game.game_gui.blit()

    clk.tick(60)