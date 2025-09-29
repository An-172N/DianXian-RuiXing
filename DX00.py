import pygame as pyg
import sys
import os

sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRC'))

from CORE.KERNEL.KERNEL import Thunder


pyg.init()
pyg.display.set_caption('DX_RSX')

flg = pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN|pyg.SCALED
scr = pyg.display.set_mode((480, 360),
                           flg,
                           vsync=1)

fnt = pyg.font.Font('AST\FNT_GNUUNIFONT.otf', 15)
clk = pyg.time.Clock()

game = Thunder(scr, fnt, clk)

game.main_gui.mask()

while True:
    if (game.run and
        not game.stg_mgr.sav and
        not game.stg_mgr.pau):
        if (not game.stg_mgr.summ and
            not game.stg_mgr.talk and
            game.sl_gen.lv_ld):
            game.pln_mgr.upd_pos()
            game.pln_mgr.keep_pos()
            game.pln_mgr.upd_size()

            game.life_mgr.invinc()

            game.item_mgr.spwn_rglr()

            game.blt_mgr.use_fusil()
            game.blt_mgr.use_bomb()

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
                                   1,
                                   game.coll_mgr.brg_coll)
            game.coll_mgr.chk_coll(game.blt_grp, game.brc_grp,
                                   0,
                                   game.coll_mgr.blt_coll)
            game.coll_mgr.chk_coll(game.item_grp, game.pln_grp,
                                   0,
                                   game.coll_mgr.item_coll)

        game.item_mgr.comb_ctr()

        game.sl_gen.sl_proc()

    game.evt_mgr.chk_evt()

    game.main_gui.arr()
    if game.run:
        game.pau_gui.arr()

        if game.stg_mgr.sav:
            game.sav_gui.arr()
    else:
        game.start_gui.arr()

    pyg.display.flip()
    clk.tick(60)