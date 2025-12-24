import pygame


class ShapeDraw:
    def __init__(self, width, height, border, color):
        self.width = width
        self.height = height
        self.border = border
        self.color = color

    def polygon(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        side = min(self.width, self.height)
        triangle_height = (3 ** 0.5) / 2 * side
        cx = self.width / 2
        cy = self.height / 2
        point1 = (cx, cy - triangle_height / 2)
        point2 = (cx - side / 2, cy + triangle_height / 2)
        point3 = (cx + side / 2, cy + triangle_height / 2)

        pygame.draw.polygon(surface, self.color, [point1, point2, point3], self.border)

        return surface

    def rect(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(surface, self.color, surface.get_rect(), self.border)

        return surface

    def circle(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        cx = self.width / 2
        cy = self.height / 2
        radius = min(self.width, self.height) / 2

        pygame.draw.circle(surface, self.color, (cx, cy), radius, self.border)

        return surface