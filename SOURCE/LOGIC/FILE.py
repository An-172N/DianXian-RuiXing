# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import json
import os
from typing import Callable, Any


def save_record(
    folder: str,
    file: str,
    title: str,
    append: str
) -> None:
    def return_path_with_makedir(
        folder: str,
        file: str
    ) -> str:
        if not os.path.exists(folder):
            os.makedirs(folder)

        return f'{folder}/{file}'

    dump = [title]
    dump.append(append)

    with open(return_path_with_makedir(folder, file), 'w', encoding='utf-8') as f:
        return json.dump(dump, f, indent=4)


def read_level(
    file: bytes,
    load: Callable[..., Any],
    *args: Any
) -> str:
    content = file.decode('ascii')
    lines = content.splitlines()

    for row, line in enumerate(lines):
        load(row, line, *args)

    return content


def get_files(
    folder: str,
    extension: str = '.json',
    reverse: bool = True
) -> list[str]:
    files = []

    try:
        for file in os.listdir(folder):
            if file.endswith(extension):
                path = os.path.join(folder, file)

                if os.path.isfile(path):
                    time = os.path.getmtime(path)

                    files.append((time, path))
    except:
        return []

    files.sort(key=lambda x: x[0], reverse=reverse)

    return [path for _, path in files]