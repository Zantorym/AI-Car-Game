import pygame
import src.constants as CONSTANTS

class Goal(pygame.sprite.Sprite):

    def __init__(self, dimensions, center, rotation):
        super(Goal, self).__init__()

        surface = pygame.Surface(dimensions, pygame.SRCALPHA)
        surface.fill(CONSTANTS.L_GREEN)
        self.image = pygame.transform.rotate(surface, rotation)
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)