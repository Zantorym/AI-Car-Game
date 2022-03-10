import cv2
import pygame


class Track:

    def __init__(self, track_id=''):
        __TRACKS_DIR = 'assets/'
        self.track_id = track_id
        self.track_path = __TRACKS_DIR + "track" + str(track_id) + ".png"
        self.contours = self.setContours()

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