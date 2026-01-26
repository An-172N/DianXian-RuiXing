# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import json
import os


def dump_file(file: str, title: str, append: object) -> None:
    dump = [title]
    dump.append(append)

    with open(file, 'w', encoding='utf-8') as f:
        return json.dump(dump, f, indent=4)


def return_file(name: str, game: str, now_datetime: tuple) -> str:
    folder = f'{os.environ["USERPROFILE"]}/Saved Games/{game}'
    file = f'{os.environ["USERPROFILE"]}/Saved Games/{game}/{name}_{now_datetime[0]}_{now_datetime[1]}.json'

    if not os.path.exists(folder):
        os.makedirs(folder)

    return file


def load_text(file: str) -> str:
    with open(file, 'r', encoding="utf-8") as f:
        return json.load(f)