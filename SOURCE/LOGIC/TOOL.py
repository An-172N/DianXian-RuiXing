# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def vector(present: tuple, target: tuple, speed: float) -> tuple:
    dir = pygame.math.Vector2(target[0] - present[0], target[1] - present[1])
    current = pygame.math.Vector2(present[0], present[1])
    target = pygame.math.Vector2(target[0], target[1])

    delta_vec = target - current
    distance = delta_vec.length()

    if distance < speed:
        return target, delta_vec
    else:
        if distance > 0:
            dir.normalize_ip()

        return current + dir * speed, delta_vec


def pop_text_animate(surface: pygame.Surface, font: pygame.font.Font, group: list, timer: int, interval: tuple, color: tuple=(255, 255, 255)) -> tuple:
    def for_text(timer: int, interval: int, gather: list) -> None:
        if timer >= interval:
            for i in gather:
                text = font.render(i["text"], False, color).convert_alpha()
                surface.blit(text, i["pos"])

    for_text(timer, interval[0], group[0])
    for_text(timer, interval[1], group[1])
    for_text(timer, interval[2], group[2])

    if timer < interval[2]:
        timer += 1

    return surface, timer


def update_fps(fps: object, timer: int, bit: int, interval: int, clock: pygame.time.Clock) -> tuple:
    current_time = pygame.time.get_ticks()

    if current_time - timer >= interval:
        fps = f"{clock.get_fps():.{bit}f} FPS"
        timer = current_time

    return fps, timer


def draw_rectangle(size: tuple, border: float, color: tuple) -> pygame.Surface:
    surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)

    pygame.draw.rect(surface, color, surface.get_rect(), border)

    return surface


def draw_circle(xy_size: tuple, border: float, color: tuple) -> pygame.Surface:
    surface = pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA)

    pygame.draw.ellipse(surface, color, xy_size, border)

    return surface


def round_angle(angle, step=10):
    angle %= 360
    if angle >= 180:
        angle -= 180

    rounded = round(angle / step) * step
    if rounded == 180:
        rounded = 0

    return rounded


def replace_illegal_char(string: str) -> str:
    return string.translate(str.maketrans('!<>:"/\\|?*', '__________'))


def add(*tuples: tuple) -> tuple:
    return tuple(map(sum, zip(*tuples)))


def fibonacci(former: int, latter: int, frequency: int) -> int:
    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(min(value, max(minimum, maximum)), min(minimum, maximum))