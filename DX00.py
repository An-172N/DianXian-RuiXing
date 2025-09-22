import pygame as pyg
import sys
import os
# 导入目录
sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRC'))
# 导入Kernel
from CORE.KERNEL.KERNEL import Thunder


pyg.init()
pyg.display.set_caption('DX_RSX')
# 游戏显示
flg = pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN|pyg.SCALED
scr = pyg.display.set_mode((480, 360),
                           flg,
                           vsync=1)
# 游戏字体和时钟
fnt = pyg.font.Font('AST\FNT_GNUUNIFONT.otf', 15)
clk = pyg.time.Clock()

game = Thunder(scr, fnt, clk)

game.game_gui.mask() # 游戏窗口遮罩，只调用一次

while True:
    if (game.run and
        not game.sav_mgr.is_sav):
        if not game.stg_mgr.pau: # 暂停、结算时不能更新
            game.item_mgr.comb_ctr()
                
            if (not game.stg_mgr.summ and
                not game.stg_mgr.talk and
                game.sl_gen.lv_ld):
                game.pln_mgr.upd_pos()
                game.pln_mgr.keep_pos()
                game.pln_mgr.upd_size()
                
                game.life_mgr.respwn()

                game.stg_mgr.mv_shhm()

                game.invinc.lgc()

                game.item_mgr.spwn_regular()
                game.item_mgr.item_upd()

                game.blt_mgr.use_fusil()
                game.blt_mgr.use_bomb()
                game.blt_mgr.upd_blts()

                game.ptcl_mgr.upd()

                game.brg_mgr.upd()

                game.rm_mgr.rm_sprs(game.blt_grp)
                game.rm_mgr.rm_sprs(game.brg_grp)
                game.rm_mgr.rm_sprs(game.item_grp)
                game.rm_mgr.rm_sprs(game.ptcl_grp)

                game.coll_mgr.chk_brg_coll()
                game.coll_mgr.chk_blt_coll()
                game.coll_mgr.chk_item_coll()

            game.sl_gen.lgc()
                
    game.evt_mgr.chk_evt()

    game.game_gui.show_fps()

    game.game_gui.blit()

    clk.tick(60)