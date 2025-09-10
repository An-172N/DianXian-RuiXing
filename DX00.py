import pygame as pyg
import sys
import os
# 导入目录
sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRC'))
# 导入开始界面
from GUI.NONGAME.STARTGUI import StartGUI
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
fnt = pyg.font.Font('AST\FONT_GNUUNIFONT.otf', 15)
clk = pyg.time.Clock()

run = True

while True:
    if not run: # 游戏
        game = Thunder(scr, fnt, clk)

        game.game_gui.mask() # 游戏窗口遮罩，只调用一次

        while not run: # 其余为循环
            if not game.stg_mgr.pau: # 暂停、结算时不能更新
                game.item_mgr.combo_ctr()
                
                if (not game.stg_mgr.summ
                    and game.sl_gen.lv_ld
                    and not game.stg_mgr.talk):
                    game.pln_mgr.upd_pos()
                    game.pln_mgr.upd_size()
                    game.pln_mgr.respwn()
                    game.stg_mgr.mv_shhm()

                    game.invinc.lgc()

                    game.item_mgr.spwn_regular()
                    game.item_mgr.item_upd()

                    game.blt_mgr.fusillade()
                    game.blt_mgr.upd_blts()

                    game.ptcl_mgr.upd()

                    game.bomb_mgr.use_bomb()

                    game.brg_mgr.upd()

                    game.rm_mgr.rm_sprs(game.blt_grp)
                    game.rm_mgr.rm_sprs(game.brg_grp)
                    game.rm_mgr.rm_sprs(game.item_grp)
                    game.rm_mgr.rm_sprs(game.ptcl_grp)

                    game.coll_mgr.chk_brg_coll()
                    game.coll_mgr.chk_blt_coll()
                    game.coll_mgr.chk_item_coll()

            game.sl_gen.lgc()

            game.game_gui.show_fps()
                
            for evt in pyg.event.get():
                if evt.type == pyg.QUIT: # 保证可以退出
                    sys.exit()
                elif evt.type == pyg.KEYUP: # 按完后操作
                    if evt.key == pyg.K_z:
                        game.blt_mgr.is_cnt_fusillade = False
                    if evt.key == pyg.K_RIGHT:
                        game.pln_mgr.mv_right = False
                    if evt.key == pyg.K_LEFT:
                        game.pln_mgr.mv_left = False
                    if evt.key == pyg.K_LSHIFT:
                        game.pln_mgr.set_pln_spd(0)
                elif evt.type == pyg.KEYDOWN: # 按下操作
                    if not game.stg_mgr.summ: # 非结算界面操作
                        if (not game.stg_mgr.pau
                            and not game.stg_mgr.talk): # 游戏主要操作
                            if evt.key == pyg.K_RIGHT:
                                game.pln_mgr.mv_right = True
                            if evt.key == pyg.K_LEFT:
                                game.pln_mgr.mv_left = True
                            if evt.key == pyg.K_LSHIFT:
                                game.pln_mgr.set_pln_spd(1)
                            if evt.key == pyg.K_z:
                                game.blt_mgr.is_cnt_fusillade = True
                            if evt.key == pyg.K_x:
                                game.bomb_mgr.single_bomb()
                            if evt.key == pyg.K_ESCAPE:
                                game.stg_mgr.pau_evt()
                        elif (game.stg_mgr.talk
                              and not game.stg_mgr.pau
                              and game.sl_gen.lv_ld):
                            if evt.key == pyg.K_z:
                                game.stg_mgr.talk_text += 1
                            if evt.key == pyg.K_x:
                                game.stg_mgr.talk = False
                        else: # 主暂停界面操作
                            if not game.stg_mgr.ru_sure: # 暂停界面操作
                                if evt.key == pyg.K_ESCAPE:
                                    game.stg_mgr.pau_evt()
                                elif evt.key == pyg.K_q:
                                    game.stg_mgr.ru_sure_evt()
                            else: # 确定退出界面操作
                                if evt.key == pyg.K_y:
                                    run = True
                                elif evt.key == pyg.K_n:
                                    game.stg_mgr.ru_sure_evt()
                    else: # 结算界面操作
                        if evt.key == pyg.K_z:
                            game.stg_mgr.next_lv()

            game.game_gui.blit()

            clk.tick(60)

        pyg.event.clear()

    else: # 主菜单
        start = StartGUI(scr, fnt, clk)

        run = True
        while run:
            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    sys.exit()
                elif evt.type == pyg.KEYDOWN:
                    if evt.key == pyg.K_z:
                        run = False
                    elif evt.key == pyg.K_c:
                        pass
                    elif evt.key == pyg.K_q:
                        sys.exit()

            start.blit()

            clk.tick(60)

        pyg.event.clear()