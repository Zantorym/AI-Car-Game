import cv2


class Track:

    def __init__(self, track_id=1):
        __TRACKS_DIR = '../assets/'
        self.track_id = track_id
        self.track_path = __TRACKS_DIR + "track" + track_id + ".png"
        self.setContours()

    def setContours(self):
        image = cv2.imread(self.track_path)
        im_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # min_thresh = 128 and max_thresh = 255
        (thresh, im_bw) = cv2.threshold(im_bw, 128, 255, 0)
        contours, _ = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def getContours(self):
        return self.contours
