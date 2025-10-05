import pygame as pyg
import datetime as dt

import LOGIC
import GUI
import KEY
import FILE


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

    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.fnt = fnt
        th.clk = clk

        th.win = pyg.Rect((120, 15,
                           345, 330))
        th.eff_range = pyg.Rect((105, 0,
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

        th.game_gui = GUI.GUI(th)
        th.evt_mgr = KEY.Event(th)

        th.sl_gen = FILE.SLGen(th)
        th.sav_mgr = FILE.Save(th)
        
        th.sc_mgr = LOGIC.ScoreMgr(th)
        th.stg_mgr = LOGIC.StageMgr(th)
        th.pln_mgr = LOGIC.PlaneMgr(th)
        th.blt_mgr = LOGIC.BulletMgr(th)
        th.coll_mgr = LOGIC.CollideMgr(th)
        th.brg_mgr = LOGIC.BarrageMgr(th)
        th.item_mgr = LOGIC.ItemMgr(th)
        th.ptcl_mgr = LOGIC.ParticleMgr(th)
        th.rst_mgr = LOGIC.ResetMgr(th)
    
    @staticmethod
    def op_file(write, file, str=None):
        if write:
            with open(file, 'w') as f:
                return f.write(str)
        else:
            with open(file, 'r') as f:
                return f.read()

    @staticmethod
    def datetime(date):
        if date:
            return dt.datetime.now().strftime('%Y-%m-%d')
        else:
            return dt.datetime.now().strftime("%H:%M:%S")