# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import json
import os


def record(
    folder: str,
    file: str,
    content: tuple[str, str],
    encoding: str = 'utf-8'
) -> None:
    def get_path_and_makedir(
        folder: str,
        file: str
    ) -> str:
        if not os.path.exists(folder):
            os.makedirs(folder)

        return f'{folder}/{file}'

    (
        dump := [content[0]],
        dump.append(content[1])
    )[0]

    with open(get_path_and_makedir(folder, file), 'w', encoding=encoding) as f:
        return json.dump(dump, f, indent=4)


def get(
    folder: str,
    extension: str = '.json',
    reverse: bool = True
) -> list[str]:
    try:
        files = []

        for file in os.listdir(folder):
            if file.endswith(extension) and os.path.isfile(path := os.path.join(folder, file)):
                time = os.path.getmtime(path)

                files.append((time, path))

        files.sort(key=lambda x: x[0], reverse=reverse)

        return [path for _, path in files]
    except:
        return []