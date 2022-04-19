import math
import random
import torch
from torch import optim
import os
from src import constants as CONSTANTS
from src.controls import GameControls
from src.ai.device import DEVICE
from src.ai.dqn import DQN
from src.ai.replay_memory import ReplayMemory
from src.ai.transition import Transition


class Agent:
    _input_size = 15

    def __init__(self):
        '''
        If there is an existing model load weights from previous policy in the new policy
        '''
        self.policy_net = DQN(Agent._input_size,
                              GameControls.action_space_size)
        if os.path.isfile(CONSTANTS.MODEL_PATH):
            self.load_saved_model()
        # self.policy_net = self.policy_net.float()
        self.target_net = DQN(Agent._input_size,
                              GameControls.action_space_size)
        # self.target_net = self.target_net.float()

        self.policy_net.to(DEVICE)
        self.target_net.to(DEVICE)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters())
        self.memory = ReplayMemory(CONSTANTS.REPLAY_MEMORY_SIZE)

        self.steps_done = 0

    def epsilon(self, update_steps: bool = True):
        eps = CONSTANTS.EPS_END + (CONSTANTS.EPS_START - CONSTANTS.EPS_END) * \
            math.exp(-1. * self.steps_done / CONSTANTS.EPS_DECAY)
        if update_steps:
            self.steps_done += 1
        return eps

    def select_action(self, state):
        sample = random.random()
        eps_threshold = self.epsilon()
        if sample > eps_threshold:
            with torch.no_grad():
                actions = self.policy_net(state)
                action = actions.max(1)[1].view(1, 1)
                return action
        else:
            action = torch.tensor([[random.randrange(GameControls.action_space_size)]],
                                  device=DEVICE,
                                  dtype=torch.long)
            return action

    def update_target_net_weights(self):
        '''
        Get called after every 10 episodes
        '''
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.save_model()
        self.save_model_params()

    def optimize_model(self):
        batch_size = CONSTANTS.BATCH_SIZE
        if len(self.memory) < batch_size:
            return
        transitions = self.memory.sample(batch_size)

        batch = Transition(*zip(*transitions))

        # TODO: change lamda to actual logic to determine if end state
        # non_final_mask = torch.tensor(tuple(map(lambda s: True,
        #                                         batch.next_state)), device=DEVICE, dtype=torch.bool)
        # non_final_next_states = torch.cat([s for s in batch.next_state
        #                                    if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        done_batch = torch.cat(batch.done)
        next_batch = torch.cat(batch.next_state)
        mask = ~done_batch
        non_final_next_states = next_batch[mask]

        state_action_values = self.policy_net(
            state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(batch_size, device=DEVICE)
        next_state_values[mask] = self.target_net(
            non_final_next_states).max(1)[0].detach()

        expected_state_action_values = (
                                               next_state_values * CONSTANTS.GAMMA) + reward_batch

        criterion = torch.nn.SmoothL1Loss()
        loss = criterion(state_action_values,
                         expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def save_model(self):
        print('Saving model')
        torch.save(self.target_net, CONSTANTS.MODEL_PATH)

    def save_model_params(self):
        print('Saving model params')
        torch.save(self.policy_net.state_dict(), CONSTANTS.MODEL_PARAMS)

    def load_saved_model(self):
        print('Loading model')
        return torch.load(CONSTANTS.MODEL_PATH)

    def load_saved_model_params(self):
        print('Loading model params')
        self.policy_net.load_state_dict(torch.load(CONSTANTS.MODEL_PARAMS))
