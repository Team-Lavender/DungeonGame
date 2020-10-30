import math
import random

def get_direction(pos_1, pos_2):
    dx = pos_2[0] - pos_1[0]
    dy = pos_2[1] - pos_1[1]
    length = math.sqrt(dx ** 2 + dy ** 2)
    return dx / length, dy / length

def get_angle(direction_vector):
    x = direction_vector[0]
    y = direction_vector[1]
    while y == 0:
        y = random.randint(-1, 1) / 100
    theta = math.atan(x / y)

    if y > 0:
        return math.degrees(theta) + 180
    if y < 0:
        return math.degrees(theta)

