# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import datetime
import json
import os
import re


def save_file(name, stage, level, score, power_rate, use_flash) -> None:
    def illegal_char(name: str) -> str:
        char = r'[!<>:"/\\|?*]'

        return re.sub(char, '_', name)

    def get_datetime() -> tuple:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime('%H-%M-%S')

        return date, time
    
    def create_file() -> str:
        now_datetime = get_datetime()

        folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
        file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{illegal_char(name)}_{now_datetime[0]}_{now_datetime[1]}.json'

        if not os.path.exists(folder):
            os.makedirs(folder)

        return file

    dump = ["RuiShan FuXing Log"]
    stage_text = stage if stage <= 3 else f'Extra'
    dump.append(
        {
            'Help recorder': name,
            'Score': score,
            'The farthest station that you reached': f"{stage_text} - {level}",
            'Pick up Shape Power rate': power_rate,
            'Shape Flash': use_flash,
            'Record date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
    )
        
    with open(create_file(), 'w') as f:
        json.dump(dump, f, indent=4)