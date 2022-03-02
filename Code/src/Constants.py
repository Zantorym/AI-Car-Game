import pygame

pygame.font.init()

FPS = 120
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