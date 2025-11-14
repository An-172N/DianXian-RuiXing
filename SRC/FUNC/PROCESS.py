def load_files(file_key_list, load_func):
    """
    加载多个文件
    
    Args:
        file_key_list: 一个列表，里面存有若干个由文件名和键值组成的元组
        load_func: 加载函数，它接收文件

    Returns:
        存有加载完毕后的文件的字典
    """

    file_dict = {}

    for key, file in file_key_list:
        file_dict[key] = load_func(file)

    return file_dict


def process_file(file, encoding, start_line, process_func):
    """
    处理文件中的数据

    Args:
        file: 要处理的文件
        encoding: 指定的编码格式
        start_line: 开始处理的行数
        process_func: 处理函数，它接收行号和行内容

    Yields:
        所有处理函数返回的值
    """

    with open(file, 'r', encoding=encoding) as f:
        for row, line in enumerate(f, start=start_line):
            line = line.rstrip('\n')
            content = process_func(row, line)

            yield content