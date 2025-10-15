import pygame as pyg

from FRIEND import Ono
from FUNC import Load
from FUNC import Spawn


class StageMgr:
    char_dict = {
        1: Ono
    }

    def __init__(th, proc):
        th.proc = proc

        th.txt_num = 0
        th.txt_pt = 0
        th.ctr = 0
        th.stg = 1
        th.lv = 5

        th.bg = th.chs_bg()
        th.bg.set_alpha(159)

        th.char = None
        th.txt = None

    def next_lv(th):
        for cls in ("rst1", "sw"):
            for bra in th.proc(cls):
                for evt in th.proc(cls, bra):
                    if evt != "run":
                        th.proc(cls, bra, evt,
                                False)

        th.proc("add", "pln", "sc",
                th.proc("get", "pln", "ttl_spt") * 512)
        th.proc("add", "pln", "sc",
                th.proc("get", "pln", "no_hurt") * 4096)

        th.proc("add", "pln", "no_hurt",
                1)
        th.proc("func", "pln", "spwn_pln")()

    def lv_proc(th):
        if not th.proc('get', 'main', 'lv_ld'):
            if th.ctr <= 60:
                th.ctr += 1
            else:
                if th.lv == 6:
                    th.char = th.chs_shhm()
                    th.txt = Load.ld_txt(th.stg)
                    th.txt_num = 0
                    th.proc('sw', 'main', 'talk',
                            True)

                    th.spwn_shhm()
                else:
                    Load.ld_stg(th.stg, th.lv,
                                th.proc("get", "main", "clr")[th.stg],
                                th.proc("get", "main", "clr")[6],
                                (127, 22), (15, 15), 4, 30 - th.stg,
                                th.proc("get", "main", "brc_grp"))

                th.ctr = 0
                th.proc('sw', 'main', 'lv_ld',
                        True)
        else:
            if (len(th.proc("get", "main", "brc_grp")) == 0 and
                not th.proc('get', 'main', 'talk')):
                if th.ctr <= 105:
                    th.ctr += 1
                    th.proc('sw', 'main', 'summ',
                            True)
                else:
                    th.next_lv()
                    th.lv_lgc()

                    th.proc('sw', 'main', 'summ',
                            False)
                    th.ctr = 0
    
    def lv_lgc(th):
        if th.lv >= 6:
            th.stg += 1
            th.lv = 1
            th.bg = th.chs_bg()
        else:
            th.lv += 1

    def chs_shhm(th):
        return th.char_dict.get(th.stg)(th.proc)
    
    def shhm_lose(th):
        th.txt_pt += 1
        th.txt_num = 0

        th.proc('sw', 'main', 'talk',
                True)
    
    def chs_bg(th):
        return pyg.image.load(f'AST/IMG_STAGE{th.stg}BG.png').convert_alpha()

    def spwn_shhm(th):
        Spawn.shhm_spwn(th.char, th.proc("get", "main", "brc_grp"),
                        (292, 60))