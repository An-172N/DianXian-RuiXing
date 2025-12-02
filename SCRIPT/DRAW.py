import pygame


class ShapeDraw:
    def __init__(self, width, height, border, color):
        self.width = width
        self.height = height
        self.border = border
        self.color = color

    def polygon(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        side_length = min(self.width, self.height)
        height_polygon = (3 ** 0.5) / 2 * side_length
        center_x = self.width // 2
        center_y = self.height // 2
        point1 = (center_x, center_y - height_polygon / 2)
        point2 = (center_x - side_length / 2, center_y + height_polygon / 2)
        point3 = (center_x + side_length / 2, center_y + height_polygon / 2)

        pygame.draw.polygon(surface, self.color, [point1, point2, point3], self.border)

        return surface

    def rect(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(surface, self.color, surface.get_rect(), self.border)

        return surface

    def circle(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        center_x = self.width // 2
        center_y = self.height // 2
        radius = min(self.width, self.height) // 2

        pygame.draw.circle(surface, self.color, (center_x, center_y), radius, self.border)

        return surface