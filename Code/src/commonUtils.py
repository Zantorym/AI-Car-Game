from typing import Tuple
from pygame import Color, Vector2

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
