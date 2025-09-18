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
    if (game.run
        and not game.sav_mgr.is_sav):
        if not game.stg_mgr.pau: # 暂停、结算时不能更新
            game.item_mgr.comb_ctr()
                
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
                
    for evt in pyg.event.get():
        if evt.type == pyg.QUIT: # 保证可以退出
            sys.exit()
        elif evt.type == pyg.KEYUP: # 按完后操作
            key_dict = {
                pyg.K_RIGHT: lambda: setattr(game.pln_mgr, "mv_right",
                                             False),
                pyg.K_LEFT: lambda: setattr(game.pln_mgr, "mv_left",
                                            False),
                pyg.K_LSHIFT: lambda: game.pln_mgr.set_pln_spd(0),
                pyg.K_z: lambda: setattr(game.blt_mgr, "is_cnt_fusil",
                                         False)
            }

            if evt.key in key_dict:
                key_dict[evt.key]()
        elif evt.type == pyg.KEYDOWN: # 按下操作
            key_dict_game = {
                pyg.K_RIGHT: lambda: setattr(game.pln_mgr, "mv_right",
                                             True),
                pyg.K_LEFT: lambda: setattr(game.pln_mgr, "mv_left",
                                            True),
                pyg.K_LSHIFT: lambda: game.pln_mgr.set_pln_spd(1),
                pyg.K_z: lambda: setattr(game.blt_mgr, "is_cnt_fusil",
                                         True),
                pyg.K_x: lambda: game.blt_mgr.single_bomb(),
                pyg.K_ESCAPE: lambda: setattr(game.stg_mgr, "pau",
                                              True)
            }

            key_dict_talk = {
                pyg.K_z: lambda: setattr(game.stg_mgr, "talk_txt",
                                         game.stg_mgr.talk_txt + 1),
                pyg.K_x: lambda: setattr(game.stg_mgr, "talk",
                                         False)
            }

            key_dict_pau = {
                pyg.K_ESCAPE: lambda: setattr(game.stg_mgr, "pau",
                                              False),
                pyg.K_q: lambda: setattr(game.stg_mgr, "ru_sure",
                                         True)
            }

            key_dict_ru_sure = {
                pyg.K_y: lambda: game.rst_mgr.rst_game(),
                pyg.K_n: lambda: setattr(game.stg_mgr, "ru_sure",
                                         False)
            }

            key_dict_start = {
                pyg.K_z: lambda: setattr(game, "run",
                                         True),
                pyg.K_q: lambda: sys.exit()
            }

            key_dict_over = {
                pyg.K_RETURN: lambda: game.sav_mgr.exit(),
                pyg.K_BACKSPACE: lambda: setattr(game.sav_mgr, "name",
                                                 game.sav_mgr.name[:-1]),
                pyg.K_ESCAPE: lambda: game.rst_mgr.rst_game()
            }

            if not game.run:
                if evt.key in key_dict_start:
                    key_dict_start[evt.key]()
            else:
                if game.sav_mgr.is_sav:
                    if evt.key in key_dict_over:
                        key_dict_over[evt.key]()
                    else:
                        game.sav_mgr.name += evt.unicode
                elif not game.stg_mgr.summ: # 非结算界面操作
                    if not game.stg_mgr.pau:
                        if not game.stg_mgr.talk: # 游戏主要操作
                            if evt.key in key_dict_game:
                                key_dict_game[evt.key]()
                        else:
                            if game.sl_gen.lv_ld:
                                if evt.key in key_dict_talk:
                                    key_dict_talk[evt.key]()
                    else: # 主暂停界面操作
                        if not game.stg_mgr.ru_sure: # 暂停界面操作
                            if evt.key in key_dict_pau:
                                key_dict_pau[evt.key]()
                        else: # 确定退出界面操作
                            if evt.key in key_dict_ru_sure:
                                key_dict_ru_sure[evt.key]()
                else: # 结算界面操作
                    if evt.key == pyg.K_z:
                        game.stg_mgr.next_lv()

    game.game_gui.blit()

    game.game_gui.show_fps()

    clk.tick(60)