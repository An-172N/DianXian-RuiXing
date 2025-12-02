def load_files(key_file_list, load_func):
    file_dict = {}

    for key, file in key_file_list:
        file_dict[key] = load_func(file)

    return file_dict


def process_file(file, encoding, start_line, process_func):
    with open(file, 'r', encoding=encoding) as f:
        for row, line in enumerate(f, start=start_line):
            line = line.rstrip('\n')
            content = process_func(row, line)

            yield content