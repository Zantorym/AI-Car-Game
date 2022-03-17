import pygame
import src.constants as CONSTANTS
from typing import Tuple
from pygame import Vector2, Surface
from src.track import Track
from src.commonUtils import normalize_angle, normalize_vector_endpoint, is_intersecting_color

class Ray():
    def __init__(self, start: Vector2, length: int, angle: int):
        self.start = start
        self.length = length
        self.angle = 0

        # Get the vector (length and direction) representation of ray
        self.vector = Vector2(length, 0)
        
        self.rotate(angle)

    def rotate(self, angle):
        self.angle = normalize_angle(self.angle + angle)
        self.vector.rotate_ip(-angle)

    def draw(self, surface: Surface):
        pygame.draw.line(surface, CONSTANTS.RAY_DRAW_COLOR, self.start, (self.start + self.vector))

    def get_pt_int_w_track(self, track: Track) -> Tuple[int, int]:
        # Check lenght of 0
        if is_intersecting_color(track.get_at(normalize_vector_endpoint(self.start))):
            return normalize_vector_endpoint(self.start)

        for test_len in range(1, self.length):
            endpoint = self.vector.copy()
            endpoint.scale_to_length(test_len)
            endpoint += self.start
            endpoint = normalize_vector_endpoint(endpoint)
            if is_intersecting_color(track.get_at(endpoint)):
                return endpoint

        # default: return max length
        return normalize_vector_endpoint(self.start + self.vector)