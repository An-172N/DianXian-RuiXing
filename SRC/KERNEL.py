import pygame as pyg

import LOGIC


class Thunder:
    clr_dict = {
        1: (255, 128, 0),
        2: (255, 255, 0),
        3: (0, 255, 0),
        4: (128, 0, 128),
        5: (45, 194, 229),
        6: (255, 255, 255),
        7: (0, 0, 0)
    }

    evt_dict = {
        "add": {
            "pln": {
                "spt": lambda th, val: setattr(th.pln_mgr, "spt",
                                               th.pln_mgr.spt + val),
                "no_hurt": lambda th, val: setattr(th.pln_mgr, "no_hurt",
                                                   th.pln_mgr.no_hurt + val),
                "ttl_spt": lambda th, val: setattr(th.pln_mgr, "ttl_spt",
                                                   th.pln_mgr.ttl_spt + val),
                "plyr": lambda th, val: setattr(th.pln_mgr, "plyr",
                                                th.pln_mgr.plyr + val),
                "sc": lambda th, val: setattr(th.pln_mgr, "sc",
                                              th.pln_mgr.sc + val)
            },
            "stg": {
                "txt_num": lambda th, val: setattr(th.stg_mgr, "txt_num",
                                                   th.stg_mgr.txt_num + val),
                "txt_pt": lambda th, val: setattr(th.stg_mgr, "txt_pt",
                                                  th.stg_mgr.txt_pt + val),
                "stg": lambda th, val: setattr(th.stg_mgr, "stg",
                                               th.stg_mgr.stg + val),
                "lv": lambda th, val: setattr(th.stg_mgr, "lv",
                                              th.stg_mgr.lv + val)
            }
        },
        "sw": {
            "main": {
                "run": lambda th, val: setattr(th, "run",
                                               val),
                "pau": lambda th, val: setattr(th, "pau",
                                               val),
                "summ": lambda th, val: setattr(th, "summ",
                                                val),
                "talk": lambda th, val: setattr(th, "talk",
                                                val),
                "sav": lambda th, val: setattr(th, "sav",
                                               val),
                "lv_ld": lambda th, val: setattr(th, "lv_ld",
                                                 val)
            },
            "pln": {
                "is_sdivide": lambda th, val: setattr(th.pln_mgr, "is_sdivide",
                                                      val),
                "coll": lambda th, val: setattr(th.pln_mgr, "coll",
                                                val),
                "mv_right": lambda th, val: setattr(th.pln_mgr, "mv_right",
                                                    val),
                "mv_left": lambda th, val: setattr(th.pln_mgr, "mv_left",
                                                   val),
                "is_slow": lambda th, val: setattr(th.pln_mgr, "is_slow",
                                                   val),
            }
        },
        "func": {
            "stg": {
                "shhm_lose": lambda th, _: th.stg_mgr.shhm_lose,
                "next_lv": lambda th, _: th.stg_mgr.next_lv,
                "lv_lgc": lambda th, _: th.stg_mgr.lv_lgc
            },
            "pln": {
                "spwn_pln": lambda th, _: th.pln_mgr.spwn_pln,
                "turn_side": lambda th, _: th.pln_mgr.turn_side,
                "mv_pln": lambda th, _: th.pln_mgr.mv_pln,
                "invinc": lambda th, _: th.pln_mgr.invinc
            },
            "item": {
                "item_spwn": lambda th, _: th.item_mgr.item_spwn
            },
            "blt": {
                "single_bomb": lambda th, _: th.blt_mgr.single_bomb,
                "blt": lambda th, _: th.blt_mgr.spwn_blt
            },
            "wbrc": {
                "brc_death": lambda th, _: th.wb_proc.brc_death
            }
        },
        "get": {
            "pln": {
                "is_sdivide": lambda th, _: th.pln_mgr.is_sdivide,
                "is_visitable": lambda th, _: th.pln_mgr.is_visitable,
                "spt": lambda th, _: th.pln_mgr.spt,
                "sc": lambda th, _: th.pln_mgr.sc,
                "no_hurt": lambda th, _: th.pln_mgr.no_hurt,
                "ttl_spt": lambda th, _: th.pln_mgr.ttl_spt,
                "plyr": lambda th, _: th.pln_mgr.plyr,
                "char": lambda th, _: th.pln_mgr.char
            },
            "stg": {
                "stg": lambda th, _: th.stg_mgr.stg,
                "lv": lambda th, _: th.stg_mgr.lv,
                "txt": lambda th, _: th.stg_mgr.txt,
                "txt_pt": lambda th, _: th.stg_mgr.txt_pt,
                "txt_num": lambda th, _: th.stg_mgr.txt_num,
                "bg": lambda th, _: th.stg_mgr.bg,
                "char": lambda th, _: th.stg_mgr.char
            },
            "item": {
                "comb": lambda th, _: th.item_mgr.comb,
            },
            "main": {
                "scr": lambda th, _: th.scr,
                "fnt": lambda th, _: th.fnt,
                "clk": lambda th, _: th.clk,
                "win": lambda th, _: th.win,
                "eff": lambda th, _: th.eff,
                "clr": lambda th, _: th.clr_dict,
                "pln_grp": lambda th, _: th.pln_grp,
                "blt_grp": lambda th, _: th.blt_grp,
                "brc_grp": lambda th, _: th.brc_grp,
                "item_grp": lambda th, _: th.item_grp,
                "brg_grp": lambda th, _: th.brg_grp,
                "ptcl_grp": lambda th, _: th.ptcl_grp,
                "run": lambda th, _: th.run,
                "pau": lambda th, _: th.pau,
                "summ": lambda th, _: th.summ,
                "talk": lambda th, _: th.talk,
                "sav": lambda th, _: th.sav,
                "lv_ld": lambda th, _: th.lv_ld
            }
        },
        "rst1": {
            "main": {
                "item_grp": lambda th, _: th.item_grp.empty(),
                "brc_grp": lambda th, _: th.brc_grp.empty(),
                "pln_grp": lambda th, _: th.pln_grp.empty(),
                "blt_grp": lambda th, _: th.blt_grp.empty(),
                "ptcl_grp": lambda th, _: th.ptcl_grp.empty(),
                "brg_grp": lambda th, _: th.brg_grp.empty()
            },
            "pln": {
                "cd_ctr": lambda th, _: setattr(th.pln_mgr, "cd_ctr",
                                                0),
                "ttl_spt": lambda th, _: setattr(th.pln_mgr, "ttl_spt",
                                                 0)
            },
            "item": {
                "spwn_ctr": lambda th, _: setattr(th.item_mgr, "spwn_ctr",
                                                  0),
                "bw_ctr": lambda th, _: setattr(th.item_mgr, "bw_ctr",
                                                0)
            },
            "blt": {
                "bomb_cnt": lambda th, _: setattr(th.blt_mgr.bomb, "bomb_cnt",
                                                  0),
                "bomb_ctr": lambda th, _: setattr(th.blt_mgr.bomb, "ctr",
                                                  0)
            }
        },
        "rst2": {
            "stg": {
                "stg": lambda th, _: setattr(th.stg_mgr, "stg",
                                             1),
                "lv": lambda th, _: setattr(th.stg_mgr, "lv",
                                            0),
                "char": lambda th, _: setattr(th.stg_mgr, "char",
                                              None)
            },
            "pln": {
                "spt": lambda th, _: setattr(th.pln_mgr, "spt",
                                             0),
                "no_hurt": lambda th, _: setattr(th.pln_mgr, "no_hurt",
                                                 0),
                "plyr": lambda th, _: setattr(th.pln_mgr, "plyr",
                                              4),
                "sc": lambda th, _: setattr(th.pln_mgr, "sc",
                                            0)
            },
            "main": {
                "run": lambda th, _: setattr(th, "run",
                                             False)
            }
        }
    }

    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.fnt = fnt
        th.clk = clk

        th.win = pyg.Rect((120, 15,
                           345, 330))
        th.eff = pyg.Rect((105, 0,
                           375, 360))

        th.run = False
        th.pau = False
        th.summ = False
        th.talk = False
        th.sav = False
        th.lv_ld = False

        th.pln_grp = pyg.sprite.Group()
        th.blt_grp = pyg.sprite.Group()
        th.brc_grp = pyg.sprite.Group()
        th.item_grp = pyg.sprite.Group()
        th.brg_grp = pyg.sprite.Group()
        th.ptcl_grp = pyg.sprite.Group()

        th.game_gui = LOGIC.GUI(th.proc)
        th.evt_mgr = LOGIC.Key(th.proc)
        th.stg_mgr = LOGIC.StageMgr(th.proc)
        th.pln_mgr = LOGIC.PlaneMgr(th.proc)
        th.blt_mgr = LOGIC.BulletMgr(th.proc)
        th.item_mgr = LOGIC.ItemMgr(th.proc)
        th.wb_proc = LOGIC.WhiteBrick(th.proc)

    def proc(th, cls, bra=None, evt=None, val=0):
        if (bra == None and
            evt == None):
            return th.evt_dict[cls]
        elif evt is None:
            return th.evt_dict[cls][bra]
        else:
            return th.evt_dict[cls][bra][evt](th, val)