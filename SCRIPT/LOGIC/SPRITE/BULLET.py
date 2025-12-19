import random
import itertools

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.LOGIC.SPRITE.BRICK as BRICK
import SCRIPT.LOGIC.SPRITE.BARRAGE as BARRAGE
import SCRIPT.LOGIC.SPRITE.PARTICLE as PARTICLE
import SCRIPT.LOGIC.SPRITE.ITEM as ITEM
import SCRIPT.LOGIC.PROCESS.STAGE as STAGE


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

        PARTICLE.spawn_particles(
            2,
            2,
            VARIABLE.main_char.color,
            VARIABLE.main_char.rect.center,
            random.randint(6, 10)
        )

        VARIABLE.shoot_cnt -= 1


def single_bomb() -> None:
    if (
        not VARIABLE.is_s_divide
        and VARIABLE.s_power >= 12
    ):
        VARIABLE.s_power -= 12
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

        PARTICLE.spawn_particles(
            2,
            2,
            target.color,
            target_pos,
            random.randint(6, 10)
        )
            
        ITEM.item_spawn(target_pos)
        BRICK.brick_death(target)
        BARRAGE.spawn_barrage(target)
            
        target.kill()

    if source.type == "bullet":
        source.kill()