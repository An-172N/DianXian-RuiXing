import sys

import pygame as pyg

from FRIEND import Ono
from FRIEND import Kli
from FUNC import Save


clr_dict = {
    1: (255, 128, 0),
    2: (255, 255, 0),
    3: (0, 255, 0),
    4: (128, 0, 128),
    5: (45, 194, 229),
    6: (255, 255, 255),
    7: (0, 0, 0)
}

char_dict = {
        1: Ono,
        5: Kli
}

evt_dict = {
    "rst1": {
        "main": {
            "pau": lambda th: setattr(th, "pau",
                                      False),
            "summ": lambda th: setattr(th, "summ",
                                       False),
            "talk": lambda th: setattr(th, "talk",
                                       False),
            "sav": lambda th: setattr(th, "sav",
                                      False),
            "lv_ld": lambda th: setattr(th, "lv_ld",
                                        False),
            "item_grp": lambda th: th.item_grp.empty(),
            "brc_grp": lambda th: th.brc_grp.empty(),
            "pln_grp": lambda th: th.pln_grp.empty(),
            "blt_grp": lambda th: th.blt_grp.empty(),
            "ptcl_grp": lambda th: th.ptcl_grp.empty(),
            "brg_grp": lambda th: th.brg_grp.empty()
        },
        "pln": {
            "is_sdivide": lambda th: setattr(th.pln_mgr, "is_sdivide",
                                             False),
            "coll": lambda th: setattr(th.pln_mgr, "coll",
                                       False),
            "mv_right": lambda th: setattr(th.pln_mgr, "mv_right",
                                           False),
            "mv_left": lambda th: setattr(th.pln_mgr, "mv_left",
                                          False),
            "is_slow": lambda th: setattr(th.pln_mgr, "is_slow",
                                          False),
            "cd_ctr": lambda th: setattr(th.pln_mgr, "cd_ctr",
                                         0),
            "bomb_cnt": lambda th: setattr(th.pln_mgr.char.bomb, "bomb_cnt",
                                           0),
            "bomb_ctr": lambda th: setattr(th.pln_mgr.char.bomb, "ctr",
                                           0)
        },
        "blt": {
            "ttl_spt": lambda th: setattr(th.blt_mgr, "ttl_spt",
                                          0)
        },
        "item": {
            "spwn_ctr": lambda th: setattr(th.item_mgr, "spwn_ctr",
                                           0),
            "bw_ctr": lambda th: setattr(th.item_mgr, "bw_ctr",
                                         0)
        }
    },
    "rst2": {
        "stg": {
            "stg": lambda th: setattr(th.stg_mgr, "stg",
                                      1),
            "lv": lambda th: setattr(th.stg_mgr, "lv",
                                     0),
            "char": lambda th: setattr(th.stg_mgr, "char",
                                       None)
        },
        "pln": {
            "no_hurt": lambda th: setattr(th.pln_mgr, "no_hurt",
                                          0),
            "plyr": lambda th: setattr(th.pln_mgr, "plyr",
                                       4),
            "sc": lambda th: setattr(th.pln_mgr, "sc",
                                     0)
        },
        "blt": {
            "spt": lambda th: setattr(th.blt_mgr, "spt",
                                      0)
        },
        "main": {
            "run": lambda th: setattr(th, "run",
                                      False)
        }
    }
}

key_dict = {
    "down": {
        "game": {
            pyg.K_RIGHT: lambda th: setattr(th.own.pln_mgr, "mv_right",
                                            True),
            pyg.K_LEFT: lambda th: setattr(th.own.pln_mgr, "mv_left",
                                           True),
            pyg.K_LSHIFT: lambda th: setattr(th.own.pln_mgr, "is_slow",
                                             True),
            pyg.K_z: lambda th: th.own.blt_mgr.spwn_blt(),
            pyg.K_x: lambda th: th.own.blt_mgr.single_bomb(),
            pyg.K_ESCAPE: lambda th: setattr(th.own, "pau",
                                             True)
        },
        "talk": {
            pyg.K_z: lambda th: setattr(th.own.stg_mgr, "txt_num",
                                        th.own.stg_mgr.txt_num + 1),
            pyg.K_x: lambda th: setattr(th.own, "talk",
                                        False)
        },
        "pau": {
            pyg.K_ESCAPE: lambda th: setattr(th.own, "pau",
                                             False),
            pyg.K_q: lambda th: th.rst_game()
        },
        "start": {
            pyg.K_z: lambda th: (setattr(th.own, "run",
                                         True),
                                 th.own.stg_mgr.next_lv(),
                                 th.own.stg_mgr.lv_lgc()),
            pyg.K_q: lambda _: sys.exit()
        },
        "over": {
            pyg.K_RETURN: lambda th: (Save.sav_file(th.own.pln_mgr.sc,
                                                    th.own.stg_mgr.stg,
                                                    th.own.stg_mgr.lv),
                                      th.rst_game()),
            pyg.K_ESCAPE: lambda th: th.rst_game(),
            pyg.K_BACKSPACE: lambda _: setattr(Save, "name",
                                               Save.name[:-1])
        }
    },
    "up": {
        "game": {
            pyg.K_RIGHT: lambda th: setattr(th.own.pln_mgr, "mv_right",
                                            False),
            pyg.K_LEFT: lambda th: setattr(th.own.pln_mgr, "mv_left",
                                           False),
            pyg.K_LSHIFT: lambda th: setattr(th.own.pln_mgr, "is_slow",
                                             False)
        }
    }
}