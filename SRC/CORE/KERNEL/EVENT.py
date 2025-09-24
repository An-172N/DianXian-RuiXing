import pygame as pyg
import sys


class Event:
    def __init__(th, own):
        th.own = own

    def chk_evt(th):
        for evt in pyg.event.get():
            if evt.type == pyg.QUIT: # 保证可以退出
                sys.exit()
            elif evt.type == pyg.KEYUP: # 按完后操作
                th.chk_keyup_evt(evt)
            elif evt.type == pyg.KEYDOWN: # 按下操作
                th.chk_keydown_evt(evt)

    def chk_keydown_evt(th, evt):
        key_dict_game = {
            pyg.K_RIGHT: lambda: setattr(th.own.pln_mgr, "mv_right",
                                         True),
            pyg.K_LEFT: lambda: setattr(th.own.pln_mgr, "mv_left",
                                        True),
            pyg.K_LSHIFT: lambda: setattr(th.own.pln_mgr, "is_slow",
                                          True),
            pyg.K_z: lambda: setattr(th.own.blt_mgr, "is_cnt_fusil",
                                     True),
            pyg.K_x: lambda: th.own.blt_mgr.single_bomb(),
            pyg.K_ESCAPE: lambda: setattr(th.own.stg_mgr, "pau",
                                          True)
        }

        key_dict_talk = {
            pyg.K_z: lambda: setattr(th.own.stg_mgr, "txt_num",
                                     th.own.stg_mgr.txt_num + 1),
            pyg.K_x: lambda: setattr(th.own.stg_mgr, "talk",
                                     False)
        }

        key_dict_pau = {
            pyg.K_ESCAPE: lambda: setattr(th.own.stg_mgr, "pau",
                                          False),
            pyg.K_q: lambda: setattr(th.own.stg_mgr, "ru_sure",
                                     True)
        }

        key_dict_ru_sure = {
            pyg.K_y: lambda: (th.own.rst_mgr.rst_spr(),
                              th.own.rst_mgr.rst_pln(),
                              th.own.rst_mgr.rst_bomb(),
                              th.own.rst_mgr.rst_ctr(),
                              th.own.rst_mgr.rst_sc(),
                              th.own.rst_mgr.rst_pau(),
                              th.own.rst_mgr.rst_item(),
                              th.own.rst_mgr.rst_stg(),
                              th.own.rst_mgr.rst_game()),
            pyg.K_n: lambda: setattr(th.own.stg_mgr, "ru_sure",
                                 False)
        }

        key_dict_start = {
            pyg.K_z: lambda: setattr(th.own, "run",
                                     True),
            pyg.K_q: lambda: sys.exit()
        }

        key_dict_over = {
            pyg.K_RETURN: lambda: (th.own.sav_mgr.sav(),
                                   th.own.rst_mgr.rst_spr(),
                                   th.own.rst_mgr.rst_pln(),
                                   th.own.rst_mgr.rst_bomb(),
                                   th.own.rst_mgr.rst_ctr(),
                                   th.own.rst_mgr.rst_sc(),
                                   th.own.rst_mgr.rst_pau(),
                                   th.own.rst_mgr.rst_item(),
                                   th.own.rst_mgr.rst_stg(),
                                   th.own.rst_mgr.rst_game()),
            pyg.K_ESCAPE: lambda: (th.own.rst_mgr.rst_spr(),
                                   th.own.rst_mgr.rst_pln(),
                                   th.own.rst_mgr.rst_bomb(),
                                   th.own.rst_mgr.rst_ctr(),
                                   th.own.rst_mgr.rst_sc(),
                                   th.own.rst_mgr.rst_pau(),
                                   th.own.rst_mgr.rst_item(),
                                   th.own.rst_mgr.rst_stg(),
                                   th.own.rst_mgr.rst_game()),
            pyg.K_BACKSPACE: lambda: setattr(th.own.sav_mgr, "name",
                                             th.own.sav_mgr.name[:-1]),
        }

        if not th.own.run:
            if evt.key in key_dict_start:
                key_dict_start[evt.key]()
        else:
            if th.own.stg_mgr.sav:
                if evt.key in key_dict_over:
                    key_dict_over[evt.key]()
                else:
                    th.own.sav_mgr.name += evt.unicode
            elif not th.own.stg_mgr.summ: # 非结算界面操作
                if not th.own.stg_mgr.pau:
                    if not th.own.stg_mgr.talk: # 游戏主要操作
                        if evt.key in key_dict_game:
                            key_dict_game[evt.key]()
                    else:
                        if th.own.sl_gen.lv_ld:
                            if evt.key in key_dict_talk:
                                key_dict_talk[evt.key]()
                else: # 主暂停界面操作
                    if not th.own.stg_mgr.ru_sure: # 暂停界面操作
                        if evt.key in key_dict_pau:
                            key_dict_pau[evt.key]()
                    else: # 确定退出界面操作
                        if evt.key in key_dict_ru_sure:
                            key_dict_ru_sure[evt.key]()
            else: # 结算界面操作
                if evt.key == pyg.K_z:
                    th.own.stg_mgr.next_lv()

    def chk_keyup_evt(th, evt):
        key_dict = {
            pyg.K_RIGHT: lambda: setattr(th.own.pln_mgr, "mv_right",
                                         False),
            pyg.K_LEFT: lambda: setattr(th.own.pln_mgr, "mv_left",
                                        False),
            pyg.K_LSHIFT: lambda: setattr(th.own.pln_mgr, "is_slow",
                                          False),
            pyg.K_z: lambda: setattr(th.own.blt_mgr, "is_cnt_fusil",
                                     False)
        }

        if th.own.run:
            if evt.key in key_dict:
                key_dict[evt.key]()