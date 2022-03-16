from typing import Tuple
import cv2
import pygame
import src.constants as CONSTANTS

class Track(pygame.sprite.Sprite):

    def __init__(self, track_id=''):
        super(Track, self).__init__()

        __TRACKS_DIR = 'assets/'
        self.track_id = track_id
        self.track_path = __TRACKS_DIR + "track" + str(track_id) + ".png"
        self.contours = self.setContours()

        self.image = pygame.image.load(self.track_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, CONSTANTS.OFFSET))
        self.mask = pygame.mask.from_surface(self.image)

    def setContours(self):
        image = cv2.imread(self.track_path)
        im_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # min_thresh = 128 and max_thresh = 255
        (thresh, im_bw) = cv2.threshold(im_bw, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def getContours(self):
        return self.contours

    def getImage(self):
        return pygame.image.load(self.track_path).convert()

    def get_at(self, abs_pt: Tuple[int, int]) -> pygame.Color:
        off_x = abs_pt[0] - self.rect.topleft[0]
        off_y = abs_pt[1] - self.rect.topleft[1]
        if 0 <= off_x <= self.rect.width and 0 <= off_y <= self.rect.height:
            return self.image.get_at((off_x, off_y))
        else:
            return None