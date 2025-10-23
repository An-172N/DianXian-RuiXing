import json
import os

from ..LOGIC import TOOL


name = ''


def sav_file(sc, stg, lv):
    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{name}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(file):
        sav = json.loads(TOOL.op_file(False, file))
    else:
        sav = ['锐山抚形日志']

    sav.append(
        {
            '助记': name,
            '分数': sc,
            '最远到达的地方': f"{stg} - {lv}",
            '记录日期': TOOL.get_dt(True),
        }
    )

    str = json.dumps(sav, indent=4)
    TOOL.op_file(True,
                 file,
                 str)