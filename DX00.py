import pygame as pyg
import sys
import os
# 导入目录
sys.dont_write_bytecode = True
curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curr_dir, 'SRCS'))
# 导入核心
from CORE.SLGENERATOR import SLGenerator
# 导入逻辑模块
from LOGIC.GETSCORE import GetScore
from LOGIC.PLANEMANAGER import PlaneManager
from LOGIC.BULLETMANAGER import BulletManager
from LOGIC.COLLIDEMANAGER import CollideManager
from LOGIC.BARRAGEMANAGER import BarrageManager
from LOGIC.ITEMMANAGER import ItemManager
from LOGIC.BOMBMANAGER import BombManager
from LOGIC.PARTICLEMANAGER import ParticleManager
from LOGIC.INVINCIBILITY import Invincibility
from LOGIC.WHITEBRICKPROCESS import WhiteBrickProcess
from LOGIC.SPRITEREMOVER import SpriteRemove 
from LOGIC.STAGEMANAGER import StageManager
# 导入GUI
from GUI.STARTGUI import StartGUI
from GUI.GAMEGUI import GameGUI
from GUI.PAUSEGUI import PauseGUI


class Thunder:
    def __init__(th, scr, game_win, fnt, clk, game_bg, eff_range):
        th.scr = scr
        th.win = game_win
        th.fnt = fnt
        th.clk = clk
        th.bg = game_bg
        th.eff_range = eff_range
        # 数值
        th.players = 4
        th.s_pt = 64
        th.ttl_s_pt = 0
        th.stg = 1
        th.lv = 5
        th.sc_cnt = 0
        th.no_hurt_cnt = 0
        th.cooldown_ctr = 0
        # 运行状态
        th.run = False
        # 精灵组
        th.pln_grp = pyg.sprite.Group()
        th.blt_grp = pyg.sprite.Group()
        th.brc_grp = pyg.sprite.Group()
        th.item_grp = pyg.sprite.Group()
        th.brg_grp = pyg.sprite.Group()
        th.ptcl_grp = pyg.sprite.Group()
        # 核心类
        th.sl_gen = SLGenerator(th)
        # 逻辑类
        th.get_sc = GetScore(th)
        th.pln_mgr = PlaneManager(th)
        th.blt_mgr = BulletManager(th)
        th.coll_mgr = CollideManager(th)
        th.brg_mgr = BarrageManager(th)
        th.item_mgr = ItemManager(th)
        th.bomb_mgr = BombManager(th)
        th.ptcl_mgr = ParticleManager(th)
        th.invinc = Invincibility(th)
        th.w_brc_proc = WhiteBrickProcess(th)
        th.rm_mgr = SpriteRemove(th)
        th.stg_mgr = StageManager(th)
        # GUI类
        th.game_gui = GameGUI(th)
        th.pau_gui = PauseGUI(th)


pyg.init()
pyg.display.set_caption('DX_RSX')
# 游戏显示
flg = pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN|pyg.SCALED
scr = pyg.display.set_mode((480, 360),
                           flg,
                           vsync=1)
# 游戏字体和时钟
fnt = pyg.font.Font('ASTS\FONT_GNUUNIFONT.otf', 15)
clk = pyg.time.Clock()
# 游戏主背景和游玩窗口
game_bg = pyg.image.load('ASTS\IMG_GAMEBG.png').convert_alpha()
game_win = pyg.Rect((120, 15, 345, 330))
eff_range = pyg.Rect((105, 0, 375, 360))

run = True

while True:
    if not run: # 游戏
        game = Thunder(scr, game_win, fnt, clk,
                       game_bg, eff_range)

        game.game_gui.mask() # 游戏窗口遮罩，只调用一次

        while not run: # 其余为循环
            if not game.stg_mgr.pau: # 暂停、结算时不能更新
                game.item_mgr.combo_ctr()
                
                if (not game.stg_mgr.summ
                    and game.sl_gen.lv_ld
                    and not game.stg_mgr.talk):
                    game.pln_mgr.upd_pos()
                    game.pln_mgr.upd_size()
                    game.pln_mgr.respwn()

                    game.invinc.lgc()

                    game.item_mgr.spwn_regular()
                    game.item_mgr.item_upd()

                    game.blt_mgr.spwn_blts()
                    game.blt_mgr.upd_blts()

                    game.ptcl_mgr.upd()

                    game.bomb_mgr.use_bomb()

                    game.brg_mgr.upd()

                    game.rm_mgr.rm_sprs(game.blt_grp)
                    game.rm_mgr.rm_sprs(game.brg_grp)
                    game.rm_mgr.rm_sprs(game.item_grp)
                    game.rm_mgr.rm_sprs(game.ptcl_grp)

                    game.coll_mgr.chk_brg_coll()
                    game.coll_mgr.chk_blt_coll()
                    game.coll_mgr.chk_item_coll()

            game.sl_gen.lgc()

            game.game_gui.show_fps()
                
            for evt in pyg.event.get():
                if evt.type == pyg.QUIT: # 保证可以退出
                    sys.exit()
                elif evt.type == pyg.KEYUP: # 按完后操作
                    if evt.key == pyg.K_RIGHT:
                        game.pln_mgr.mv_right = False
                    if evt.key == pyg.K_LEFT:
                        game.pln_mgr.mv_left = False
                    if evt.key == pyg.K_LSHIFT:
                        game.pln_mgr.set_pln_spd(0)
                elif evt.type == pyg.KEYDOWN: # 按下操作
                    if not game.stg_mgr.summ: # 非结算界面操作
                        if not game.stg_mgr.pau and not game.stg_mgr.talk: # 游戏主要操作
                            if evt.key == pyg.K_RIGHT:
                                game.pln_mgr.mv_right = True
                            if evt.key == pyg.K_LEFT:
                                game.pln_mgr.mv_left = True
                            if evt.key == pyg.K_LSHIFT:
                                game.pln_mgr.set_pln_spd(1)
                            if evt.key == pyg.K_x:
                                game.bomb_mgr.single_bomb()
                            if evt.key == pyg.K_ESCAPE:
                                game.stg_mgr.pau_evt()
                        elif game.stg_mgr.talk and not game.stg_mgr.pau:
                            if evt.key == pyg.K_z:
                                game.stg_mgr.text += 1
                            if evt.key == pyg.K_x:
                                game.stg_mgr.talk = False
                        else: # 主暂停界面操作
                            if not game.stg_mgr.ru_sure: # 暂停界面操作
                                if evt.key == pyg.K_ESCAPE:
                                    game.stg_mgr.pau_evt()
                                elif evt.key == pyg.K_q:
                                    game.stg_mgr.ru_sure_evt()
                            else: # 确定退出界面操作
                                if evt.key == pyg.K_y:
                                    run = True
                                elif evt.key == pyg.K_n:
                                    game.stg_mgr.ru_sure_evt()
                    else: # 结算界面操作
                        if evt.key == pyg.K_z:
                            game.stg_mgr.next_lv()

            game.game_gui.blit()

            clk.tick(60)

        pyg.event.clear()

    else: # 主菜单
        start = StartGUI(scr, fnt, clk)

        run = True
        while run:
            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    sys.exit()
                elif evt.type == pyg.KEYDOWN:
                    if evt.key == pyg.K_z:
                        run = False
                    elif evt.key == pyg.K_c:
                        pass
                    elif evt.key == pyg.K_q:
                        sys.exit()

            start.blit()

            clk.tick(60)

        pyg.event.clear()