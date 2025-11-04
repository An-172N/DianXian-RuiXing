def coordinate_difference(target_coordinate, source_coordinate):
    dx = target_coordinate[0] - source_coordinate[0]
    dy = target_coordinate[1] - source_coordinate[1]

    return dx, dy
    

def normalize(direction, magnitude):
    normalize_x = direction[0] / magnitude
    normalize_y = direction[1] / magnitude

    return normalize_x, normalize_y