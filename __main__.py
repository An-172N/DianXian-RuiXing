# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议

import sys
import os
import zipfile
import argparse
import random


def read_resource(file):
    try:
        with zipfile.ZipFile(sys.argv[0], 'r') as zf:
            with zf.open(file) as f:
                return f.read().decode('utf-8')
    except:
        path = os.path.join(os.path.dirname(__file__), file)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()


def main():
    title = '锐行 ~ Thunder Out of the Mountain'
    version = '1.2.3'
    author = 'An_172N'
    sys.dont_write_bytecode = True
    sys.modules['numpy'] = None
    parser = argparse.ArgumentParser()
    for i, j in (('-s', 1), ('-l', 1), ('-f', 3), ('-p', 0), ('-sd', None)):
        parser.add_argument(i, type=int, default=j)
    args = parser.parse_args()
    random.seed(args.sd)
    while True:
        choose = input(
            f"={title}==================\n"
            "TH：去锐山\n"
            "R ：读我\n"
            "L ：程序代码许可\n"
            "Q ：回家吃烤鸡扒\n"
            f"==============================Ver {version} | By {author}=\n"
        ).upper()
        if choose == "TH":
            import pygame

            clock = pygame.time.Clock()
            pygame.display.init()
            pygame.font.init()
            pygame.mixer.init()
            pygame.mixer.set_num_channels(2)

            import KERNEL

            pygame.display.set_caption(title)
            KERNEL.update(clock, (int(args.s), int(args.l), int(args.f), int(args.p)), version, title)
            os.execv(sys.executable, ['python'] + sys.argv)
        elif choose == "R":
            content = read_resource("README.md")
            print(content)
        elif choose == "L":
            content = read_resource("LICENSE")
            print(content)
        elif choose == "Q":
            print("还是奥尔良鸡扒？")
            break
        else:
            print("这是什么呀？")


if __name__ == "__main__":
    main()