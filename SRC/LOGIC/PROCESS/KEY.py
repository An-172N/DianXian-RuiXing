import sys
import os
import json
import re
import datetime as dt

import pygame as pyg

import DICT
import FUNC


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
        folder = f'{os.environ["USERPROFILE"]}/Saved Games/{game}'
        pattern = re.compile(rf'^{re.escape(th.name)}(\d+){re.escape(".json")}$')

        if not os.path.exists(folder):
            os.makedirs(folder)
        num =[]
        for i in os.listdir(folder):
            match = pattern.match(i)
            if match:
                num.append(int(match.group(1)))

        if num:
            next_num = max(num) + 1
        else:
            next_num = 1

        file = f'{os.environ["USERPROFILE"]}/Saved Games/{game}/{th.name}{next_num}.json'
        dump = [tit]
        dump.append({
                        'Nickname': th.name,
                        'Score': sc,
                        'The farthest place that you reached': f"{stg} - {lv}",
                        'Record date': dt.datetime.now().strftime('%Y-%m-%d'),
                    })

        str = json.dumps(dump, indent=4)
        FUNC.Process.process_file(file, 'r', lambda f: f.write(str))