from typing import Iterator, Callable, Any


def load_files(files: list, func: Callable[[str], Any]) -> dict:
    return {
        key: func(file)
        for key, file in files
    }


def process_file(file: str, encoding: str, start: int, func: Callable[[int, str], Any]) -> Iterator[Callable[[int, str], Any]]:
    with open(file, 'r', encoding=encoding) as f:
        yield from (
            func(row, line.rstrip('\n'))
            for row, line in enumerate(f, start=start)
        )