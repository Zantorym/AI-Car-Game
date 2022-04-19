import os
import numpy
from typing import Tuple
from pygame import Color, Vector2
from src import constants as CONSTANTS


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)


def normalize_angle(angle):
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle


def normalize_vector_endpoint(endpoint: Vector2) -> Tuple[int, int]:
    return (round(endpoint.x), round(endpoint.y))


def is_intersecting_color(track_color: Color) -> bool:
    if not track_color:
        return False
    return track_color[3] == 255


def save_gamestates_to_csv(gamestates: numpy.ndarray):
    if gamestates is not None:
        with open(CONSTANTS.GAMESTATE_SAVE_FILENAME, 'ab') as f:
            numpy.savetxt(f, gamestates, fmt='%5.10f')

def load_gamestates_from_csv() -> numpy.ndarray:
    filename = CONSTANTS.GAMESTATE_SAVE_FILENAME
    if os.path.exists(filename) and os.path.isfile(filename):
        np = numpy.loadtxt(filename)
        return np
