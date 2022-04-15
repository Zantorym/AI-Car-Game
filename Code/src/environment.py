import numpy
import pygame
import src.constants as CONSTANTS
from typing import Tuple
from src.observations import Observations
from src.car import Car
from src.track import Track
from src.goal import Goal
from src.obstacle import Obstacle
from src.enums import *
from src.controls import GameControls


class Environment:
    def __init__(
        self,
        track_num: TrackNum,
        car_start: Tuple[int, int],
        car_angle: float,
        car_speed: float = 0.0,
        car_steer_angle: float = 0.0,
    ):
        self.track_num = track_num
        self.start_car_pos = car_start
        self.start_car_angle = car_angle
        self.start_car_speed = car_speed
        self.start_car_steer_angle = car_steer_angle

        self.track = Track(self.track_num)
        self.goal = Goal(*self.get_goal_settings())

        self.track_group = pygame.sprite.Group()
        self.track_group.add(self.track)
        self.goal_group = pygame.sprite.Group()
        self.goal_group.add(self.goal)

    def get_goal_settings(self):
        game_start_position = CONSTANTS.GAME_START_POSITIONS[self.track_num]
        goal_dimension = game_start_position['goal_dimension']
        goal_center = game_start_position['goal_center_pos']
        goal_rotation = game_start_position['goal_rotation_deg']
        return (goal_dimension, goal_center, goal_rotation)

    def reset(self):
        self.car = Car(self.start_car_pos, self.start_car_angle,
                       start_speed=self.start_car_speed,
                       start_steer_angle=self.start_car_steer_angle)
        self.observations: Observations = Observations(self.car, self.track)

        self.car_group = pygame.sprite.GroupSingle()
        self.car_group.add(self.car)

    def has_collide_track(self):
        return pygame.sprite.spritecollide(
            self.car,
            self.track_group,
            False,
            collided=pygame.sprite.collide_mask
        )

    def has_collide_goal(self):
        return pygame.sprite.spritecollide(
            self.car,
            self.goal_group,
            False,
            collided=pygame.sprite.collide_mask
        )

    def next(self, action: int):
        (steering, acceleration) = GameControls.action_to_car_controls(action)
        self.car.update(steering, acceleration)
        self.observations.update(self.car)
        self.game_over = self.has_collide_track()
        self.win = (not self.game_over) and self.has_collide_goal()

    def place_obstacle(self, obstacle: Obstacle):
        self.track.place_obstacle(obstacle, obstacle.rect)

    def render(self, surface: pygame.Surface, draw_rays: bool = False):
        surface.blit(self.track.image, self.track.rect)
        surface.blit(self.goal.image, self.goal.rect)
        surface.blit(self.car.image, self.car.rect)
        if draw_rays:
            self.observations.draw_rays(surface)

    def gamestate_as_np(self, action: int) -> numpy.array:
        np = numpy.array([
            *GameControls.actions_to_keys(action),
            self.car.speed, self.car.steer_angle,
            *self.observations.ray_lengths(),
            self.observations.distance_travelled,
            1 if self.game_over else 0,
            1 if self.win else 0,
        ])
        return np

    def observation(self) -> numpy.array:
        np = numpy.array([
            self.car.speed, self.car.steer_angle,
            *self.observations.ray_lengths(),
        ])
        return np
