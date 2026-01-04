from typing import Iterator, Callable, Any


def load_files(files: list, func: Callable[[str], Any]) -> dict:
    return {
        key: func(file)
        for key, file in files
    }


def process_file(string: str, start: int, func: Callable[[int, str], Any]) -> Iterator[Any]:
    yield from (
        func(row, line)
        for row, line in enumerate(string.splitlines(), start=start)
    )