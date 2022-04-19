import sys
import pygame
import torch
from pygame.locals import (
    KEYDOWN,
    QUIT,
    K_ESCAPE,
)
from random import choice
from typing import List
from itertools import count
from src import constants as CONSTANTS
from src.enums import GameStatus
from src.env_creator import EnvironmentCreator
from src.obstacle import Obstacle
from src.commonUtils import print_text
from src.ai.agent import Agent
from src.ai.agent import DEVICE


class GameTrain:
    def __init__(self):
        self.creator = EnvironmentCreator(
            True, has_goal=False, use_user_data_for_rewards=True)
        self.agent = Agent()
        self.obstacles: List[Obstacle] = []
        self.game_status = GameStatus.ONGOING
        self.clock = pygame.time.Clock()

    def get_game_screen(self):
        screen = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
        screen.fill((255, 255, 255))
        self.screen = screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game_status = GameStatus.ESC

            elif event.type == QUIT:
                self.game_status = GameStatus.QUIT

    def place_obstacles_loop(self):
        # TODO: place obstacles from file
        pass

    def game_loop(self):
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
        ])

        num_episodes = CONSTANTS.NUM_EPISODES
        for i_episode in range(num_episodes):
            if self.game_status != GameStatus.ONGOING:
                break

            # Initialize the environment and state
            track_num = choice([0, 1, 2])
            env = self.creator.create_environment(track_num)
            env.reset()
            state = torch.from_numpy(env.observation()).unsqueeze(0).float()

            print('Starting episode no.:', i_episode)
            print('Explore probability:', self.agent.epsilon(False))

            for t in count():
                self.handle_events()
                if self.game_status != GameStatus.ONGOING:
                    break

                # Select and perform an action
                action = self.agent.select_action(state)
                next_state, reward, done, info = env.step(action.item())
                reward = torch.tensor([reward], device=DEVICE).float()
                next_state = torch.from_numpy(next_state).unsqueeze(0).float()
                done = torch.tensor([done], dtype=torch.bool)

                # Store the transition in memory
                self.agent.memory.push(state, action, next_state, reward, done)

                # Move to the next state
                state = next_state

                # Perform one step of the optimization (on the policy network)
                self.agent.optimize_model()

                self.screen.fill((255, 255, 255))
                env.render(self.screen, True)
                pygame.display.flip()

                if done:
                    break
                elif int(t) >= CONSTANTS.MAX_TIMESTEPS_PER_EPISODE:
                    break

            # Update the target network, copying all weights and biases in DQN
            if i_episode % CONSTANTS.TARGET_UPDATE == 0:
                self.agent.update_target_net_weights()

        print_text(self.screen, 'TRAINING COMPLETE',
                   pygame.font.Font(None, 128))

        if self.game_status not in [GameStatus.ESC, GameStatus.QUIT]:
            self.game_status = GameStatus.TRAIN_COMPLETE

    def game_end_loop(self):
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
        ])

        if CONSTANTS.SAVE_TRAINED_MODEL_TO_FILE:
            self.agent.save_weights(CONSTANTS.TRAINED_MODEL_SAVE_FILENAME)

        while self.game_status == GameStatus.TRAIN_COMPLETE:
            self.handle_events()
            self.clock.tick(CONSTANTS.FPS)

        if self.game_status == GameStatus.QUIT:
            pygame.quit()
            sys.exit()

    def start(self):
        self.get_game_screen()
        self.place_obstacles_loop()
        self.game_loop()
        self.game_end_loop()
