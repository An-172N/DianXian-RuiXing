import sys
import os
import json
import datetime as dt

import pygame as pyg

import DICT


class Key:
    def __init__(th, own):
        th.own = own

        th.name = ''

    def chk_key(th):
        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                sys.exit()
            elif evt.type == pyg.KEYUP:
                if th.own.run:
                    if evt.key in DICT.key_dict["up"]["game"]:
                        DICT.key_dict["up"]["game"][evt.key](th.own)
            elif evt.type == pyg.KEYDOWN:
                if not th.own.run:
                    if evt.key in DICT.key_dict["down"]["start"]:
                        DICT.key_dict["down"]["start"][evt.key](th.own)
                else:
                    if th.own.sav:
                        if evt.key in DICT.key_dict["down"]["over"]:
                            DICT.key_dict["down"]["over"][evt.key](th.own)
                        else:
                            th.name += evt.unicode
                    elif th.own.pau:
                        if evt.key in DICT.key_dict["down"]["pau"]:
                            DICT.key_dict["down"]["pau"][evt.key](th.own)
                    elif th.own.talk:
                        if evt.key in DICT.key_dict["down"]["talk"]:
                            DICT.key_dict["down"]["talk"][evt.key](th.own)
                    elif not th.own.summ and th.own.lv_ld:
                        if evt.key in DICT.key_dict["down"]["game"]:
                            DICT.key_dict["down"]["game"][evt.key](th.own)
    
    def rst_game(th):
        for cls in ("rst1", "rst2"):
            for bra in DICT.rst_dict[cls]:
                for evt in DICT.rst_dict[cls][bra]:
                    DICT.rst_dict[cls][bra][evt](th.own)

    def sav_file(th, sc, stg, lv, game, tit):
        date = dt.datetime.now().strftime('%Y-%m-%d')
        time = dt.datetime.now().strftime('%H-%M-%s')

        folder = f'{os.environ["USERPROFILE"]}/Saved Games/{game}'
        file = f'{os.environ["USERPROFILE"]}/Saved Games/{game}/{th.name}-{date}-{time}.json'

        if not os.path.exists(folder):
            os.makedirs(folder)

        dump = [tit]
        dump.append({
                        'Nickname': th.name,
                        'Score': sc,
                        'The farthest place that you reached': f"{stg} - {lv}",
                        'Pick up SPT rate': th.own.item_mgr.cal_spt(),
                        'Record date': dt.datetime.now().strftime('%Y-%m-%d'),
                    })
        
        with open(file, 'w') as f:
            json.dump(dump, f, indent=4)