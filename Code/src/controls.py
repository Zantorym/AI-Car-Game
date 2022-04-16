import pygame
from src.enums import Steering, Acceleration

'''
Mapping of Actions to Controls / vice-versa:
Action     Keys
0          -
1          w
2          s
3          a
4          d
5          wa
6          wd
7          sa
8          sd
'''


class GameControls:
    action_space_size: int = 9

    def __init__(self):
        pass

    @staticmethod
    def keys_to_actions(keys_pressed) -> int:
        keys: str = ''
        if keys_pressed[pygame.K_w]:
            keys += 'w'
        if keys_pressed[pygame.K_s]:
            keys += 's'
        if keys_pressed[pygame.K_a]:
            keys += 'a'
        if keys_pressed[pygame.K_d]:
            keys += 'd'

        if keys == 'w':
            return 1
        elif keys == 's':
            return 2
        elif keys == 'a':
            return 3
        elif keys == 'd':
            return 4
        elif keys == 'wa':
            return 5
        elif keys == 'wd':
            return 6
        elif keys == 'sa':
            return 7
        elif keys == 'sd':
            return 8
        else:
            return 0

    @staticmethod
    def actions_to_keys(action: int):
        if action in [1, 5, 6]:
            w = 1
        else:
            w = 0
        
        if action in [2, 7, 8]:
            s = 1
        else:
            s = 0

        if action in [3, 5, 7]:
            a = 1
        else:
            a = 0

        if action in [4, 6, 8]:
            d = 1
        else:
            d = 0
        
        return (w, a, s, d)

    @staticmethod
    def action_to_car_controls(action: int):
        if action in [1, 5, 6]:
            acceleration = Acceleration.ACCELERATE
        elif action in [2, 7, 8]:
            acceleration = Acceleration.BRAKE
        else:
            acceleration = Acceleration.NONE

        if action in [3, 5, 7]:
            steering = Steering.LEFT
        elif action in [4, 6, 8]:
            steering = Steering.RIGHT
        else:
            steering = Steering.NONE

        return (steering, acceleration)
