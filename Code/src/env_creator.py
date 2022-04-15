from src.environment import Environment
import src.constants as CONSTANTS


class EnvironmentCreator:
    def __init__(self,
                 randomize: bool = False,
                 settings_file: str = './env_random_settings.json'
                 ):
        self.randomized = randomize

    def create_environment(self,
                           track_num: int) -> Environment:
        if not self.randomized:
            env = Environment(track_num, *self.get_default_car_start(track_num))
            return env
        else:
            is_valid = False
            while not is_valid:
                pass

    def get_default_car_start(self, track_num: int):
        game_start_position = CONSTANTS.GAME_START_POSITIONS[track_num]
        start_pos = game_start_position['car_start_pos']
        start_angle = game_start_position['car_start_angle']
        return (start_pos, start_angle)

    def is_valid_start(self, env: Environment):
        return not (env.has_collide_track()
                    or env.has_collide_goal())
