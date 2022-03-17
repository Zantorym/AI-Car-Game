import pygame
import src.constants as CONSTANTS
from enum import Enum
from math import sin, radians, degrees
from pygame.math import Vector2

class Steering(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

class Acceleration(Enum):
    NONE = 0
    ACCELERATE = 1
    BRAKE = 2

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0.0, sprite_path='assets/car.png',
                manueverability=CONSTANTS.STEER_MANEURABILITY,
                max_steering=CONSTANTS.MAX_STEER_ANGLE,
                acceleration=CONSTANTS.ACCELERATION,
                max_acceleration=CONSTANTS.MAX_ACCELERATION):
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
                self.steer_angle -= self.maneuverability_value * CONSTANTS.NATURAL_STEERING_RETURN_MULTIPLIER
                self.steer_angle = max(self.steer_angle, 0.0)
            elif self.steer_angle < 0.0:
                self.steer_angle += self.maneuverability_value * CONSTANTS.NATURAL_STEERING_RETURN_MULTIPLIER
                self.steer_angle = min(self.steer_angle, 0.0)
    
    def accelerate(self, acceleration):
        if acceleration == Acceleration.ACCELERATE:
            self.speed += self.acceleration_value            
        elif acceleration == Acceleration.BRAKE:
            self.speed -= self.acceleration_value
        else:
            self.speed -= self.acceleration_value * CONSTANTS.NATURAL_DECELERATION_MULTIPLIER
        
        self.speed = max(0, min(self.speed, self.max_acceleration))