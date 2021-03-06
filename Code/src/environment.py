import numpy
import pygame
import src.constants as CONSTANTS
from typing import Tuple
from sklearn.metrics.pairwise import euclidean_distances
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
        has_goal: bool = True,
        user_data: numpy.ndarray = None,
    ):
        self.track_num = track_num
        self.start_car_pos = car_start
        self.start_car_angle = car_angle
        self.start_car_speed = car_speed
        self.start_car_steer_angle = car_steer_angle

        self.track = Track(self.track_num)

        self.track_group = pygame.sprite.Group()
        self.track_group.add(self.track)

        self.has_goal = has_goal
        if has_goal:
            self.goal = Goal(*self.get_goal_settings())
            self.goal_group = pygame.sprite.Group()
            self.goal_group.add(self.goal)

        self.user_data = user_data
        if user_data is not None:
            self.user_data_controls = self.user_data[:, 0:4]
            self.user_data_observations = self.user_data[:, 4:-2]

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

        self.prev_state = self.observation()

    def has_collide_track(self):
        collisions = pygame.sprite.spritecollide(
            self.car,
            self.track_group,
            False,
            collided=pygame.sprite.collide_mask
        )
        return len(collisions) > 0

    def has_collide_goal(self):
        if not self.has_goal:
            return False

        collisions = pygame.sprite.spritecollide(
            self.car,
            self.goal_group,
            False,
            collided=pygame.sprite.collide_mask
        )
        return len(collisions) > 0

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
        if self.has_goal:
            surface.blit(self.goal.image, self.goal.rect)
        surface.blit(self.car.image, self.car.rect)
        if draw_rays:
            self.observations.draw_rays(surface)

    def gamestate_as_np(self, action: int) -> numpy.array:
        np = numpy.array([
            *GameControls.actions_to_keys(action),
            *self.observation(),
            # self.observations.distance_travelled,
            1 if self.game_over else 0,
            1 if self.win else 0,
        ])
        return np

    def observation(self) -> numpy.array:
        ray_lengths = numpy.array(self.observations.ray_lengths())
        ray_lengths = ray_lengths / CONSTANTS.DEFAULT_RAY_LENGTH
        speed = self.car.speed / CONSTANTS.MAX_SPEED
        steer_angle = self.car.steer_angle / CONSTANTS.MAX_STEER_ANGLE

        np = numpy.array([
            speed, steer_angle,
            *ray_lengths,
        ])
        return np

    def reward(self,
               prev_state: numpy.ndarray,
               next_state: numpy.ndarray,
               action: int) -> float:
        if self.user_data is None:
            return self.observation_based_reward(prev_state, next_state, action)
        else:
            return self.user_data_based_reward(prev_state, next_state, action)

    def observation_based_reward(self,
                                 prev_state: numpy.ndarray,
                                 next_state: numpy.ndarray,
                                 action: int) -> float:
        if self.game_over:
            return -1.0
        elif self.car.speed >= CONSTANTS.MAX_SPEED * 0.75:
            return self.car.speed / CONSTANTS.MAX_SPEED
        elif self.car.speed <= CONSTANTS.MAX_SPEED * 0.25:
            return -1.0 * (1.0 - (self.car.speed / CONSTANTS.MAX_SPEED))
        elif self.car.speed >= CONSTANTS.MAX_SPEED * 0.5:
            return 0.25
        else:
            return -0.25

    def user_data_based_reward(self,
                               prev_state: numpy.ndarray,
                               next_state: numpy.ndarray,
                               action: int) -> float:
        # Check first if game over
        if self.game_over:
            return -1.0

        # Otherwise compare against user action
        distances = euclidean_distances(
            numpy.expand_dims(prev_state, axis=0), self.user_data_observations)
        min_index = numpy.argmin(distances)
        min_distance = distances[0][min_index]
        user_control = self.user_data_controls[min_index]
        user_action = GameControls.gamestates_to_actions(user_control)
        if user_action == action:
            if min_distance <= CONSTANTS.CUTOFF_DISTANCE_FOR_REWARD:
                # print("Distance:", min_distance)
                return 1.0
            else:
                return 0.0
        else:
            return -1.0
        # elif GameControls.is_inverse_controls(user_action, action):
        #     return -1.0
        # else:
        #     return 0.0

    def done(self) -> bool:
        return self.game_over or self.win

    def step(self, action: int):
        self.next(action)
        next_state = self.observation()
        reward = self.reward(self.prev_state, next_state, action)
        done = self.done()
        self.prev_state = next_state
        return (next_state, reward, done, None)
