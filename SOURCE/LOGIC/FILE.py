# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import json
import os


def dump_file(file: str, title: str, append: object) -> None:
    dump = [title]
    dump.append(append)

    with open(file, 'w', encoding='utf-8') as f:
        return json.dump(dump, f, indent=4)


def return_file_with_makedir(folder: str, file: str) -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)

    return f'{folder}/{file}'


def read_level(file: str, load: object, *args: tuple) -> str:
    with open(file, 'r', encoding="ascii") as f:
        string = f.read().splitlines()

        for row, line in enumerate(string):
            load(row, line, *args)

        return string