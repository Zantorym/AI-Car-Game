import pygame
from src import constants as CONSTANTS
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)


def show_key_strokes(surface, key_strokes):
    active = CONSTANTS.D_GREEN
    default = CONSTANTS.GREY
    w = active if key_strokes[K_w] else default
    a = active if key_strokes[K_a] else default
    s = active if key_strokes[K_s] else default
    d = active if key_strokes[K_d] else default

    pygame.draw.rect(surface, w, (55, 7, 40, 40))
    pygame.draw.rect(surface, a, (5, 53, 40, 40))
    pygame.draw.rect(surface, s, (55, 53, 40, 40))
    pygame.draw.rect(surface, d, (105, 53, 40, 40))

    surface.blit(CONSTANTS.W_FONT.render(
        f'W', True, CONSTANTS.BLACK), dest=(65, 18))  # W
    surface.blit(CONSTANTS.A_FONT.render(
        f'A', True, CONSTANTS.BLACK), dest=(17, 62))  # A
    surface.blit(CONSTANTS.S_FONT.render(
        f'S', True, CONSTANTS.BLACK), dest=(67, 62))  # S
    surface.blit(CONSTANTS.D_FONT.render(
        f'D', True, CONSTANTS.BLACK), dest=(117, 62))  # D


def render_controls(surface, key_strokes):
    # Display visual indicator of keys pressed state
    show_key_strokes(surface, key_strokes)

    # Display boxes as borders for keys
    pygame.draw.rect(surface, CONSTANTS.BLACK, (55, 7, 40, 40), 2)  # W
    pygame.draw.rect(surface, CONSTANTS.BLACK, (5, 53, 40, 40), 2)  # A
    pygame.draw.rect(surface, CONSTANTS.BLACK, (55, 53, 40, 40), 2)  # S
    pygame.draw.rect(surface, CONSTANTS.BLACK, (105, 53, 40, 40), 2)  # D
