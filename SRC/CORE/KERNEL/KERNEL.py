import pygame as pyg
import datetime as dt
# 导入核心
from CORE.KERNEL.EVENT import Event
from CORE.LOAD.SLGEN import SLGenerator
from CORE.LOAD.SAVE import Save
# 导入逻辑模块
from LOGIC.SPRITE.MINE.PLANE import Plane
from LOGIC.SPRITE.MINE.BULLET import Bullet
from LOGIC.SPRITE.MINE.ITEM import Item
from LOGIC.SPRITE.OTHER.BARRAGE import Barrage
from LOGIC.SPRITE.OTHER.PARTICLE import Particle
from LOGIC.PROCESS.GAME.SCORE import Score
from LOGIC.PROCESS.GAME.STAGE import Stage
from LOGIC.PROCESS.GAME.RESET import Reset
from LOGIC.PROCESS.SPRITE.COLLIDE import Collide
from LOGIC.PROCESS.SPRITE.INVINCIBILITY import Invincibility
from LOGIC.PROCESS.SPRITE.REMOVE import Remove
from LOGIC.PROCESS.SPRITE.LIFE import Life
# 导入GUI
from GUI.NONGAME.STARTGUI import StartGUI
from GUI.NONGAME.SAVEGUI import SaveGUI
from GUI.GAME.GAMEGUI import GameGUI
from GUI.GAME.PAUSEGUI import PauseGUI


class Thunder:
    def __init__(th, scr, fnt, clk):
        th.scr = scr
        th.fnt = fnt
        th.clk = clk
        # 游玩窗口
        th.win = pyg.Rect((120, 15,
                           345, 330))
        th.eff_range = pyg.Rect((105, 0,
                                 375, 360))
        # 游戏运行状态
        th.run = False
        # 精灵组
        th.pln_grp = pyg.sprite.Group()
        th.blt_grp = pyg.sprite.Group()
        th.brc_grp = pyg.sprite.Group()
        th.item_grp = pyg.sprite.Group()
        th.brg_grp = pyg.sprite.Group()
        th.ptcl_grp = pyg.sprite.Group()
        # GUI类
        th.start_gui = StartGUI(th)
        th.sav_gui = SaveGUI(th)
        th.game_gui = GameGUI(th)
        th.pau_gui = PauseGUI(th)
        # 核心类
        th.evt_mgr = Event(th)
        th.sl_gen = SLGenerator(th)
        th.sav_mgr = Save(th)
        # 逻辑类
        th.sc_mgr = Score(th)
        th.pln_mgr = Plane(th)
        th.blt_mgr = Bullet(th)
        th.coll_mgr = Collide(th)
        th.brg_mgr = Barrage(th)
        th.item_mgr = Item(th)
        th.ptcl_mgr = Particle(th)
        th.invinc = Invincibility(th)
        th.rm_mgr = Remove(th)
        th.rst_mgr = Reset(th)
        th.life_mgr = Life(th)
        th.stg_mgr = Stage(th)

    def draw_rect(th, wid, hei, bd, clr):
        surface = pyg.Surface((wid, hei), pyg.SRCALPHA)

        pyg.draw.rect(surface, clr, surface.get_rect(), bd)

        return surface

    def txt_func(th, txt):
        return th.fnt.render(f"{txt}",
                             False,
                             (255, 255, 255))
    
    @staticmethod
    def date():
        return dt.datetime.now().strftime('%Y-%m-%d')
    
    @staticmethod
    def time():
        return dt.datetime.now().strftime("%H:%M:%S")