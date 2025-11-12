import sys

import pygame as pyg

from FRIEND import Ono
from FRIEND import Kli
from FRIEND import Hro


clr_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    5: (45, 194, 229),
    6: (255, 255, 255),
    7: (0, 0, 0)
}

char_dict = {
        1: Ono,
        2: Hro,
        4: Kli
}

rst_dict = {
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
            "coll": lambda th: setattr(th.pln_mgr, "coll",
                                       False),
            "is_sdivide": lambda th: setattr(th.pln_mgr, "is_sdivide",
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
        },
        "stg":{
            "txt_pt": lambda th: setattr(th.stg_mgr, "txt_pt",
                                         0),
            "txt_num": lambda th: setattr(th.pln_mgr, "txt_num",
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
                                          3),
            "sc": lambda th: setattr(th.pln_mgr, "sc",
                                        0)
        },
        "blt": {
            "spt": lambda th: setattr(th.blt_mgr, "spt",
                                      0),
            "can_shoot": lambda th: setattr(th.blt_mgr, "can_shoot",
                                            False)
        },
        "item": {
            "spwn_ctr": lambda th: setattr(th.item_mgr, "comb",
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
            pyg.K_RIGHT: lambda th: setattr(th.pln_mgr, "mv_right",
                                            True),
            pyg.K_LEFT: lambda th: setattr(th.pln_mgr, "mv_left",
                                           True),
            pyg.K_LSHIFT: lambda th: setattr(th.pln_mgr, "is_slow",
                                             True),
            pyg.K_z: lambda th: th.blt_mgr.spwn_blt(),
            pyg.K_x: lambda th: th.blt_mgr.single_bomb(),
            pyg.K_ESCAPE: lambda th: setattr(th, "pau",
                                             True)
        },
        "talk": {
            pyg.K_z: lambda th: setattr(th.stg_mgr, "txt_num",
                                        th.stg_mgr.txt_num + 1),
            pyg.K_x: lambda th: setattr(th, "talk",
                                        False)
        },
        "pau": {
            pyg.K_ESCAPE: lambda th: setattr(th, "pau",
                                             False),
            pyg.K_q: lambda th: th.key_mgr.rst_game()
        },
        "start": {
            pyg.K_z: lambda th: (setattr(th, "run",
                                         True),
                                 th.stg_mgr.next_lv(),
                                 th.stg_mgr.lv_lgc()),
            pyg.K_q: lambda _: sys.exit()
        },
        "over": {
            pyg.K_RETURN: lambda th: (th.key_mgr.sav_file(th.pln_mgr.sc,
                                                          th.stg_mgr.stg,
                                                          th.stg_mgr.lv,
                                                          "DX00",
                                                          "RuiShan Fuxing Log"),
                                      th.key_mgr.rst_game()),
            pyg.K_ESCAPE: lambda th: th.key_mgr.rst_game(),
            pyg.K_BACKSPACE: lambda th: setattr(th.key_mgr, "name",
                                               th.key_mgr.name[:-1])
        }
    },
    "up": {
        "game": {
            pyg.K_RIGHT: lambda th: setattr(th.pln_mgr, "mv_right",
                                            False),
            pyg.K_LEFT: lambda th: setattr(th.pln_mgr, "mv_left",
                                           False),
            pyg.K_LSHIFT: lambda th: setattr(th.pln_mgr, "is_slow",
                                             False),
            pyg.K_z: lambda th: (th.blt_mgr.spwn_blt(),
                                 setattr(th.blt_mgr, "can_shoot",
                                         True))
        }
    }
}