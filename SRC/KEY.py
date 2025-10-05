import pygame as pyg
import sys


class Event:
    def __init__(th, own):
        th.own = own

    def chk_evt(th):
        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                sys.exit()
            elif evt.type == pyg.KEYUP:
                if th.own.run:
                    th.keyup_game(evt)
            elif evt.type == pyg.KEYDOWN:
                if not th.own.run:
                    th.keydown_start(evt)
                else:
                    if th.own.sav:
                        th.keydown_over(evt)
                    elif th.own.pau:
                        th.keydown_pau(evt)
                    elif th.own.talk:
                        th.keydown_talk(evt)
                    else:
                        th.keydown_game(evt)

    def keydown_game(th, evt):
        key_game = {
            pyg.K_RIGHT: lambda: setattr(th.own.pln_mgr, "mv_right",
                                         True),
            pyg.K_LEFT: lambda: setattr(th.own.pln_mgr, "mv_left",
                                        True),
            pyg.K_LSHIFT: lambda: setattr(th.own.pln_mgr, "is_slow",
                                          True),
            pyg.K_z: lambda: setattr(th.own.blt_mgr, "is_cnt_fusil",
                                     True),
            pyg.K_x: lambda: th.own.blt_mgr.single_bomb(),
            pyg.K_ESCAPE: lambda: setattr(th.own, "pau",
                                          True)
        }

        if evt.key in key_game:
            key_game[evt.key]()

    def keydown_talk(th, evt):
        key_talk = {
            pyg.K_z: lambda: setattr(th.own.stg_mgr, "txt_num",
                                     th.own.stg_mgr.txt_num + 1),
            pyg.K_x: lambda: setattr(th.own, "talk",
                                     False)
        }

        if evt.key in key_talk:
            key_talk[evt.key]()

    def keydown_pau(th, evt):
        key_pau = {
            pyg.K_ESCAPE: lambda: setattr(th.own, "pau",
                                          False),
            pyg.K_q: lambda: th.own.rst_mgr.rst_game()
        }

        if evt.key in key_pau:
            key_pau[evt.key]()

    def keydown_start(th, evt):
        key_start = {
            pyg.K_z: lambda: (setattr(th.own, "run",
                                      True),
                              th.own.stg_mgr.next_lv(),
                              th.own.stg_mgr.lv_lgc()),
            pyg.K_q: lambda: sys.exit()
        }

        if evt.key in key_start:
            key_start[evt.key]()

    def keydown_over(th, evt):
        key_over = {
            pyg.K_RETURN: lambda: (th.own.sav_mgr.sav(),
                                   th.own.rst_mgr.rst_game()),
            pyg.K_ESCAPE: lambda: th.own.rst_mgr.rst_game(),
            pyg.K_BACKSPACE: lambda: setattr(th.own.sav_mgr, "name",
                                             th.own.sav_mgr.name[:-1]),
        }

        if evt.key in key_over:
            key_over[evt.key]()
        else:
            th.own.sav_mgr.name += evt.unicode

    def keyup_game(th, evt):
        key = {
            pyg.K_RIGHT: lambda: setattr(th.own.pln_mgr, "mv_right",
                                         False),
            pyg.K_LEFT: lambda: setattr(th.own.pln_mgr, "mv_left",
                                        False),
            pyg.K_LSHIFT: lambda: setattr(th.own.pln_mgr, "is_slow",
                                          False),
            pyg.K_z: lambda: setattr(th.own.blt_mgr, "is_cnt_fusil",
                                     False)
        }

        if evt.key in key:
            key[evt.key]()