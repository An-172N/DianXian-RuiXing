# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

from SOURCE import HUMAN, SPRITE, PRELOAD


window = pygame.Rect(120, 15, 345, 330)
effective = pygame.Rect(70, -50, 410, 410)


is_run = False
is_pause = False
is_summary = False
is_talk = False
is_save = False
is_level_load = False
is_blit = False


name = ''


power = 0
shoot_counter = 0


is_shoot = True


item_spawn_timer = 0
combo_timer = 120
combo = 0


flash = 3
no_flash = 0
score = 0
cooldown_timer = 0
use_flash = 0
total_power = 0
stage_total_power = 0


is_move_right = False
is_move_left = False
is_fast = False
is_visitable = True
is_s_divide = False
is_collide = True


text_number = 0
text_part = 0
wait_level_load_timer = 0
stage = 1
level = 0


background = PRELOAD.picture[6]
second_background = PRELOAD.picture[stage]


char = None
text = None


plane_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
barrage_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()


main_char = HUMAN.Kli(bullet_group, particle_group)
decision_point = SPRITE.Rect.Rect((2, 2), 0, (128, 128, 128))


last_time = pygame.time.get_ticks()
fps_text = last_time