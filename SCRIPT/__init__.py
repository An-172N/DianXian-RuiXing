# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权

import os

import pygame


asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')
char_image = pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_CHAR.png')).convert_alpha()
brick_image = pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_BRICK.png')).convert_alpha()
barrage_image = pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_BARRAGE.png')).convert_alpha()


import SCRIPT.KERNEL as KERNEL
import SCRIPT.GLOBAL as GLOBAL
import SCRIPT.GUI as GUI
import SCRIPT.KEY as KEY
import SCRIPT.RESET as RESET
import SCRIPT.HUMAN as HUMAN
import SCRIPT.SPRITE as SPRITE
import SCRIPT.COLLIDE as COLLIDE


update = KERNEL.update