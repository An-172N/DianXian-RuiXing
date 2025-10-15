import sys

import pygame as pyg

from FUNC import Save


class Key:
    key_dict = {
        "down": {
            "game": {
                pyg.K_RIGHT: lambda th: th.proc("sw", "pln", "mv_right",
                                                True),
                pyg.K_LEFT: lambda th: th.proc("sw", "pln", "mv_left",
                                               True),
                pyg.K_LSHIFT: lambda th: th.proc("sw", "pln", "is_slow",
                                                 True),
                pyg.K_z: lambda th: th.proc("func", "blt", "blt")(),
                pyg.K_x: lambda th: th.proc("func", "blt", "single_bomb")(),
                pyg.K_ESCAPE: lambda th: th.proc("sw", "main", "pau",
                                                 True)
            },
            "talk": {
                pyg.K_z: lambda th: th.proc("add", "stg", "txt_num",
                                            1),
                pyg.K_x: lambda th: th.proc("sw", "main", "talk",
                                            False)
            },
            "pau": {
                pyg.K_ESCAPE: lambda th: th.proc("sw", "main", "pau",
                                                 False),
                pyg.K_q: lambda th: th.rst_game()
            },
            "start": {
                pyg.K_z: lambda th: (th.proc("sw", "main", "run",
                                             True),
                                     th.proc("func", "stg", "next_lv")(),
                                     th.proc("func", "stg", "lv_lgc")()),
                pyg.K_q: lambda _: sys.exit()
            },
            "over": {
                pyg.K_RETURN: lambda th: (Save.sav_file(th.proc("get", "pln", "sc"),
                                                        th.proc("get", "stg", "stg"),
                                                        th.proc("get", "stg", "lv")),
                                          th.rst_game()),
                pyg.K_ESCAPE: lambda th: th.rst_game(),
                pyg.K_BACKSPACE: lambda th: setattr(Save, "name",
                                                    Save.name[:-1])
            }
        },
        "up": {
            "game": {
                pyg.K_RIGHT: lambda th: th.proc("sw", "pln", "mv_right",
                                                False),
                pyg.K_LEFT: lambda th: th.proc("sw", "pln", "mv_left",
                                               False),
                pyg.K_LSHIFT: lambda th: th.proc("sw", "pln", "is_slow",
                                                 False)
            }
        }
    }

    def __init__(th, proc):
        th.proc = proc

    def chk_key(th):
        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                sys.exit()
            elif evt.type == pyg.KEYUP:
                if th.proc('get', 'main', 'run'):
                    if evt.key in th.key_dict["up"]["game"]:
                        th.key_dict["up"]["game"][evt.key](th)
            elif evt.type == pyg.KEYDOWN:
                if not th.proc('get', 'main', 'run'):
                    if evt.key in th.key_dict["down"]["start"]:
                        th.key_dict["down"]["start"][evt.key](th)
                else:
                    if th.proc('get', 'main', 'sav'):
                        if evt.key in th.key_dict["down"]["over"]:
                            th.key_dict["down"]["over"][evt.key](th)
                        else:
                            Save.name += evt.unicode
                    elif th.proc('get', 'main', 'pau'):
                        if evt.key in th.key_dict["down"]["pau"]:
                            th.key_dict["down"]["pau"][evt.key](th)
                    elif th.proc('get', 'main', 'talk'):
                        if evt.key in th.key_dict["down"]["talk"]:
                            th.key_dict["down"]["talk"][evt.key](th)
                    else:
                        if evt.key in th.key_dict["down"]["game"]:
                            th.key_dict["down"]["game"][evt.key](th)
    
    def rst_game(th):
        for cls in ("rst1", "rst2", "sw"):
            for bra in th.proc(cls):
                for evt in th.proc(cls, bra):
                    th.proc(cls, bra, evt,
                            False)