import sys
import os

sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRC'))

import pygame as pyg

import KERNEL
from FUNC import Collide


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
            game.blt_mgr.use_bomb()

            game.pln_grp.update()
            game.blt_grp.update()
            game.brg_grp.update()
            game.item_grp.update()
            game.ptcl_grp.update()
            game.brc_grp.update()

            Collide.rm_spr(game.eff, game.blt_grp)
            Collide.rm_spr(game.eff, game.brg_grp)
            Collide.rm_spr(game.win, game.item_grp)
            Collide.rm_spr(game.win, game.ptcl_grp)

            Collide.chk_coll(game.brg_grp, game.pln_grp,
                             1,
                             game.pln_mgr.coll_brg)
            Collide.chk_coll(game.blt_grp, game.brc_grp,
                             0,
                             game.blt_mgr.blt_coll)
            Collide.chk_coll(game.item_grp, game.pln_grp,
                             0,
                             game.item_mgr.item_coll)

        game.item_mgr.comb_ctr()

        game.stg_mgr.lv_proc()

    game.evt_mgr.chk_key()

    game.game_gui.blit()

    clk.tick(60)