import cv2
import math
from typing import Tuple
from pygame import Color, Vector2

def edge_detect(file_name, tresh_min=128, tresh_max=255):
    """
    :argument
    contours_list: A list that containing the list of the outer points of the track and the inner points of the track
    car_pos: the position of the car

    Function to return if the car is inside a track or outside
    """
    image = cv2.imread('../assets/track1.png')
    im_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    (thresh, im_bw) = cv2.threshold(im_bw, tresh_min, tresh_max, 0)
    contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    print(len(contours))
    print(contours)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('cnt_' + file_name, image)


def distance(pt1, pt2):
    """
    :argument
    pt1: point 1 of instance myPoint
    pt2: point 2 of instance myPoint

    Return distance between 2 points
    """
    return (((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2) ** 0.5)


def rotate(origin, point, angle):
    """
    :argument
    origin: myPoint(0,0)
    point: initial point of instance myPoint
    angle: angle by which the point needs to be returned

    Returns the point rotated by an angle
    """
    qx = origin.x + math.cos(angle) * (point.x - origin.x) - math.sin(angle) * (point.y - origin.y)
    qy = origin.y + math.sin(angle) * (point.x - origin.x) + math.cos(angle) * (point.y - origin.y)
    q = myPoint(qx, qy)
    return q


def rotateRect(pt1, pt2, pt3, pt4, angle):
    """
    :argument
    pt1, pt2, pt3, pt4: points corresponding to the corners of a rectangle
    angle: angle by which the point needs to be returned

    Returns the all the points rotated by an angle (rotated rectangle)
    """

    pt_center = myPoint((pt1.x + pt3.x) / 2, (pt1.y + pt3.y) / 2)

    pt1 = rotate(pt_center, pt1, angle)
    pt2 = rotate(pt_center, pt2, angle)
    pt3 = rotate(pt_center, pt3, angle)
    pt4 = rotate(pt_center, pt4, angle)

    return pt1, pt2, pt3, pt4


class myPoint:
    """
    Class resonating an (x,y) coordinate on a 2D plane
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPoint(self):
        return self.x, self.y


class myLine:
    def __init__(self, pt1, pt2):
        self.pt1 = myPoint(pt1.x, pt1.y)
        self.pt2 = myPoint(pt2.x, pt2.y)

def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)

def normalize_angle(angle):
    while angle > 360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def normalize_vector_endpoint(endpoint: Vector2) -> Tuple[int, int]:
    return (round(endpoint.x), round(endpoint.y))

def is_intersecting_color(track_color: Color) -> bool:
    if not track_color:
        return False
    return track_color[3] == 255
