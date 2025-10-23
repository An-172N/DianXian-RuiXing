import sys

import pygame as pyg

import DICT
from FUNC import Save


class Key:
    def __init__(th, own):
        th.own = own

    def chk_key(th):
        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                sys.exit()
            elif evt.type == pyg.KEYUP:
                if th.own.run:
                    if evt.key in DICT.key_dict["up"]["game"]:
                        DICT.key_dict["up"]["game"][evt.key](th)
            elif evt.type == pyg.KEYDOWN:
                if not th.own.run:
                    if evt.key in DICT.key_dict["down"]["start"]:
                        DICT.key_dict["down"]["start"][evt.key](th)
                else:
                    if th.own.sav:
                        if evt.key in DICT.key_dict["down"]["over"]:
                            DICT.key_dict["down"]["over"][evt.key](th)
                        else:
                            Save.name += evt.unicode
                    elif th.own.pau:
                        if evt.key in DICT.key_dict["down"]["pau"]:
                            DICT.key_dict["down"]["pau"][evt.key](th)
                    elif th.own.talk:
                        if evt.key in DICT.key_dict["down"]["talk"]:
                            DICT.key_dict["down"]["talk"][evt.key](th)
                    else:
                        if evt.key in DICT.key_dict["down"]["game"]:
                            DICT.key_dict["down"]["game"][evt.key](th)
    
    def rst_game(th):
        for cls in ("rst1", "rst2"):
            for bra in th.own.proc(cls):
                for evt in th.own.proc(cls, bra):
                    th.own.proc(cls, bra, evt)