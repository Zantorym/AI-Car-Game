import pygame
import src.constants as CONSTANTS
from typing import Tuple


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, center: Tuple[int, int],
                 radius: int = CONSTANTS.OBSTACLE_DEFAULT_RADIUS,
                 color: pygame.Color = CONSTANTS.OBSTACLE_DEFAULT_COLOR):
        super(Obstacle, self).__init__()

        self.color = color
        self.diameter = radius * 2
        self.radius = radius

        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (radius, radius), radius)
        self.image = surface
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)
