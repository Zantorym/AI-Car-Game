import pygame
import torch
from itertools import count
from src import constants as CONSTANTS
from src.env_creator import EnvironmentCreator
from src.ai.device import DEVICE
from src.ai.agent import Agent


pygame.init()
pygame.font.init()
pygame.display.set_caption("Crazy Driver")
screen = pygame.display.set_mode((CONSTANTS.WIDTH, CONSTANTS.HEIGHT))
screen.fill((255, 255, 255))

creator = EnvironmentCreator(True)
agent = Agent()
clock = pygame.time.Clock()

num_episodes = CONSTANTS.NUM_EPISODES
for i_episode in range(num_episodes):

    # Initialize the environment and state
    env = creator.create_environment(1)
    env.reset()
    state = torch.from_numpy(env.observation()).unsqueeze(0).float()

    print('Starting episode no.:', i_episode)

    for t in range(CONSTANTS.MAX_TIMESTEPS_PER_EPISODE):
        # Select and perform an action
        action = agent.select_action(state)
        next_state, reward, done, info = env.step(action.item())
        reward = torch.tensor([reward], device=DEVICE).float()
        next_state = torch.from_numpy(next_state).unsqueeze(0).float()
        done = torch.tensor([done], dtype=torch.bool)

        # Store the transition in memory
        agent.memory.push(state, action, next_state, reward, done)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        agent.optimize_model()

        screen.fill((255, 255, 255))
        env.render(screen, True)
        pygame.display.flip()
        # clock.tick(CONSTANTS.FPS)
        
        if done:
            break

    # Update the target network, copying all weights and biases in DQN
    if i_episode % CONSTANTS.TARGET_UPDATE == 0:
        agent.update_target_net_weights()

print('Complete')
