import pygame
from pygame import Vector2, Surface
from src.commonUtils import normalize_angle
from typing import Tuple
# from .commonUtils import myPoint, rotate
# import math

class Ray():
    def __init__(self, start: Vector2, length: int, angle: int):
        self.start = start
        self.length = length
        self.angle = 0

        # Get the vector (length and direction) representation of ray
        self.vector = Vector2(length, 0)
        # Vector from start point to center of ray
        self.center = self.vector * 0.5

        surface = Surface((length, 1), pygame.SRCALPHA)
        surface.fill((255, 0, 0, 255))
        self.image = surface
        self.surface = self.image.copy()
        self.rect = self.image.get_rect(topleft=self.start)
        
        self.rotate(angle)

    def rotate(self, angle):
        self.angle = normalize_angle(self.angle + angle)
        self.vector.rotate_ip(-angle)
        self.center = self.vector * 0.5
        surface = self.image.copy()
        self.surface = pygame.transform.rotate(surface, self.angle)
        self.rect = self.surface.get_rect(center=self.start+self.center)

    def draw(self, surface: Surface):
        surface.blit(self.surface, self.rect)

    def get_pt_int_w_mask(self, mask : pygame.mask.Mask, mask_topleft: Tuple[int, int]) -> Tuple[int, int]:
        (offset_x, offset_y) = (mask_topleft[0]-self.rect.topleft[0], mask_topleft[1]-self.rect.topleft[1])
        selfmask = pygame.mask.from_surface(self.surface)

        self_w, self_h = selfmask.get_size()
        mask_w, mask_h = mask.get_size()

        for y in range(self_h-1, -1, -1) if 0 < self.angle <= 180 else range(self_h):
            for x in range(self_w-1, -1, -1) if 0 < self.angle <= 180 else range(self_w):
                if selfmask.get_at((x, y)) and (0 <= x - offset_x < mask_w and 0 <= y - offset_y < mask_h and mask.get_at((x - offset_x, y - offset_y))):
                    return x + self.rect.topleft[0], y + self.rect.topleft[1]
                    
        # No overlap, return the end point of the ray
        endpoint = Vector2(self.start) + self.vector
        return endpoint.x, endpoint.y

################
# OLD CODE BELOW
################

# class Ray:
#     def __init__(self, x, y, angle):
#         self.x = x
#         self.y = y
#         self.angle = angle

#     def cast(self, wall):
#         x1 = wall.x1
#         y1 = wall.y1
#         x2 = wall.x2
#         y2 = wall.y2

#         vec = rotate(myPoint(0, 0), myPoint(0, -1000), self.angle)

#         x3 = self.x
#         y3 = self.y
#         x4 = self.x + vec.x
#         y4 = self.y + vec.y

#         den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

#         if (den == 0):
#             den = 0
#         else:
#             t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
#             u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

#             if t > 0 and t < 1 and u < 1 and u > 0:
#                 pt = myPoint(math.floor(x1 + t * (x2 - x1)), math.floor(y1 + t * (y2 - y1)))
#                 return (pt)