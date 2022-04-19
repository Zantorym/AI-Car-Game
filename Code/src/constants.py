import pygame

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
YELLOW = pygame.Color(220, 220, 0)

# Game related constants
COLLISION_EVENT = pygame.USEREVENT + 1
STOP_GAME_ON_GAMEOVER: bool = True
STOP_GAME_ON_WIN: bool = True
PRINT_MOUSE_CLICK_LOCATION: bool = True

# Car related default values
STEER_MANEURABILITY = 5
MAX_STEER_ANGLE = 30
ACCELERATION = 0.05
MAX_SPEED = 2
NATURAL_DECELERATION_MULTIPLIER = 0.1
NATURAL_STEERING_RETURN_MULTIPLIER = 0.5

# Ray related constants
DEGREES_BETWEEN_RAYS = 15
DEFAULT_RAY_LENGTH = 300
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
GAMESTATE_SAVE_FILENAME = 'assets/gamestate/gamestates.csv'
SAVE_TRAINED_MODEL_TO_FILE = True
TRAINED_MODEL_SAVE_FILENAME = 'assets/model/ai-model.pkl'

# Obstacles related
OBSTACLE_DEFAULT_RADIUS = 20
OBSTACLE_DEFAULT_COLOR = DARK_RED
MAX_OBSTACLES_PER_TRACK = 3

# AI training related
BATCH_SIZE = 512
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.001
EPS_DECAY = 5000
TARGET_UPDATE = 10
REPLAY_MEMORY_SIZE = 10000
NUM_EPISODES = 100
MAX_TIMESTEPS_PER_EPISODE = 15000
CUTOFF_DISTANCE_FOR_REWARD = 0.30
