from enum import Enum


class GameStatus(Enum):
    PLACE_OBSTACLES = 0
    GAME_START = 1
    ONGOING = 2
    GAME_OVER = 3
    WIN = 4
    ESC = 5
    QUIT = 6


class PlayerType(Enum):
    PLAYER = 0
    AI = 1


class TrackNum(Enum):
    TRACK0 = 0
    TRACK1 = 1
    TRACK2 = 2


class Steering(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


class Acceleration(Enum):
    NONE = 0
    ACCELERATE = 1
    BRAKE = 2
