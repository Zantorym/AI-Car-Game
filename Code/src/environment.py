import numpy
import pygame
import src.constants as CONSTANTS
from typing import List
from src.game_state import GameState
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
        car_start: CarStartPosType,
    ):
        self.track_num = track_num
        self.car_start_pos_type = car_start
        self.track = Track(self.track_num)
        self.goal = Goal(*self.get_goal_settings())

        self.track_group = pygame.sprite.Group()
        self.track_group.add(self.track)
        self.goal_group = pygame.sprite.Group()
        self.goal_group.add(self.goal)

    def get_default_car_start(self):
        game_start_position = CONSTANTS.GAME_START_POSITIONS[int(
            self.track_num)]
        start_pos = game_start_position['car_start_pos']
        start_angle = game_start_position['car_start_angle']
        return (start_pos, start_angle)

    def get_goal_settings(self):
        game_start_position = CONSTANTS.GAME_START_POSITIONS[self.track_num]
        goal_dimension = game_start_position['goal_dimension']
        goal_center = game_start_position['goal_center_pos']
        goal_rotation = game_start_position['goal_rotation_deg']
        return (goal_dimension, goal_center, goal_rotation)

    def reset(self):
        self.car = Car(*self.get_default_car_start())
        self.gamestate: GameState = GameState(self.car, self.track)

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

    def is_valid_start(self):
        return not (self.has_collide_track()
                    or self.has_collide_goal())

    def next(self, action: int):
        (steering, acceleration) = GameControls.action_to_car_controls(action)
        self.car.update(steering, acceleration)
        self.gamestate.update(self.car)
        self.game_over = self.has_collide_track()
        self.win = (not self.game_over) and self.has_collide_goal()

    def place_obstacle(self, obstacle: Obstacle):
        self.track.place_obstacle(obstacle, obstacle.rect)

    def render(self, surface: pygame.Surface, draw_rays: bool = False):
        surface.blit(self.track.image, self.track.rect)
        surface.blit(self.goal.image, self.goal.rect)
        surface.blit(self.car.image, self.car.rect)
        if draw_rays:
            self.gamestate.draw_rays(surface)

    def gamestate_as_np(self, action: int):
        np = numpy.array([
            *GameControls.actions_to_keys(action),
            self.car.speed, self.car.steer_angle,
            *self.gamestate.ray_lengths(),
            self.gamestate.distance_travelled,
            1 if self.game_over else 0,
            1 if self.win else 0,
        ])
        return np
