from .commonUtils import myPoint, myLine, rotate, distance, rotateRect
from .ray import Ray
import src.Constants as c
from math import sin, radians, degrees
import pygame
import cv2
from pygame.math import Vector2
from enum import Enum

GOALREWARD = 1

class Steering(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

class Acceleration(Enum):
    NONE = 0
    ACCELERATE = 1
    DECELERATE = 2

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0.0, sprite_path='assets/car.png',
                manueverability=c.STEER_MANEURABILITY,
                max_steering=c.MAX_STEER_ANGLE,
                acceleration=c.ACCELERATION,
                max_acceleration=c.MAX_ACCELERATION):
        super(Car, self).__init__()

        self.position = Vector2((x, y))
        self.velocity = Vector2((0, 0))

        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.vehicle_length = self.sprite.get_width()

        self.angle = angle
        self.steer_angle = 0
        self.speed = 0

        self.maneuverability_value = manueverability
        self.max_steering = max_steering
        self.acceleration_value = acceleration
        self.max_acceleration = max_acceleration

        self.image = self.sprite.copy()
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, steering, acceleration):
        self.accelerate(acceleration)
        self.steer(steering)
        self.velocity = Vector2(self.speed, 0)

        if self.steer_angle:
            turning_radius = self.vehicle_length / sin(radians(self.steer_angle))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0.0

        self.position += self.velocity.rotate(-self.angle)
        self.angle += degrees(angular_velocity)

        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)


    def steer(self, steering):
        if steering == Steering.LEFT:
            self.steer_angle += self.maneuverability_value
            self.steer_angle = min(self.steer_angle, self.max_steering)
        elif steering == Steering.RIGHT:
            self.steer_angle -= self.maneuverability_value
            self.steer_angle = max(self.steer_angle, -self.max_steering)
        else:
            if self.steer_angle > 0.0:
                self.steer_angle -= self.maneuverability_value * 0.5
                self.steer_angle = max(self.steer_angle, 0.0)
            elif self.steer_angle < 0.0:
                self.steer_angle += self.maneuverability_value * 0.5
                self.steer_angle = min(self.steer_angle, 0.0)
    
    def accelerate(self, acceleration):
        if acceleration == Acceleration.ACCELERATE:
            self.speed += self.acceleration_value            
        elif acceleration == Acceleration.DECELERATE:
            self.speed -= self.acceleration_value
        else:
            self.speed -= self.acceleration_value * 0.5
        
        self.speed = max(0, min(self.speed, self.max_acceleration))    

    ################
    # OLD CODE BELOW
    ################

    # def __init__(self, x, y, car_path='assets/car.png'):
    #     self.pt = myPoint(x, y)
    #     self.x = x
    #     self.y = y
    #     self.width = 30
    #     self.height = 14

    #     self.points = 0

    #     if car_path:
    #         self.original_image = pygame.image.load(car_path).convert_alpha()
    #         self.original_image.set_colorkey((0, 0, 0))
    #         self.image = self.original_image.copy()  # This will reference the rotated image.
    #     self.rect = self.image.get_rect().move(self.x, self.y)

    #     self.angle = math.radians(180)
    #     self.soll_angle = self.angle

    #     self.dvel = 1
    #     self.vel = 0
    #     self.velX = 0
    #     self.velY = 0
    #     self.maxvel = 15  # before 15

    #     # self.angle = math.radians(180)
    #     # self.soll_angle = self.angle

    #     self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
    #     self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
    #     self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
    #     self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

    #     self.p1 = self.pt1
    #     self.p2 = self.pt2
    #     self.p3 = self.pt3
    #     self.p4 = self.pt4

    #     # print(self.p1, self.p2, self.p3, self.p4)  # TODO: to check which point corresponds to which corner

    #     self.distances = []

    # def respawn(self):
    #     self.__init__(500, 300)

    # def action(self, choice):
    #     if choice == 0:                     # Continue straight with same speed
    #         pass
    #     elif choice == 1:                   # Increase speed : W
    #         self.accelerate(self.dvel)
    #     elif choice == 2:                   # Turn left : A
    #         self.turn(1)
    #     elif choice == 3:                   # Decrease speed : S
    #         self.accelerate(-self.dvel)
    #     elif choice == 4:                   # Turn right : D
    #         self.turn(-1)
    #     pass

    # def accelerate(self, dvel):
    #     dvel = dvel

    #     self.vel = self.vel + dvel*0.5

    #     if self.vel > self.maxvel:
    #         self.vel = self.maxvel

    #     if self.vel < -self.maxvel:
    #         self.vel = -self.maxvel

    # def turn(self, dir):
    #     self.soll_angle = self.soll_angle + dir * math.radians(5)

    # def update(self):

    #     # drifting code

    #     # if(self.soll_angle > self.angle):
    #     #     if(self.soll_angle > self.angle + math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)):
    #     #         self.angle = self.angle + math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)
    #     #     else:
    #     #         self.angle = self.soll_angle

    #     # if(self.soll_angle < self.angle):
    #     #     if(self.soll_angle < self.angle - math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)):
    #     #         self.angle = self.angle - math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)
    #     #     else:
    #     #         self.angle = self.soll_angle

    #     self.angle = self.soll_angle

    #     vec_temp = rotate(myPoint(0, 0), myPoint(0, self.vel), self.angle)
    #     self.velX, self.velY = vec_temp.x, vec_temp.y

    #     self.x = self.x + self.velX
    #     self.y = self.y + self.velY

    #     self.rect.center = self.x, self.y

    #     self.pt1 = myPoint(self.pt1.x + self.velX, self.pt1.y + self.velY)
    #     self.pt2 = myPoint(self.pt2.x + self.velX, self.pt2.y + self.velY)
    #     self.pt3 = myPoint(self.pt3.x + self.velX, self.pt3.y + self.velY)
    #     self.pt4 = myPoint(self.pt4.x + self.velX, self.pt4.y + self.velY)

    #     self.p1, self.p2, self.p3, self.p4 = rotateRect(self.pt1, self.pt2, self.pt3, self.pt4, self.soll_angle)

    #     self.image = pygame.transform.rotate(self.original_image, 90 - self.soll_angle * 180 / math.pi)
    #     x, y = self.rect.center  # Save its current center.
    #     self.rect = self.image.get_rect()  # Replace old rect with new rect.
    #     self.rect.center = (x, y)

    # def cast(self, walls):

    #     ray1 = Ray(self.x, self.y, self.soll_angle)
    #     ray2 = Ray(self.x, self.y, self.soll_angle - math.radians(30))
    #     ray3 = Ray(self.x, self.y, self.soll_angle + math.radians(30))
    #     ray4 = Ray(self.x, self.y, self.soll_angle + math.radians(45))
    #     ray5 = Ray(self.x, self.y, self.soll_angle - math.radians(45))
    #     ray6 = Ray(self.x, self.y, self.soll_angle + math.radians(90))
    #     ray7 = Ray(self.x, self.y, self.soll_angle - math.radians(90))
    #     ray8 = Ray(self.x, self.y, self.soll_angle + math.radians(180))

    #     ray9 = Ray(self.x, self.y, self.soll_angle + math.radians(10))
    #     ray10 = Ray(self.x, self.y, self.soll_angle - math.radians(10))
    #     ray11 = Ray(self.x, self.y, self.soll_angle + math.radians(135))
    #     ray12 = Ray(self.x, self.y, self.soll_angle - math.radians(135))
    #     ray13 = Ray(self.x, self.y, self.soll_angle + math.radians(20))
    #     ray14 = Ray(self.x, self.y, self.soll_angle - math.radians(20))

    #     ray15 = Ray(self.p1.x, self.p1.y, self.soll_angle + math.radians(90))
    #     ray16 = Ray(self.p2.x, self.p2.y, self.soll_angle - math.radians(90))

    #     ray17 = Ray(self.p1.x, self.p1.y, self.soll_angle + math.radians(0))
    #     ray18 = Ray(self.p2.x, self.p2.y, self.soll_angle - math.radians(0))

    #     self.rays = []
    #     self.rays.append(ray1)
    #     self.rays.append(ray2)
    #     self.rays.append(ray3)
    #     self.rays.append(ray4)
    #     self.rays.append(ray5)
    #     self.rays.append(ray6)
    #     self.rays.append(ray7)
    #     self.rays.append(ray8)

    #     self.rays.append(ray9)
    #     self.rays.append(ray10)
    #     self.rays.append(ray11)
    #     self.rays.append(ray12)
    #     self.rays.append(ray13)
    #     self.rays.append(ray14)

    #     self.rays.append(ray15)
    #     self.rays.append(ray16)

    #     self.rays.append(ray17)
    #     self.rays.append(ray18)

    #     observations = []
    #     self.closestRays = []

    #     for ray in self.rays:
    #         closest = None  # myPoint(0,0)
    #         record = math.inf
    #         for wall in walls:
    #             pt = ray.cast(wall)
    #             if pt:
    #                 dist = distance(myPoint(self.x, self.y), pt)
    #                 if dist < record:
    #                     record = dist
    #                     closest = pt

    #         if closest:
    #             # append distance for current ray
    #             self.closestRays.append(closest)
    #             observations.append(record)

    #         else:
    #             observations.append(1000)

    #     for i in range(len(observations)):
    #         # invert observation values 0 is far away 1 is close
    #         observations[i] = ((1000 - observations[i]) / 1000)

    #     observations.append(self.vel / self.maxvel)
    #     return observations

    # def check_collision(self, contours_list):
    #     """
    #     :argument
    #     contours_list: A list that containing the list of the outer points of the track and the inner points of the track

    #     Function to return if the car is inside a track or outside
    #     """
    #     points = [self.p1, self.p2, self.p3, self.p4]
    #     for point in points:
    #         outer_bool = cv2.pointPolygonTest(contours_list[0], point.getPoint(), False)
    #         inner_bool = cv2.pointPolygonTest(contours_list[1], point.getPoint(), False)
    #         print(outer_bool, inner_bool)
    #         if not (outer_bool == 1 and inner_bool == 1):
    #             # TODO: Collision occurs
    #             pygame.event.post(pygame.event.Event(c.COLLISION_EVENT))

    # def score(self, goal):

    #     line1 = myLine(self.p1, self.p3)

    #     vec = rotate(myPoint(0, 0), myPoint(0, -50), self.angle)
    #     line1 = myLine(myPoint(self.x, self.y), myPoint(self.x + vec.x, self.y + vec.y))

    #     x1 = goal.x1
    #     y1 = goal.y1
    #     x2 = goal.x2
    #     y2 = goal.y2

    #     x3 = line1.pt1.x
    #     y3 = line1.pt1.y
    #     x4 = line1.pt2.x
    #     y4 = line1.pt2.y

    #     den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    #     if (den == 0):
    #         den = 0
    #     else:
    #         t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    #         u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    #         if t > 0 and t < 1 and u < 1 and u > 0:
    #             pt = math.floor(x1 + t * (x2 - x1)), math.floor(y1 + t * (y2 - y1))

    #             d = distance(myPoint(self.x, self.y), myPoint(pt[0], pt[1]))
    #             if d < 20:
    #                 # pygame.draw.circle(win, (0,255,0), pt, 5)
    #                 self.points += GOALREWARD
    #                 return (True)

    #     return (False)

    # def reset(self):

    #     self.x = 50
    #     self.y = 300
    #     self.velX = 0
    #     self.velY = 0
    #     self.vel = 0
    #     self.angle = math.radians(180)
    #     self.soll_angle = self.angle
    #     self.points = 0

    #     self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
    #     self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
    #     self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
    #     self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

    #     self.p1 = self.pt1
    #     self.p2 = self.pt2
    #     self.p3 = self.pt3
    #     self.p4 = self.pt4

    # def draw(self, win):
    #     win.blit(self.image, self.rect)
