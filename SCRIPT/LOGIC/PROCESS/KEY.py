import os
import json
import datetime as dt

import SCRIPT.VARIABLE
from ..SPRITE import ITEM


def sav_file():
    date = dt.datetime.now().strftime('%Y-%m-%d')
    time = dt.datetime.now().strftime('%H-%M-%S')

    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{SCRIPT.VARIABLE.name}-{date}-{time}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    dump = ["RuiShan Fuxing Log"]
    dump.append({
                    'Nickname': SCRIPT.VARIABLE.name,
                    'Score': SCRIPT.VARIABLE.sc,
                    'The farthest place that you reached': f"{SCRIPT.VARIABLE.stage} - {SCRIPT.VARIABLE.level}",
                    'Pick up SPT rate': ITEM.cal_spt(),
                    'Shape Flash': SCRIPT.VARIABLE.sflash,
                    'Record date': dt.datetime.now().strftime('%Y-%m-%d')
                })
        
    with open(file, 'w') as f:
        json.dump(dump, f, indent=4)