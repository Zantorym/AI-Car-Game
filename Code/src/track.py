import pygame
import src.constants as CONSTANTS
from src.obstacle import Obstacle
from typing import Tuple
from src.commonUtils import resource_path


class Track(pygame.sprite.Sprite):

    def __init__(self, track_id=''):
        super(Track, self).__init__()

        __TRACKS_DIR = 'assets/'
        self.track_id = track_id
        self.track_path = __TRACKS_DIR + "track" + str(track_id) + ".png"

        self.image = pygame.image.load(resource_path(self.track_path)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, CONSTANTS.OFFSET))
        self.mask = pygame.mask.from_surface(self.image)

    def get_at(self, abs_pt: Tuple[int, int]) -> pygame.Color:
        off_x = abs_pt[0] - self.rect.topleft[0]
        off_y = abs_pt[1] - self.rect.topleft[1]
        if 0 <= off_x < self.rect.width and 0 <= off_y < self.rect.height:
            return self.image.get_at((off_x, off_y))
        else:
            return None

    def place_obstacle(self, obstacle: Obstacle, abs_pos):
        position = (abs_pos[0], abs_pos[1]-CONSTANTS.OFFSET)
        self.image.blit(obstacle.image, position)
        self.mask = pygame.mask.from_surface(self.image)
