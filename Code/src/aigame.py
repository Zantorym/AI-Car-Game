from src.game import Game
import sys
import pygame
import torch
from src import constants as CONSTANTS
from src.enums import GameStatus, TrackNum
from src.ai.agent import Agent
from src.commonUtils import print_text, save_gamestates_to_csv

class AIGame(Game):
    def __init__(self, track_num: TrackNum):
        Game.__init__(self, track_num)
        self.agent = Agent()
        self.agent.load_weights(CONSTANTS.TRAINED_MODEL_SAVE_FILENAME)

    def game_loop(self):
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
        ])

        if (CONSTANTS.SAVE_GAMESTATE_TO_FILE):
            self.gamestates_np = None

        while self.game_status in [GameStatus.GAME_START, GameStatus.ONGOING]:
            self.handle_events()

            current_state = torch.from_numpy(self.environment.observation()).unsqueeze(0).float()
            action = self.agent.predict_action(current_state)

            # Car has been controlled, update status to ongoing
            if self.game_status == GameStatus.GAME_START and action != 0:
                self.game_status = GameStatus.ONGOING
            self.environment.next(action)

            # Rendering
            self.render(True)

            # Collision Detection
            if self.environment.game_over:
                # returned list is not empty
                self.game_status = GameStatus.GAME_OVER
            elif self.environment.win:
                self.game_status = GameStatus.WIN

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

        while self.game_status in [GameStatus.GAME_OVER, GameStatus.WIN]:
            self.handle_events()
            self.clock.tick(CONSTANTS.FPS)

        if self.game_status == GameStatus.QUIT:
            pygame.quit()
            sys.exit()

    def start(self):
        self.get_game_screen()
        self.prepare_environment()
        self.place_obstacles_loop()
        self.game_loop()
        self.game_end_loop()