import cv2
import pygame
import src.constants as CONSTANTS
from src.game_state import GameState
from src.car import Car, Steering, Acceleration
from src.track import Track
from src.commonUtils import print_text

import sys

from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    KEYDOWN,
    QUIT,
    K_ESCAPE,
)

pygame.init()
pygame.font.init()

pygame.display.set_caption("Crazy Driver")
SCREEN = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
SCREEN.fill((255, 255, 255))

# track_back_image = track.getImage().convert()
# track_back_rect = track_back_image.get_rect().move(0, c.OFFSET))

action_space = None
observation_space = None
game_reward = 0
score = 0

key_strokes = {'w': False, 'a': False, 's': False, 'd': False}

# def display_track_background():
#     SCREEN.blit(track.image, track.rect)

def show_key_strokes(surface, key_strokes):
    active = CONSTANTS.D_GREEN
    default = CONSTANTS.BLACK
    w = active if key_strokes[K_w] else default
    a = active if key_strokes[K_a] else default
    s = active if key_strokes[K_s] else default
    d = active if key_strokes[K_d] else default

    # pygame.draw.rect(SCREEN, w_bg, (905, 5, 40, 40), 2)  # W
    # pygame.draw.rect(SCREEN, a_bg, (855, 55, 40, 40), 2)  # A
    # pygame.draw.rect(SCREEN, s_bg, (905, 55, 40, 40), 2)  # S
    # pygame.draw.rect(SCREEN, d_bg, (955, 55, 40, 40), 2)  # D

    SCREEN.blit(CONSTANTS.W_FONT.render(f'W', True, w), dest=(907, 5))  # W
    SCREEN.blit(CONSTANTS.A_FONT.render(f'A', True, a), dest=(857, 55))  # A
    SCREEN.blit(CONSTANTS.S_FONT.render(f'S', True, s), dest=(907, 55))  # S
    SCREEN.blit(CONSTANTS.D_FONT.render(f'D', True, d), dest=(957, 55))  # D


def render_controls(surface, key_strokes):
    # screen.fill(tuple(c.BLACK))
    # screen.blit(back_image, back_rect)

    # # TODO: Update car pos
    # car.update()
    # car.draw(screen)

    # if action == 1:
    #     pygame.draw.rect(screen, (0, 255, 0), (850, 50, 40, 40))
    # if action == 2:
    #     pygame.draw.rect(screen, (0, 255, 0), (800, 100, 40, 40))
    # if action == 3:
    #     pygame.draw.rect(screen, (0, 255, 0), (850, 100, 40, 40))
    # if action == 4:
    #     pygame.draw.rect(screen, (0, 255, 0), (900, 100, 40, 40))

    # Key-strokes info
    show_key_strokes(surface, key_strokes)

    # # score
    # text_surface = c.POINTS_FONT.render(f'Points {car.points}', True, pygame.Color('green'))
    # screen.blit(text_surface, dest=(0, 0))
    # # speed
    # text_surface = c.SPEED_FONT.render(f'Speed {car.vel * -1}', True, pygame.Color('green'))
    # screen.blit(text_surface, dest=(420, 0))



def update_car(car, keys_pressed):
    steering = Steering.NONE
    acceleration = Acceleration.NONE

    if keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]:
        steering = Steering.LEFT
    elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]:
        steering = Steering.RIGHT

    if keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s]:
        acceleration = Acceleration.ACCELERATE
    elif keys_pressed[pygame.K_s] and not keys_pressed[pygame.K_w]:
        acceleration = Acceleration.DECELERATE

    car.update(steering, acceleration)

car_start_x = CONSTANTS.WIDTH / 2
car_start_y = CONSTANTS.HEIGHT / 2
car_start_angle = 45

def main():
    clock = pygame.time.Clock()
    # data = []

    track = Track(2)
    car = Car(car_start_x, car_start_y, car_start_angle, sprite_path='assets/car.png')
    gamestate = GameState(car, track)

    all_sprites_group = pygame.sprite.Group()
    all_sprites_group.add(track)
    all_sprites_group.add(car)
    obstacles_group = pygame.sprite.Group()
    obstacles_group.add(track)
    car_group = pygame.sprite.GroupSingle()
    car_group.add(car)

    running = True
    while running:
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        # Checking user event
        keys_pressed = pygame.key.get_pressed()

        # Handle game functions
        update_car(car, keys_pressed)
        # car.update(keys_pressed)
        # Update gamestate
        gamestate.update(car)
                
        # Rendering
        # display_track_background()
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(track.image, track.rect)
        car.draw(SCREEN)
        render_controls(SCREEN, keys_pressed)
        gamestate.draw_rays(SCREEN)

        # Collision Detection
        if (pygame.sprite.spritecollide(car, obstacles_group, False, collided=pygame.sprite.collide_mask)):
            # returned list is not empty
            collision_detected = True
        else:
            collision_detected = False

        if (collision_detected):
            print_text(SCREEN, 'COLLISSION', pygame.font.Font(None, 64))
        else:
            print_text(SCREEN, 'NO', pygame.font.Font(None, 64))

        # Update Screen
        pygame.display.flip()


        clock.tick(CONSTANTS.FPS)

    pygame.quit()
    sys.exit()

    # while True:
    #     clock.tick(c.FPS)
    #     for event in pygame.event.get():

    #         # Exiting the game
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()

    #         if event.type == c.COLLISION_EVENT:
    #             # TODO: action to be done on collision
    #             # car.respawn()
    #             pygame.quit()
    #             sys.exit()

    #         # Checking user event
    #         keys_pressed = pygame.key.get_pressed()
    #         actions = []
    #         action = 0
    #         if keys_pressed[pygame.K_w]:
    #             # Increase speed
    #             action = 1
    #         if keys_pressed[pygame.K_a]:
    #             # Turn left
    #             action = 2
    #         if keys_pressed[pygame.K_s]:
    #             # Decrease Speed
    #             action = 3
    #         if keys_pressed[pygame.K_d]:
    #             # Turn right
    #             action = 4
    #         # TODO: do we want to implement a mechanism for constant speed without a key press
    #         car.action(action)
    #         actions.append(action)

    #         # Store the user data for imitation learning
    #         # wall_distance = car.get_wall_distance()
    #         # data.append([wall_distance, actions])

    #         # if event.type == env.terminate_run:
    #         #     env.return_to_home()

    #     key_strokes = {
    #         'w': keys_pressed[pygame.K_w],
    #         'a': keys_pressed[pygame.K_a],
    #         's': keys_pressed[pygame.K_s],
    #         'd': keys_pressed[pygame.K_d]
    #     }

    #     car.check_collision(track.getContours())
    #     render(car, action, SCREEN, key_strokes)
    #     pygame.display.update()


if __name__ == '__main__':
    main()
