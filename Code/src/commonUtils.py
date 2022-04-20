import os
import numpy
from typing import Tuple
from pygame import Color, Vector2
from src import constants as CONSTANTS
import sys

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
        with open(resource_path(CONSTANTS.GAMESTATE_SAVE_FILENAME), 'ab') as f:
            numpy.savetxt(f, gamestates, fmt='%5.10f')

def load_gamestates_from_csv() -> numpy.ndarray:
    filename = CONSTANTS.GAMESTATE_SAVE_FILENAME
    if os.path.exists(resource_path(filename)) and os.path.isfile(resource_path(filename)):
        np = numpy.loadtxt(resource_path(filename))
        return np
