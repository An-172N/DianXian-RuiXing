import pygame as pyg
import datetime as dt

from CORE.FILE.SLGEN import SLGen
from CORE.FILE.SAVE import Save

from LOGIC.SPRITE.MAIN.PLANE import PlaneMgr
from LOGIC.SPRITE.MAIN.BULLET import BulletMgr
from LOGIC.SPRITE.MAIN.ITEM import ItemMgr
from LOGIC.SPRITE.SUB.BARRAGE import BarrageMgr
from LOGIC.SPRITE.SUB.PARTICLE import ParticleMgr
from LOGIC.PROCESS.GAME.EVENT import EventMgr
from LOGIC.PROCESS.GAME.SCORE import ScoreMgr
from LOGIC.PROCESS.GAME.STAGE import StageMgr
from LOGIC.PROCESS.GAME.RESET import ResetMgr
from LOGIC.PROCESS.SPRITE.COLLIDE import CollideMgr
from LOGIC.PROCESS.SPRITE.LIFE import LifeMgr

from GUI.GAME.MAIN import MainGUI
from GUI.SUB.START import StartGUI
from GUI.SUB.SAVE import SaveGUI
from GUI.SUB.PAUSE import PauseGUI


class Thunder:
    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.fnt = fnt
        th.clk = clk

        th.win = pyg.Rect((120, 15,
                           345, 330))
        th.eff_range = pyg.Rect((105, 0,
                                 375, 360))

        th.run = False

        th.pln_grp = pyg.sprite.Group()
        th.blt_grp = pyg.sprite.Group()
        th.brc_grp = pyg.sprite.Group()
        th.item_grp = pyg.sprite.Group()
        th.brg_grp = pyg.sprite.Group()
        th.ptcl_grp = pyg.sprite.Group()

        th.start_gui = StartGUI(th)
        th.sav_gui = SaveGUI(th)
        th.pau_gui = PauseGUI(th)
        th.main_gui = MainGUI(th)

        th.sl_gen = SLGen(th)
        th.sav_mgr = Save(th)

        th.evt_mgr = EventMgr(th)
        th.sc_mgr = ScoreMgr(th)
        th.stg_mgr = StageMgr(th)
        th.pln_mgr = PlaneMgr(th)
        th.blt_mgr = BulletMgr(th)
        th.coll_mgr = CollideMgr(th)
        th.brg_mgr = BarrageMgr(th)
        th.item_mgr = ItemMgr(th)
        th.ptcl_mgr = ParticleMgr(th)
        th.rst_mgr = ResetMgr(th)
        th.life_mgr = LifeMgr(th)

    def draw_rect(th, wid, hei, bd, clr, pos):
        surface = pyg.Surface((wid, hei), pyg.SRCALPHA)

        pyg.draw.rect(surface,
                      clr,
                      surface.get_rect(),
                      bd)

        th.scr.blit(surface, pos)

    def txt_func(th, txt, pos):
        th.scr.blit(th.fnt.render(f"{txt}",
                                  False,
                                  (255, 255, 255)),
                    pos)
        
    def op_file(th, write, file, str=None):
        op_file = file

        if write:
            with open(op_file, 'w') as f: return f.write(str)
        else:
            with open(op_file, 'r') as f: return f.read()

    @staticmethod
    def datetime(sw):
        if sw: return dt.datetime.now().strftime('%Y-%m-%d')
        else: return dt.datetime.now().strftime("%H:%M:%S")