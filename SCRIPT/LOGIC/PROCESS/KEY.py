import os
import json
import datetime as dt

import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.SPRITE import ITEM


def sav_file() -> None:
    date = dt.datetime.now().strftime('%Y-%m-%d')
    time = dt.datetime.now().strftime('%H-%M-%S')

    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{VARIABLE.name}-{date}-{time}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    dump = ["RuiShan Fuxing Log"]
    dump.append({
                    'Nickname': VARIABLE.name,
                    'Score': VARIABLE.sc,
                    'The farthest place that you reached': f"{VARIABLE.stage} - {VARIABLE.level}",
                    'Pick up SPower rate': ITEM.cal_s_power(),
                    'Shape Flash': VARIABLE.sflash,
                    'Record date': dt.datetime.now().strftime('%Y-%m-%d')
                })
        
    with open(file, 'w') as f:
        json.dump(dump, f, indent=4)