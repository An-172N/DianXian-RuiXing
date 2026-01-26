# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import datetime
import json
import os


def dump_file(file: str, name: str, stage_level: tuple, score: int, power_rate: str, use_flash: int) -> None:
    dump = ["锐山抚形日志"]
    dump.append(
        {
            '助记者': name,
            '分数': score,
            '最远到达的地方': f"{stage_level[0]} - {stage_level[1]}",
            '拾形点率': power_rate,
            '形闪次数': use_flash,
            '记录日期': datetime.datetime.now().strftime('%Y-%m-%d')
        }
    )
        
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(dump, f, indent=4)


def create_file(name: str, game: str, now_datetime: tuple) -> str:
    folder = f'{os.environ["USERPROFILE"]}/Saved Games/{game}'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/{game}/{name}_{now_datetime[0]}_{now_datetime[1]}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    return file


def load_text(file: str) -> str:
    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)