import random as rand
import itertools

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.LOGIC.SPRITE.BRICK as BRICK
import SCRIPT.LOGIC.SPRITE.BARRAGE as BARRAGE

from SCRIPT.LOGIC.FRIEND.BASE import Base
from SCRIPT.LOGIC.SPRITE import ITEM
from SCRIPT.LOGIC.PROCESS import STAGE


def spawn_bullet() -> None:
    if (
        VARIABLE.can_shoot
        and VARIABLE.shoot_cnt > 0
    ):
        p = 2 ** (VARIABLE.s_power // 32)
        q = 2 ** (VARIABLE.s_power // 16)

        for i, j in itertools.product(
            range(0, p),
            range(-q, q + 1, q)
        ):
            VARIABLE.main_char.bomb.fire(
                0 + i * 10,
                0 + i * 12,
                j
            )

        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 60):
            sprite = Base(
                (2, 2, 0),
                VARIABLE.main_char.color,
                1
            )
            sprite.speed = rand.randint(6, 10)
            sprite.rect.center = VARIABLE.main_char.rect.center
            sprite.current_angle = i
            VARIABLE.particle_group.add(sprite)

        VARIABLE.shoot_cnt -= 1


def single_bomb() -> None:
    if (
        not VARIABLE.is_s_divide
        and VARIABLE.s_power >= 16
    ):
        VARIABLE.s_power -= 16
        VARIABLE.is_s_divide = True


def bullet_collide(source, target) -> None:
    if source.type == "bullet":
        if getattr(target, 'is_die', False):
            source.kill()
            return

    target.hp -= source.damage
    VARIABLE.score += 64

    if target.hp <= 0:
        target.is_die = True
        target_pos = (target.rect.centerx, target.rect.centery)

        if hasattr(target, "bomb"):
            STAGE.shhm_lose()

        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 60):
            sprite = Base(
                (2, 2, 0),
                target.color,
                1
            )
            sprite.speed = rand.randint(6, 10)
            sprite.rect.center = target_pos
            sprite.current_angle = i
            VARIABLE.particle_group.add(sprite)
            
        ITEM.item_spawn(target_pos)
        BRICK.brick_death(target)
        BARRAGE.spawn_barrage(target)
            
        target.kill()

    if source.type == "bullet":
        source.kill()