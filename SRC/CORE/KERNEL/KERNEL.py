import pygame as pyg
# 导入核心
from CORE.SLGEN.SLGENERATOR import SLGenerator
# 导入逻辑模块
from LOGIC.SPRITE.PLANE import Plane
from LOGIC.SPRITE.BULLET import Bullet
from LOGIC.SPRITE.BARRAGE import Barrage
from LOGIC.SPRITE.ITEM import Item
from LOGIC.SPRITE.PARTICLE import Particle
from LOGIC.PROCESS.RESET import Reset
from LOGIC.PROCESS.SCORE import Score
from LOGIC.PROCESS.COLLIDE import Collide
from LOGIC.PROCESS.INVINCIBILITY import Invincibility
from LOGIC.PROCESS.REMOVE import Remove
from LOGIC.PROCESS.STAGE import Stage
# 导入GUI
from GUI.NONGAME.STARTGUI import StartGUI
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
        th.game_gui = GameGUI(th)
        th.pau_gui = PauseGUI(th)
        # 核心类
        th.sl_gen = SLGenerator(th)
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
        th.stg_mgr = Stage(th)
        th.rst_mgr = Reset(th)