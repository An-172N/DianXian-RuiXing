import pygame as pyg

import SCRIPT.DICT
import FUNC
from SCRIPT.LOGIC.FRIEND import DecPt


win = pyg.Rect((120, 15,
                345, 330))
eff = pyg.Rect((105, 0,
                375, 360))
pln_grp = pyg.sprite.Group()
blt_grp = pyg.sprite.Group()
brc_grp = pyg.sprite.Group()
item_grp = pyg.sprite.Group()
brg_grp = pyg.sprite.Group()
ptcl_grp = pyg.sprite.Group()
run = False
pau = False
summ = False
talk = False
sav = False
level_ld = False
is_rst = False

bg = pyg.image.load('ASSET\IMG_GAMEBG.png').convert_alpha()
last_time = pyg.time.get_ticks()
fps_txt = last_time

name = ''

spt = 0
can_shoot = False

bw_ctr = 150
comb = 0

player = 4
no_hurt = 0
sc = 0
cd_ctr = 0
sflash = 0
ttl_spt = 0
stg_ttl_spt = 0
ttl_spwn_spt = 0
mv_right = False
mv_left = False
is_slow = False
is_visitable = True
is_sdivide = False
coll = True
main_char = SCRIPT.DICT.char_dict.get(4)()
d_pt = DecPt()

txt_num = 0
txt_pt = 0
ctr = 0
stage = 1
level = 0
pic_list = [
    (1, 'ASSET/IMG_STAGE1BG.png'),
    (2, 'ASSET/IMG_STAGE2BG.png'),
    (3, 'ASSET/IMG_STAGE3BG.png')
]
pic = FUNC.Process.load_files(pic_list, lambda f: pyg.image.load(f).convert_alpha())
sec_bg = pic[stage]
sec_bg.set_alpha(159)
char = None
txt = None