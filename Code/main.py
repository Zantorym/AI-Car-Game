from src.game import Game

def main(track_num: int):
    game = Game(track_num)
    game.game_loop()

# import sys
# import pygame
# import numpy as np
# import src.constants as CONSTANTS
# from typing import List
# from src.game_state import GameState
# from src.car import Car, Steering, Acceleration
# from src.track import Track
# from src.goal import Goal
# from src.obstacle import Obstacle
# from src.commonUtils import print_text
# from pygame.locals import (
#     K_w,
#     K_a,
#     K_s,
#     K_d,
#     KEYDOWN,
#     QUIT,
#     K_ESCAPE,
# )


# pygame.init()
# pygame.font.init()

# pygame.display.set_caption("Crazy Driver")
# SCREEN = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
# SCREEN.fill((255, 255, 255))

# action_space = None
# observation_space = None
# game_reward = 0
# score = 0

# key_strokes = {'w': False, 'a': False, 's': False, 'd': False}


# def show_key_strokes(surface, key_strokes):
#     active = CONSTANTS.D_GREEN
#     default = CONSTANTS.GREY
#     w = active if key_strokes[K_w] else default
#     a = active if key_strokes[K_a] else default
#     s = active if key_strokes[K_s] else default
#     d = active if key_strokes[K_d] else default

#     pygame.draw.rect(surface, w, (55, 7, 40, 40))
#     pygame.draw.rect(surface, a, (5, 53, 40, 40))
#     pygame.draw.rect(surface, s, (55, 53, 40, 40))
#     pygame.draw.rect(surface, d, (105, 53, 40, 40))

#     surface.blit(CONSTANTS.W_FONT.render(
#         f'W', True, CONSTANTS.BLACK), dest=(65, 18))  # W
#     surface.blit(CONSTANTS.A_FONT.render(
#         f'A', True, CONSTANTS.BLACK), dest=(17, 62))  # A
#     surface.blit(CONSTANTS.S_FONT.render(
#         f'S', True, CONSTANTS.BLACK), dest=(67, 62))  # S
#     surface.blit(CONSTANTS.D_FONT.render(
#         f'D', True, CONSTANTS.BLACK), dest=(117, 62))  # D


# def render_controls(surface, key_strokes):
#     # Display visual indicator of keys pressed state
#     show_key_strokes(surface, key_strokes)

#     # Display boxes as borders for keys
#     pygame.draw.rect(surface, CONSTANTS.BLACK, (55, 7, 40, 40), 2)  # W
#     pygame.draw.rect(surface, CONSTANTS.BLACK, (5, 53, 40, 40), 2)  # A
#     pygame.draw.rect(surface, CONSTANTS.BLACK, (55, 53, 40, 40), 2)  # S
#     pygame.draw.rect(surface, CONSTANTS.BLACK, (105, 53, 40, 40), 2)  # D


# def update_car(car, keys_pressed):
#     steering = Steering.NONE
#     acceleration = Acceleration.NONE

#     if keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]:
#         steering = Steering.LEFT
#     elif keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]:
#         steering = Steering.RIGHT

#     if keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s]:
#         acceleration = Acceleration.ACCELERATE
#     elif keys_pressed[pygame.K_s] and not keys_pressed[pygame.K_w]:
#         acceleration = Acceleration.BRAKE

#     car.update(steering, acceleration)


# def save_gamestates_to_csv(gamestates: np.ndarray, suffix: str):
#     if gamestates is not None:
#         np.savetxt(CONSTANTS.GAMESTATE_SAVE_FILENAME_FORMAT.format(
#             suffix), gamestates, fmt='%10.5f', delimiter=',')


# def main(num):
#     clock = pygame.time.Clock()

#     current_game_status = GameStatus.PLACE_OBSTACLES

#     track_num = num

#     # Setting the car starting position for the track
#     game_start_position = CONSTANTS.GAME_START_POSITIONS[int(track_num)]
#     car_start_x = game_start_position['car_start_pos'][0]
#     car_start_y = game_start_position['car_start_pos'][1]
#     car_start_angle = game_start_position['car_start_angle']
#     # Setting the goal position for the track
#     goal_dimension = game_start_position['goal_dimension']
#     goal_center = game_start_position['goal_center_pos']
#     goal_rotation = game_start_position['goal_rotation_deg']

#     track = Track(track_num)
#     goal = Goal(goal_dimension, goal_center, goal_rotation)
#     car = Car(car_start_x, car_start_y, car_start_angle,
#               sprite_path='assets/car.png')
#     gamestate = GameState(car, track)
#     if (CONSTANTS.SAVE_GAMESTATE_TO_FILE):
#         gamestates_np = None

