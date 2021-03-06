import pygame
import src.constants as CONSTANTS
from pygame import Surface, Vector2
from src.track import Track
from src.car import Car
from src.ray import Ray
from src.commonUtils import normalize_angle


class Observations:
    def __init__(self, car: Car, track: Track):
        self.car_position: Vector2 = car.position.copy()
        self.car_facing: float = car.angle
        self.car_speed: float = car.speed
        self.car_steer_angle: float = car.steer_angle
        self.distance_travelled: float = 0.0
        self.track = track
        self.track_mask = track.mask
        self.track_topleft = track.rect.topleft

        self.obstacle_hit = 0
        self.finish_line_reached = 0

        self.update_rays()

    def update_rays(self):
        rays = []  # Each value is a tuple of ((start_pos), (end_pos), length)
        for angle in range(0, 181, CONSTANTS.DEGREES_BETWEEN_RAYS):
            # starts 90 degrees to the right
            ray_angle = normalize_angle(self.car_facing - 90.0 + angle)
            ray = Ray(self.car_position,
                      CONSTANTS.DEFAULT_RAY_LENGTH, ray_angle)
            # ray_end = Vector2(ray.get_pt_int_w_mask(self.track_mask, self.track_topleft))
            ray_end = Vector2(ray.get_pt_int_w_track(self.track))
            length = Vector2(ray_end - self.car_position).length()
            rays.append((self.car_position, ray_end, length))
        self.rays = rays

    def update(self, car: Car):
        last_pos = self.car_position
        self.car_position = car.position.copy()
        self.car_facing = car.angle
        self.car_speed: float = car.speed
        self.car_steer_angle: float = car.steer_angle
        self.distance_travelled += Vector2(self.car_position -
                                           last_pos).length()
        self.update_rays()

    def draw_rays(self, surface: Surface):
        for ray in self.rays:
            pygame.draw.line(surface, CONSTANTS.RAY_DRAW_COLOR, ray[0], ray[1])

    def ray_lengths(self):
        return [ray[2] for ray in self.rays]

    def set_obstacle_hit(self, val: bool):
        self.obstacle_hit = 1 if val else 0

    def set_finish_line_reached(self, val: bool):
        self.finish_line_reached = 1 if val else 0
