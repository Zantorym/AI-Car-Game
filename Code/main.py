import sys
import pygame
import numpy as np
import pandas as pd
from os.path import exists
import src.constants as CONSTANTS
import argparse
from enum import Enum
from typing import List
from src.model import predict_action
from src.game_state import GameState
from src.car import Car, Steering, Acceleration
from src.track import Track
from src.goal import Goal
from src.obstacle import Obstacle
from src.commonUtils import print_text, create_df_for_model

from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    KEYDOWN,
    QUIT,
    K_ESCAPE,
)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--player", help="who is playing the game: human or ai", default='ai')
args = vars(ap.parse_args())

class GameStatus(Enum):
    ONGOING = 0
    GAME_OVER = 1
    WIN = 2
    PLACE_OBSTACLES = 3


pygame.init()
pygame.font.init()

pygame.display.set_caption("Crazy Driver")
SCREEN = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
SCREEN.fill((255, 255, 255))

action_space = None
observation_space = None
game_reward = 0
score = 0
player = args['player']
save_gamestate = player == 'human'


key_strokes = {'w': False, 'a': False, 's': False, 'd': False}

def show_key_strokes(surface, key_strokes):
    active = CONSTANTS.D_GREEN
    default = CONSTANTS.GREY
    w = active if key_strokes[K_w] else default
    a = active if key_strokes[K_a] else default
    s = active if key_strokes[K_s] else default
    d = active if key_strokes[K_d] else default

    pygame.draw.rect(surface, w, (55, 7, 40, 40))
    pygame.draw.rect(surface, a, (5, 53, 40, 40))
    pygame.draw.rect(surface, s, (55, 53, 40, 40))
    pygame.draw.rect(surface, d, (105, 53, 40, 40))

    surface.blit(CONSTANTS.W_FONT.render(
        f'W', True, CONSTANTS.BLACK), dest=(65, 18))  # W
    surface.blit(CONSTANTS.A_FONT.render(
        f'A', True, CONSTANTS.BLACK), dest=(17, 62))  # A
    surface.blit(CONSTANTS.S_FONT.render(
        f'S', True, CONSTANTS.BLACK), dest=(67, 62))  # S
    surface.blit(CONSTANTS.D_FONT.render(
        f'D', True, CONSTANTS.BLACK), dest=(117, 62))  # D


def render_controls(surface, key_strokes):
    # Display visual indicator of keys pressed state
    show_key_strokes(surface, key_strokes)

    # Display boxes as borders for keys
    pygame.draw.rect(surface, CONSTANTS.BLACK, (55, 7, 40, 40), 2)  # W
    pygame.draw.rect(surface, CONSTANTS.BLACK, (5, 53, 40, 40), 2)  # A
    pygame.draw.rect(surface, CONSTANTS.BLACK, (55, 53, 40, 40), 2)  # S
    pygame.draw.rect(surface, CONSTANTS.BLACK, (105, 53, 40, 40), 2)  # D


def update_car(car, keys_pressed, ai_keys_action):
    steering = Steering.NONE
    acceleration = Acceleration.NONE

    if (keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]) or (ai_keys_action['a'] and not ai_keys_action['d']):
        steering = Steering.LEFT
    elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a] or (ai_keys_action['d'] and not ai_keys_action['a']):
        steering = Steering.RIGHT

    if keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s] or (ai_keys_action['w'] and not ai_keys_action['s']):
        acceleration = Acceleration.ACCELERATE
    elif keys_pressed[pygame.K_s] and not keys_pressed[pygame.K_w] or (ai_keys_action['s'] and not ai_keys_action['w']):
        acceleration = Acceleration.BRAKE

    car.update(steering, acceleration)


def save_gamestates_to_csv(gamestates: np.ndarray):
    if gamestates is not None:
        gamedata = create_df_for_model(gamestates, CONSTANTS.COLUMN_NAMES)
        print(gamedata)
        if exists(CONSTANTS.GAMESTATE_FILE):
            gamedata.to_csv(CONSTANTS.GAMESTATE_FILE, mode='a', header=False)
        else:
            gamedata.to_csv(CONSTANTS.GAMESTATE_FILE)


