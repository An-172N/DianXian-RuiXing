import sys
import os

sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRC'))

import pygame as pyg

import KERNEL
import FUNC


pyg.init()
pyg.display.set_caption('DX_RSX')

flg = pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN|pyg.SCALED
scr = pyg.display.set_mode((480, 360),
                           flg,
                           vsync=1)

fnt = pyg.font.Font('AST\FNT_GNUUNIFONT.otf', 15)
clk = pyg.time.Clock()

game = KERNEL.Thunder(scr, fnt, clk)

info_list = [
    "点线锐山行 ~ Thunder Out of the Mountain",
    "Ver 0.01",
    "Copyright (c) 2025 An_172N",
    "本游戏遵循 GPL 3.0 开源协议",
    " ",
    "(代码写的好寄吧烂"
]
for i in info_list:
    print(i)

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

            [spr.kill() for spr in game.blt_grp
             if not game.eff.collidepoint(spr.rect.center)]
            [spr.kill() for spr in game.brg_grp
             if not game.eff.collidepoint(spr.rect.center)]
            [spr.kill() for spr in game.item_grp
             if not game.win.collidepoint(spr.rect.center)]
            [spr.kill() for spr in game.ptcl_grp
             if not game.win.collidepoint(spr.rect.center)]

            coll1 = FUNC.Process.find_match(game.brg_grp, game.pln_grp,
                                            lambda src, tar: src.rect.collidepoint(tar.rect.center))
            for src, tar in coll1:
                game.pln_mgr.coll_brg(src, tar)
            coll2 = FUNC.Process.find_match(game.blt_grp, game.brc_grp,
                                            lambda src, tar: src.rect.colliderect(tar.rect))
            for src, tar in coll2:
                game.blt_mgr.blt_coll(src, tar)
            coll3 = FUNC.Process.find_match(game.item_grp, game.pln_grp,
                                            lambda src, tar: src.rect.colliderect(tar.rect))
            for src, tar in coll3:
                game.item_mgr.item_coll(src, tar)

        game.item_mgr.comb_ctr()

        game.stg_mgr.lv_proc()

    game.key_mgr.chk_key()

    game.gui.blit()

    clk.tick(60)