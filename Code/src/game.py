import numpy
import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
    K_ESCAPE,
)
from typing import List
from src.controls import GameControls
from src import constants as CONSTANTS
from src.enums import GameStatus, TrackNum
from src.env_creator import EnvironmentCreator
from src.environment import Environment
from src.obstacle import Obstacle
from src.game_display_utils import render_controls
from src.commonUtils import print_text, save_gamestates_to_csv


class Game:
    def __init__(self, track_num: TrackNum):
        self.environment: Environment = EnvironmentCreator().create_environment(track_num)
        self.obstacles: List[Obstacle] = []
        self.game_status = GameStatus.PLACE_OBSTACLES
        self.clock = pygame.time.Clock()

    def get_game_screen(self):
        screen = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
        screen.fill((255, 255, 255))
        self.screen = screen

    def prepare_environment(self):
        self.environment.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game_status = GameStatus.ESC

            elif event.type == QUIT:
                self.game_status = GameStatus.QUIT

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if CONSTANTS.PRINT_MOUSE_CLICK_LOCATION:
                    print((mouse_x, mouse_y))
                if self.game_status == GameStatus.PLACE_OBSTACLES:
                    obstacle = Obstacle((mouse_x, mouse_y))
                    self.environment.place_obstacle(obstacle)
                    self.obstacles.append(obstacle)
                    if len(self.obstacles) == CONSTANTS.MAX_OBSTACLES_PER_TRACK:
                        self.game_status = GameStatus.GAME_START

    def render(self, draw_rays=False):
        self.screen.fill((255, 255, 255))
        self.environment.render(self.screen, draw_rays)

    def place_obstacles_loop(self):
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.MOUSEBUTTONDOWN,
            pygame.KEYDOWN,
        ])

        while self.game_status == GameStatus.PLACE_OBSTACLES:
            self.handle_events()

            self.render()
            mouse_loc = pygame.mouse.get_pos()
            pygame.draw.circle(self.screen, CONSTANTS.YELLOW,
                               mouse_loc, CONSTANTS.OBSTACLE_DEFAULT_RADIUS)
            pygame.display.flip()

            self.clock.tick(CONSTANTS.FPS)

    def game_loop(self):
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
        ])

        if (CONSTANTS.SAVE_GAMESTATE_TO_FILE):
            self.gamestates_np = None

        while self.game_status in [GameStatus.GAME_START, GameStatus.ONGOING]:
            self.handle_events()
            keys_pressed = pygame.key.get_pressed()

            action = GameControls.keys_to_actions(keys_pressed)
            # Car has been controlled, update status to ongoing
            if self.game_status == GameStatus.GAME_START and action != 0:
                self.game_status = GameStatus.ONGOING
            self.environment.next(action)

            # Rendering
            self.render(True)

            # Create surface for controls display
            controls_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
            render_controls(controls_surface, keys_pressed)
            self.screen.blit(controls_surface, (900, 0))

            # Collision Detection
            if self.environment.game_over:
                # returned list is not empty
                self.game_status = GameStatus.GAME_OVER
            elif self.environment.win:
                self.game_status = GameStatus.WIN

            # Save gamestate to a numpy array
            if self.game_status in [
                GameStatus.ONGOING,
                GameStatus.GAME_OVER,
                GameStatus.WIN,
            ] and CONSTANTS.SAVE_GAMESTATE_TO_FILE:
                if self.gamestates_np is None:
                    self.gamestates_np = [
                        self.environment.gamestate_as_np(action)]
                else:
                    self.gamestates_np = numpy.append(
                        self.gamestates_np, [self.environment.gamestate_as_np(action)], axis=0)

            if (self.game_status == GameStatus.GAME_OVER):
                print_text(self.screen, 'GAME OVER',
                           pygame.font.Font(None, 128))
            elif (self.game_status == GameStatus.WIN):
                print_text(self.screen, 'GOAL', pygame.font.Font(None, 128))

            # Update Screen
            pygame.display.flip()

            self.clock.tick(CONSTANTS.FPS)

    def game_end_loop(self):
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
        ])

        save_gamestates_to_csv(self.gamestates_np)
        self.gamestates_np = None

        while self.game_status in [GameStatus.GAME_OVER, GameStatus.WIN]:
            self.handle_events()
            self.clock.tick(CONSTANTS.FPS)

    def start(self):
        self.get_game_screen()
        self.prepare_environment()
        self.place_obstacles_loop()
        self.game_loop()
        self.game_end_loop()
