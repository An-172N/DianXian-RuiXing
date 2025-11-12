def load_files(files_with_keys, load_func):
    """加载多个文件"""

    file_dict = {}

    for file, key in files_with_keys:
        file_dict[key] = load_func(file)

    return file_dict


def line(start_position, end_position, border, color):
    x_min = min(start_position[0], end_position[0])
    y_min = min(start_position[1], end_position[1])
    x_max = max(start_position[0], end_position[0])
    y_max = max(start_position[1], end_position[1])

    surface = pyg.Surface((x_max - x_min + border, y_max - y_min + border), pyg.SRCALPHA)

    start = (start_position[0] - x_min, start_position[1] - y_min)
    end = (end_position[0] - x_min, end_position[1] - y_min)
    pyg.draw.line(surface, color, start, end, border)

    return surface