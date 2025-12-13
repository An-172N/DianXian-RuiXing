import os
import json
import datetime as dt

import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.SPRITE import ITEM


def save_file() -> None:
    date = dt.datetime.now().strftime('%Y-%m-%d')
    time = dt.datetime.now().strftime('%H-%M-%S')

    folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{VARIABLE.name}-{date}-{time}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    dump = ["RuiShan Fuxing Log"]
    stage = VARIABLE.stage if VARIABLE.stage <= 3 else f'Extra'
    dump.append(
        {
            'Nickname': VARIABLE.name,
            'Score': VARIABLE.score,
            'The farthest place that you reached': f"{stage} - {VARIABLE.level}",
            'Pick up SPower rate': ITEM.cal_s_power(),
            'Shape Flash': VARIABLE.s_flash,
            'Record date': dt.datetime.now().strftime('%Y-%m-%d')
        }
    )
        
    with open(file, 'w') as f:
        json.dump(dump, f, indent=4)