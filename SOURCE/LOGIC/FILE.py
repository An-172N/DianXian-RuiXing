# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import json
import os


def save_record(
    folder: str,
    file: str,
    title: str,
    append: object
):
    def return_file_with_makedir(
        folder: str,
        file: str
    ) -> str:
        if not os.path.exists(folder):
            os.makedirs(folder)

        return f'{folder}/{file}'

    dump = [title]
    dump.append(append)

    with open(return_file_with_makedir(folder, file), 'w', encoding='utf-8') as f:
        return json.dump(dump, f, indent=4)


def read_level(
    file: bytes,
    load: object,
    *args
) -> str:
    content = file.decode('ascii')
    lines = content.splitlines()

    for row, line in enumerate(lines):
        load(row, line, *args)

    return content