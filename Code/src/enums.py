from enum import Enum


class GameStatus(Enum):
    PLACE_OBSTACLES = 0
    ONGOING = 1
    GAME_OVER = 2
    WIN = 3


class PlayerType(Enum):
    PLAYER = 0
    AI = 1


class TrackNum(Enum):
    TRACK0 = 0
    TRACK1 = 1
    TRACK2 = 2


class CarStartPosType(Enum):
    TRACK_DEFAULTS = 0
    RANDOMIZED = 1


class Steering(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


class Acceleration(Enum):
    NONE = 0
    ACCELERATE = 1
    BRAKE = 2
