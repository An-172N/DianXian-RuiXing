import pygame as pyg

import LOGIC


class Thunder:
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

        th.gui = LOGIC.GUI(th)
        th.key_mgr = LOGIC.Key(th)
        th.pln_mgr = LOGIC.PlaneMgr(th)
        th.stg_mgr = LOGIC.StageMgr(th)
        th.blt_mgr = LOGIC.BulletMgr(th)
        th.item_mgr = LOGIC.ItemMgr(th)