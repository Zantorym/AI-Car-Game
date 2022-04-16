import json
from random import choice, randint
from typing import Tuple
from src.environment import Environment
import src.constants as CONSTANTS


class EnvironmentCreator:
    def __init__(self,
                 randomize: bool = False,
                 settings_file: str = './env_random_settings.json',
                 has_goal: bool = True,
                 ):
        self.randomized = randomize
        self.has_goal = has_goal
        if randomize:
            self.random_settings = self.read_settings_file(settings_file)

    def create_environment(self,
                           track_num: int) -> Environment:
        if not self.randomized:
            env = Environment(
                track_num, *self.get_default_car_start(track_num),
                has_goal=self.has_goal)
            return env
        else:
            while True:
                # pos = self.generate_car_start_pos(track_num)
                # angle = self.generate_car_start_angle()
                (pos, angle) = self.generate_car_start_pos_n_angle(track_num)
                speed = self.generate_car_start_speed()
                steer_angle = self.generate_car_start_steer_angle()
                env = Environment(track_num, pos, angle, speed, steer_angle,
                                  has_goal=self.has_goal)
                env.reset()
                if self.is_valid_start(env):
                    return env

    def get_default_car_start(self, track_num: int):
        game_start_position = CONSTANTS.GAME_START_POSITIONS[track_num]
        start_pos = game_start_position['car_start_pos']
        start_angle = game_start_position['car_start_angle']
        return (start_pos, start_angle)

    def is_valid_start(self, env: Environment):
        return not (env.has_collide_track()
                    or env.has_collide_goal())

    def read_settings_file(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    def generate_car_start_pos_n_angle(self, track_num: int) -> Tuple[Tuple[int, int], int]:
        possible_settings = self.random_settings['car_start_pos_and_angle'][track_num]
        setting = choice(possible_settings)

        shift_x = self.random_settings['car_start_pos_shift_x']
        shift_y = self.random_settings['car_start_pos_shift_y']
        shifted_x = setting[0][0] + randint(-1 * shift_x, shift_x)
        shifted_y = setting[0][1] + randint(-1 * shift_y, shift_y)

        shift_angle = self.random_settings['car_start_shift_angle']
        shifted_angle = setting[1] + randint(-1 * shift_angle, shift_angle)

        return ((shifted_x, shifted_y), shifted_angle)

    def generate_car_start_pos(self, track_num: int) -> Tuple[int, int]:
        possible_start_pos = self.random_settings['car_start_positions'][track_num]
        shift_x = self.random_settings['car_start_pos_shift_x']
        shift_y = self.random_settings['car_start_pos_shift_y']

        start_pos = choice(possible_start_pos)
        shifted_x = start_pos[0] + randint(-1 * shift_x, shift_x)
        shifted_y = start_pos[1] + randint(-1 * shift_y, shift_y)
        return (shifted_x, shifted_y)

    def generate_car_start_angle(self) -> int:
        step_size = self.random_settings['car_start_angle_step_size']
        angle = randint(0, 359)
        angle = (angle // step_size) * step_size
        return angle

    def generate_car_start_speed(self) -> float:
        step_size = self.random_settings['car_start_speed_step_size']
        max_speed = CONSTANTS.MAX_SPEED
        steps = max_speed // step_size
        step = randint(0, steps)
        speed = step_size * step
        return speed

    def generate_car_start_steer_angle(self) -> float:
        step_size = self.random_settings['car_start_steer_angle_step_size']
        max_steer_angle = CONSTANTS.MAX_STEER_ANGLE
        steps = (max_steer_angle * 2) // step_size
        step = randint(0, steps)
        steer_angle = (step_size * step) - max_steer_angle
        return steer_angle