#     all_sprites_group = pygame.sprite.Group()
#     all_sprites_group.add(track)
#     all_sprites_group.add(car)
#     obstacles_group = pygame.sprite.Group()
#     obstacles_group.add(track)
#     goal_group = pygame.sprite.Group()
#     goal_group.add(goal)
#     car_group = pygame.sprite.GroupSingle()
#     car_group.add(car)
#     obstacles: List[Obstacle] = []

#     running = True
#     while running:
#         mouse_down = False
#         for event in pygame.event.get():
#             # Check for KEYDOWN event
#             if event.type == KEYDOWN:
#                 # If the Esc key is pressed, then exit the main loop
#                 if event.key == K_ESCAPE:
#                     running = False

#             # Check for QUIT event. If QUIT, then set running to false.
#             elif event.type == QUIT:
#                 running = False

#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_down = True

#             # Checking user event
#             keys_pressed = pygame.key.get_pressed()

#         # Only update car and game status if not yet game over
#         if (not (current_game_status == GameStatus.GAME_OVER and CONSTANTS.STOP_GAME_ON_GAMEOVER)) and \
#                 (not (current_game_status == GameStatus.WIN and CONSTANTS.STOP_GAME_ON_WIN)):

#             # Handle mouse
#             if mouse_down:
#                 mouse_x, mouse_y = pygame.mouse.get_pos()
#                 if CONSTANTS.PRINT_MOUSE_CLICK_LOCATION:
#                     print((mouse_x, mouse_y))
#                 if current_game_status == GameStatus.PLACE_OBSTACLES:
#                     obstacle = Obstacle((mouse_x, mouse_y))
#                     track.place_obstacle(obstacle, obstacle.rect)
#                     obstacles.append(obstacle)
#                     if len(obstacles) == CONSTANTS.MAX_OBSTACLES_PER_TRACK:
#                         current_game_status = GameStatus.ONGOING

#             if current_game_status != GameStatus.PLACE_OBSTACLES:
#                 # Handle game functions
#                 update_car(car, keys_pressed)
#                 # Update gamestate
#                 gamestate.update(car, keys_pressed)

#             # Rendering
#             SCREEN.fill((255, 255, 255))
#             SCREEN.blit(track.image, track.rect)
#             SCREEN.blit(goal.image, goal.rect)
#             car.draw(SCREEN)
#             # Create surface for controls display
#             controls_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
#             render_controls(controls_surface, keys_pressed)
#             SCREEN.blit(controls_surface, (900, 0))
#             if current_game_status == GameStatus.PLACE_OBSTACLES:
#                 mouse_loc = pygame.mouse.get_pos()
#                 pygame.draw.circle(SCREEN, CONSTANTS.YELLOW,
#                                    mouse_loc, CONSTANTS.OBSTACLE_DEFAULT_RADIUS)
#             else:
#                 # Draw rays on screen
#                 gamestate.draw_rays(SCREEN)

#             # Collision Detection
#             if current_game_status == GameStatus.PLACE_OBSTACLES:
#                 # No collision detection during placing of obstacles
#                 pass
#             elif (pygame.sprite.spritecollide(car, obstacles_group, False, collided=pygame.sprite.collide_mask)):
#                 # returned list is not empty
#                 current_game_status = GameStatus.GAME_OVER
#                 gamestate.set_obstacle_hit(True)
#                 gamestate.set_finish_line_reached(False)
#             elif (pygame.sprite.spritecollide(car, goal_group, False, collided=pygame.sprite.collide_mask)):
#                 current_game_status = GameStatus.WIN
#                 gamestate.set_obstacle_hit(False)
#                 gamestate.set_finish_line_reached(True)
#             else:
#                 current_game_status = GameStatus.ONGOING
#                 gamestate.set_obstacle_hit(False)
#                 gamestate.set_finish_line_reached(False)

#             # Save gamestate to a numpy array
#             if current_game_status == GameStatus.ONGOING and CONSTANTS.SAVE_GAMESTATE_TO_FILE:
#                 if gamestates_np is None:
#                     gamestates_np = [gamestate.to_numpy()]
#                 else:
#                     gamestates_np = np.append(
#                         gamestates_np, [gamestate.to_numpy()], axis=0)
#                 if current_game_status == GameStatus.GAME_OVER or current_game_status == GameStatus.WIN:
#                     save_gamestates_to_csv(gamestates_np, num)
#                     gamestates_np = None

#             if (current_game_status == GameStatus.GAME_OVER):
#                 print_text(SCREEN, 'GAME OVER', pygame.font.Font(None, 128))
#             elif (current_game_status == GameStatus.WIN):
#                 print_text(SCREEN, 'GOAL', pygame.font.Font(None, 128))

#             # Update Screen
#             pygame.display.flip()

#         clock.tick(CONSTANTS.FPS)

#     pygame.quit()
#     sys.exit()


# if __name__ == '__main__':
#     main()
