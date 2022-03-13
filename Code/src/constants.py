import pygame

pygame.font.init()

FPS = 60
WIDTH = 1200
HEIGHT = 900
OFFSET = 100
GREY = pygame.Color(128,128,128)
BLACK = pygame.Color(0,0,0)
L_GREEN = pygame.Color(0, 220, 0)
D_GREEN = pygame.Color(0,80,0)

SPEED_FONT = pygame.font.SysFont('comicsans', 50)
POINTS_FONT = pygame.font.SysFont('comicsans', 50)
W_FONT = pygame.font.SysFont('comicsans', 32)
A_FONT = pygame.font.SysFont('comicsans', 32)
S_FONT = pygame.font.SysFont('comicsans', 32)
D_FONT = pygame.font.SysFont('comicsans', 32)

COLLISION_EVENT = pygame.USEREVENT + 1

# Car related default values
STEER_MANEURABILITY = 5
MAX_STEER_ANGLE = 30
ACCELERATION = 0.05
MAX_ACCELERATION = 2
NATURAL_DECELERATION_MULTIPLIER = 0.1
NATURAL_STEERING_RETURN_MULTIPLIER = 0.5