import cv2
import pygame
from src.car import Car
from src.track import Track
import src.Constants as c

import sys

pygame.init()
pygame.font.init()

pygame.display.set_caption("Crazy Driver")
SCREEN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
SCREEN.fill((0, 0, 0))

track = Track()
back_image = track.getImage()
back_rect = back_image.get_rect().move(0, c.OFFSET)

action_space = None
observation_space = None
game_reward = 0
score = 0

key_strokes = {'w': False, 'a': False, 's': False, 'd': False}


def show_key_strokes(key_strokes):
    active = c.D_GREEN
    default = c.BLACK
    w = active if key_strokes['w'] else default
    a = active if key_strokes['a'] else default
    s = active if key_strokes['s'] else default
    d = active if key_strokes['d'] else default

    # pygame.draw.rect(SCREEN, w_bg, (905, 5, 40, 40), 2)  # W
    # pygame.draw.rect(SCREEN, a_bg, (855, 55, 40, 40), 2)  # A
    # pygame.draw.rect(SCREEN, s_bg, (905, 55, 40, 40), 2)  # S
    # pygame.draw.rect(SCREEN, d_bg, (955, 55, 40, 40), 2)  # D

    SCREEN.blit(c.W_FONT.render(f'W', False, w), dest=(907, 5))  # W
    SCREEN.blit(c.A_FONT.render(f'A', True, a), dest=(857, 55))  # A
    SCREEN.blit(c.S_FONT.render(f'S', True, s), dest=(907, 55))  # S
    SCREEN.blit(c.D_FONT.render(f'D', True, d), dest=(957, 55))  # D


def render(car, action, screen, key_strokes):
    screen.fill(tuple(c.BLACK))
    screen.blit(back_image, back_rect)

    # TODO: Update car pos
    car.update()
    car.draw(screen)

    if action == 1:
        pygame.draw.rect(screen, (0, 255, 0), (850, 50, 40, 40))
    if action == 2:
        pygame.draw.rect(screen, (0, 255, 0), (800, 100, 40, 40))
    if action == 3:
        pygame.draw.rect(screen, (0, 255, 0), (850, 100, 40, 40))
    if action == 4:
        pygame.draw.rect(screen, (0, 255, 0), (900, 100, 40, 40))

    # Key-strokes info
    show_key_strokes(key_strokes)

    # score
    text_surface = c.POINTS_FONT.render(f'Points {car.points}', True, pygame.Color('green'))
    screen.blit(text_surface, dest=(0, 0))
    # speed
    text_surface = c.SPEED_FONT.render(f'Speed {car.vel * -1}', True, pygame.Color('green'))
    screen.blit(text_surface, dest=(420, 0))


def main():
    car = Car(500, 300)
    clock = pygame.time.Clock()
    data = []

    while True:
        clock.tick(c.FPS)
        for event in pygame.event.get():

            # Exiting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == c.COLLISION_EVENT:
                # TODO: action to be done on collision
                # car.respawn()
                pygame.quit()
                sys.exit()

            # Checking user event
            keys_pressed = pygame.key.get_pressed()
            actions = []
            action = 0
            if keys_pressed[pygame.K_w]:
                # Increase speed
                action = 1
            if keys_pressed[pygame.K_a]:
                # Turn left
                action = 2
            if keys_pressed[pygame.K_s]:
                # Decrease Speed
                action = 3
            if keys_pressed[pygame.K_d]:
                # Turn right
                action = 4
            # TODO: do we want to implement a mechanism for constant speed without a key press
            car.action(action)
            actions.append(action)

            # Store the user data for imitation learning
            # wall_distance = car.get_wall_distance()
            # data.append([wall_distance, actions])

            # if event.type == env.terminate_run:
            #     env.return_to_home()

        key_strokes = {
            'w': keys_pressed[pygame.K_w],
            'a': keys_pressed[pygame.K_a],
            's': keys_pressed[pygame.K_s],
            'd': keys_pressed[pygame.K_d]
        }

        car.check_collision(track.getContours())
        render(car, action, SCREEN, key_strokes)
        pygame.display.update()


if __name__ == '__main__':
    main()
