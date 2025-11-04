def find_match(source_group, target_group, match_func):
    match_list = []

    for i in source_group:
        for j in target_group:
            if match_func(i, j):
                match_list.append((i, j))

    return match_list


def load_files(file_with_key, load_func):
    file_dict = {}

    for file, key in file_with_key:
        file_dict[key] = load_func(file)

    return file_dict


def process_file(file, mode, process_func):
    with open(file, mode) as f:
        return process_func(f)