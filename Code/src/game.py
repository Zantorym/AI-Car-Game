import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
    K_ESCAPE,
)
from typing import List
from src.controls import GameControls
from src import constants as CONSTANTS
from src.enums import CarStartPosType, GameStatus, TrackNum
from src.environment import Environment
from src.obstacle import Obstacle
from src.game_display_utils import render_controls
from src.commonUtils import print_text


class Game:
    def __init__(self, track_num: TrackNum):
        self.environment = Environment(track_num,
                                       CarStartPosType.TRACK_DEFAULTS)
        self.obstacles: List[Obstacle] = []
        self.clock = pygame.time.Clock()
        

    def get_game_screen(self):
        # pygame.init()
        # pygame.font.init()
        pygame.display.set_caption("Crazy Driver")
        screen = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
        screen.fill((255, 255, 255))
        return screen

    def game_loop(self):
        SCREEN = self.get_game_screen()
        current_game_status = GameStatus.PLACE_OBSTACLES

        if (CONSTANTS.SAVE_GAMESTATE_TO_FILE):
            gamestates_np = None

        self.environment.reset()
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

                # Checking user event
                keys_pressed = pygame.key.get_pressed()

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
                        self.environment.place_obstacle(obstacle)
                        self.obstacles.append(obstacle)
                        if len(self.obstacles) == CONSTANTS.MAX_OBSTACLES_PER_TRACK:
                            current_game_status = GameStatus.ONGOING

                if current_game_status != GameStatus.PLACE_OBSTACLES:
                    action = GameControls.keys_to_actions(keys_pressed)
                    self.environment.next(action)

                # Rendering
                SCREEN.fill((255, 255, 255))
                self.environment.render(SCREEN, True)
                
                # Create surface for controls display
                controls_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
                render_controls(controls_surface, keys_pressed)
                SCREEN.blit(controls_surface, (900, 0))
                if current_game_status == GameStatus.PLACE_OBSTACLES:
                    mouse_loc = pygame.mouse.get_pos()
                    pygame.draw.circle(SCREEN, CONSTANTS.YELLOW,
                                       mouse_loc, CONSTANTS.OBSTACLE_DEFAULT_RADIUS)

                # Collision Detection
                if current_game_status == GameStatus.PLACE_OBSTACLES:
                    # No collision detection during placing of obstacles
                    pass
                elif self.environment.game_over:
                    # returned list is not empty
                    current_game_status = GameStatus.GAME_OVER
                elif self.environment.win:
                    current_game_status = GameStatus.WIN
                else:
                    current_game_status = GameStatus.ONGOING

                # # Save gamestate to a numpy array
                # if current_game_status == GameStatus.ONGOING and CONSTANTS.SAVE_GAMESTATE_TO_FILE:
                #     if gamestates_np is None:
                #         gamestates_np = [gamestate.to_numpy()]
                #     else:
                #         gamestates_np = np.append(
                #             gamestates_np, [gamestate.to_numpy()], axis=0)
                #     if current_game_status == GameStatus.GAME_OVER or current_game_status == GameStatus.WIN:
                #         save_gamestates_to_csv(gamestates_np, num)
                #         gamestates_np = None

                if (current_game_status == GameStatus.GAME_OVER):
                    print_text(SCREEN, 'GAME OVER',
                               pygame.font.Font(None, 128))
                elif (current_game_status == GameStatus.WIN):
                    print_text(SCREEN, 'GOAL', pygame.font.Font(None, 128))

                # Update Screen
                pygame.display.flip()

            self.clock.tick(CONSTANTS.FPS)


# if __name__ == '__main__':
#     main()