def main(num):
    clock = pygame.time.Clock()

    current_game_status = GameStatus.PLACE_OBSTACLES

    track_num = num
    ai_keys_action = CONSTANTS.DEFAULT_ACTION_DICT

    # Setting the car starting position for the track
    game_start_position = CONSTANTS.GAME_START_POSITIONS[int(track_num)]
    car_start_x = game_start_position['car_start_pos'][0]
    car_start_y = game_start_position['car_start_pos'][1]
    car_start_angle = game_start_position['car_start_angle']
    # Setting the goal position for the track
    goal_dimension = game_start_position['goal_dimension']
    goal_center = game_start_position['goal_center_pos']
    goal_rotation = game_start_position['goal_rotation_deg']

    track = Track(track_num)
    goal = Goal(goal_dimension, goal_center, goal_rotation)
    car = Car(car_start_x, car_start_y, car_start_angle,
              sprite_path='assets/car.png')
    gamestate = GameState(car, track)
    if (save_gamestate):
        gamestates_np = None

    all_sprites_group = pygame.sprite.Group()
    all_sprites_group.add(track)
    all_sprites_group.add(car)
    obstacles_group = pygame.sprite.Group()
    obstacles_group.add(track)
    goal_group = pygame.sprite.Group()
    goal_group.add(goal)
    car_group = pygame.sprite.GroupSingle()
    car_group.add(car)
    obstacles: List[Obstacle] = []

    keys_pressed = pygame.key.get_pressed()
    running = True
    while running:
        mouse_down = False

        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

        if player == 'human':
            for event in pygame.event.get():
                # Checking user event
                keys_pressed = pygame.key.get_pressed()
        else:
            if(current_game_status != GameStatus.PLACE_OBSTACLES):
                print('sdikbfjb')
                # Get data from current state in a numpy array
                current_gamedata = [gamestate.to_numpy()[4:19]]
                x = create_df_for_model(current_gamedata, CONSTANTS.TRAINING_NAMES)
                # Send data to trained model and get results
                actions = predict_action(x).flatten()
                print(actions)
                # Fire events based on result
                # pygame.event.clear()
                # if bool(actions[0]):
                #     pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w))
                # if bool(actions[1]):
                #     pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
                # if bool(actions[2]):
                #     pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
                # if bool(actions[3]):
                #     pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
                ai_keys_action = {
                    'w': bool(actions[0]),
                    'a': bool(actions[1]),
                    's': bool(actions[2]),
                    'd': bool(actions[3])
                }

        # Only update car and game status if not yet game over
        if (not (current_game_status == GameStatus.GAME_OVER and CONSTANTS.STOP_GAME_ON_GAMEOVER)) and \
                (not (current_game_status == GameStatus.WIN and CONSTANTS.STOP_GAME_ON_WIN)):

            # Handle mouse
            if mouse_down:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if CONSTANTS.PRINT_MOUSE_CLICK_LOCATION:
                    print((mouse_x, mouse_y))
                if current_game_status == GameStatus.PLACE_OBSTACLES:
                    obstacle = Obstacle((mouse_x, mouse_y))
                    track.place_obstacle(obstacle, obstacle.rect)
                    obstacles.append(obstacle)
                    if len(obstacles) == CONSTANTS.MAX_OBSTACLES_PER_TRACK:
                        current_game_status = GameStatus.ONGOING

            # Update car attributes
            if current_game_status != GameStatus.PLACE_OBSTACLES:
                # Handle game functions
                update_car(car, keys_pressed, ai_keys_action)
                # Update gamestate
                gamestate.update(car, keys_pressed)

            # Rendering
            SCREEN.fill((255, 255, 255))
            SCREEN.blit(track.image, track.rect)
            SCREEN.blit(goal.image, goal.rect)
            car.draw(SCREEN)
            # Create surface for controls display
            controls_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
            render_controls(controls_surface, keys_pressed)
            SCREEN.blit(controls_surface, (900, 0))
            if current_game_status == GameStatus.PLACE_OBSTACLES:
                mouse_loc = pygame.mouse.get_pos()
                pygame.draw.circle(SCREEN, CONSTANTS.YELLOW,
                                   mouse_loc, CONSTANTS.OBSTACLE_DEFAULT_RADIUS)
            else:
                # Draw rays on screen
                gamestate.draw_rays(SCREEN)

            # Collision Detection
            if current_game_status == GameStatus.PLACE_OBSTACLES:
                # No collision detection during placing of obstacles
                pass
            elif (pygame.sprite.spritecollide(car, obstacles_group, False, collided=pygame.sprite.collide_mask)):
                # returned list is not empty
                current_game_status = GameStatus.GAME_OVER
                gamestate.set_obstacle_hit(True)
                gamestate.set_finish_line_reached(False)
            elif (pygame.sprite.spritecollide(car, goal_group, False, collided=pygame.sprite.collide_mask)):
                current_game_status = GameStatus.WIN
                gamestate.set_obstacle_hit(False)
                gamestate.set_finish_line_reached(True)
            else:
                current_game_status = GameStatus.ONGOING
                gamestate.set_obstacle_hit(False)
                gamestate.set_finish_line_reached(False)

            # Save gamestate to a numpy array
            if current_game_status == GameStatus.ONGOING and save_gamestate:
                if gamestates_np is None:
                    gamestates_np = [gamestate.to_numpy()]
                else:
                    gamestates_np = np.append(
                        gamestates_np, [gamestate.to_numpy()], axis=0)
            if current_game_status == GameStatus.GAME_OVER or current_game_status == GameStatus.WIN:
                save_gamestates_to_csv(gamestates_np)
                gamestates_np = None

            if (current_game_status == GameStatus.GAME_OVER):
                print_text(SCREEN, 'GAME OVER', pygame.font.Font(None, 128))
            elif (current_game_status == GameStatus.WIN):
                print_text(SCREEN, 'TRAINING MODEL NOW', pygame.font.Font(None, 128))

            # Update Screen
            pygame.display.flip()

        clock.tick(CONSTANTS.FPS)

    pygame.quit()
    sys.exit()



# if __name__ == '__main__':
#     main()
