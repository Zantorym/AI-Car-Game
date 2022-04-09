import pygame

pygame.font.init()

FPS = 60
WIDTH = 1200
HEIGHT = 900
OFFSET = 100

# Color constants
GREY = pygame.Color(128, 128, 128)
BLACK = pygame.Color(0, 0, 0)
L_GREEN = pygame.Color(0, 220, 0, 255)
D_GREEN = pygame.Color(0, 80, 0)
DARK_RED = pygame.Color(255, 100, 100)

# Font constants
SPEED_FONT = pygame.font.SysFont('comicsans', 50)
POINTS_FONT = pygame.font.SysFont('comicsans', 50)
W_FONT = pygame.font.SysFont('comicsans', 32)
A_FONT = pygame.font.SysFont('comicsans', 32)
S_FONT = pygame.font.SysFont('comicsans', 32)
D_FONT = pygame.font.SysFont('comicsans', 32)

# Game related constants
COLLISION_EVENT = pygame.USEREVENT + 1
STOP_GAME_ON_GAMEOVER: bool = True
STOP_GAME_ON_WIN: bool = True

# Car related default values
STEER_MANEURABILITY = 5
MAX_STEER_ANGLE = 30
ACCELERATION = 0.05
MAX_ACCELERATION = 2
NATURAL_DECELERATION_MULTIPLIER = 0.1
NATURAL_STEERING_RETURN_MULTIPLIER = 0.5

# Ray related constants
DEGREES_BETWEEN_RAYS = 15
DEFAULT_RAY_LENGHT = 300
RAY_DRAW_COLOR = pygame.Color(255, 0, 0)

# Car starting positions per track
GAME_START_POSITIONS = [
    {
        'car_start_pos': (500, 809),
        'car_start_angle': 0,
        'goal_dimension': (10, 105),
        'goal_center_pos': (480, 808),
        'goal_rotation_deg': 0,
    },
    {
        'car_start_pos': (280, 317),
        'car_start_angle': 10,
        'goal_dimension': (10, 100),
        'goal_center_pos': (260, 320),
        'goal_rotation_deg': 10,
    },
    {
        'car_start_pos': (235, 770),
        'car_start_angle': 0,
        'goal_dimension': (10, 75),
        'goal_center_pos': (215, 771),
        'goal_rotation_deg': 0,
    },
]

# GameState tracking
SAVE_GAMESTATE_TO_FILE = True
GAMESTATE_SAVE_FILENAME_FORMAT = 'gamestates_{}.csv'

# Obstacles related
OBSTACLE_DEFAULT_RADIUS = 20
OBSTACLE_DEFAULT_COLOR = DARK_RED
