import math

import pygame as pyg


def polygon(width, height, border, color):
    surface = pyg.Surface((width, height), pyg.SRCALPHA)

    side_length = min(width, height)
    height_polygon = math.sqrt(3) / 2 * side_length
    center_x = width // 2
    center_y = height // 2
    point1 = (center_x, center_y - height_polygon / 2)
    point2 = (center_x - side_length / 2, center_y + height_polygon / 2)
    point3 = (center_x + side_length / 2, center_y + height_polygon / 2)

    pyg.draw.polygon(surface, color, [point1, point2, point3], border)

    return surface


def rect(width, height, border, color):
    surface = pyg.Surface((width, height), pyg.SRCALPHA)

    pyg.draw.rect(surface, color, surface.get_rect(), border)

    return surface


def circle(width, height, border, color):
    surface = pyg.Surface((width, height), pyg.SRCALPHA)

    center_x = width // 2
    center_y = height // 2
    radius = min(width, height) // 2

    pyg.draw.circle(surface, color, (center_x, center_y), radius, border)

    return surface


def line(start_position, end_position, border, color):
    x_min = min(start_position[0], end_position[0])
    y_min = min(start_position[1], end_position[1])
    x_max = max(start_position[0], end_position[0])
    y_max = max(start_position[1], end_position[1])

    surface = pyg.Surface((x_max - x_min + border, y_max - y_min + border), pyg.SRCALPHA)

    start = (start_position[0] - x_min, start_position[1] - y_min)
    end = (end_position[0] - x_min, end_position[1] - y_min)
    pyg.draw.line(surface, color, start, end, border)

    return surface