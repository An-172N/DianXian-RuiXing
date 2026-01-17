# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import sys


def main() -> int:
    import pygame

    pygame.display.init()
    pygame.font.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((480, 360), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED, vsync=1)
    title = pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')

    import SCRIPT.KERNEL

    SCRIPT.KERNEL.update(clock, screen, title)

    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    
    block_module = [
        'numpy', 'timidity',
        'pygame._freetype', 'pygame._sdl2', 'pygame._camera',
        'pygame._camera_vidcapture', 'pygame._sprite', 'pygame._camera_opencv',
        'pygame.mixer_music', 'pygame.mixer', 'pygame.joystick',
        'pygame.gfxdraw', 'pygame.mouse', 'pygame.threads',
        'pygame.pypm', 'pygame.macosx', 'pygame.examples',
        'pygame.locals', 'pygame.camera', 'pygame.__pyinstaller',
        'pygame.freetype', 'pygame.midi', 'pygame.scrap',
        'gzip', 'calendar', 'html',
        'heapq', 'csv', 'logging',
        'urllib', 'pkgutil', 'cgi',
        'smtplib', 'multiprocessing', 'ensurepip',
        'venv', 'distutils', 'pdb',
        'tkinter', 'email', 'xml',
        'doctest', 'unittest', 'idlelib',
        'uu', 'ftplib', 'hashlib',
        'pathlib', 'mailcap', 'webbrowser',
        'quopri', 'cgitb', 'cmd',
        'imaplib', 'imghdr', 'platform',
        'poplib', 'tarfile', 'xdrlib',
        'zipfile', 'lzma', 'pstats',
        'sndhdr', 'shlex', 'sched',
        'pipes', 'netrc', 'pprint',
        'string', 'stringprep', 'struct',
        'symtable', 'timeit', 'tomllib',
        'socketserver', 'unicodedata', 'rlcompleter',
        'numbers', 'nturl2path', 'token',
        'tokenize', 'colorsys', 'code',
        'codeop', 'configparser', 'dis',
        'linecache', 'inspect', 'bz2',
        'opcode', 'select', 'selectors',
        'base64', 'chunk', 'copy',
        'dataclasses', 'difflib', 'fileinput',
        'filecmp', 'getopt', 'glob',
        'fractions', 'decimal', 'statistics',
        'tempfile', 'mimetypes', 'modulefinder',
        'pickle', 'pickletools', 'pyclbr',
        'rlcompleter', 'sysconfig', 'textwrap'
    ]

    for module in block_module:
        sys.modules[module] = None

    main()