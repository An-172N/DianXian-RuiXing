from typing import Iterator, Callable, Any


def load_files(key_file_list: list, load_func: Callable[[str], Any]) -> dict:
    file_dict = {}

    for key, file in key_file_list:
        file_dict[key] = load_func(file)

    return file_dict


def process_file(file: str, encoding: str, start_line: int, process_func: Callable[[int, str], Any]) -> Iterator[Any]:
    with open(file, 'r', encoding=encoding) as f:
        for row, line in enumerate(f, start=start_line):
            line = line.rstrip('\n')
            content = process_func(row, line)

            yield content