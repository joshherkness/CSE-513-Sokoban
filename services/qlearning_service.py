import sokoenginepy as se
import random
import math
import time
from services.state_helper import StateHelper

class Solver(object):
    '''Q learning solver for a sokoban puzzle.'''

    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, max_actions=-1):
        '''Iitializer for the solver'''
        self.q_values = {}
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.max_actions = max_actions

    def run(self, board, episodes,
        run_callback=lambda Q, b : None, 
        episode_callback=lambda e, m, R, s, t, b : None, 
        action_callback=lambda e, a, m, r, b: None):
        '''Runs a series of episodes using q learning'''
        mover = se.Mover(board)
        self.q_values.clear()
        for e in range(episodes):
            self.run_episode(mover, e, action_callback, episode_callback)
            mover = se.Mover(mover.initial_board)
        run_callback(self.q_values, mover.board)
        return self.q_values

    def run_episode(self, mover, episode, action_callback, episode_callback):
        '''Runs a single episode using q learning'''
        moves = 0
        rewards = []
        start_time = time.time()
        while not StateHelper.is_terminal(mover.board) and (moves < self.max_actions or self.max_actions == -1):
            moves = moves + 1
            state = str(mover.board)
            action = self.maximize_action(mover.board)
            reward = StateHelper.take_action(mover, action)
            rewards.append(reward)
            new_q = (self.get_q(state, action) 
                + self.learning_rate * (reward + self.discount_factor * self.maximize_q(mover.board) - self.get_q(state, action)))
            self.q_values[state, action] = new_q
            action_callback(episode, action, moves, reward, mover.board)
        end_time = time.time()
        episode_callback(episode, moves, rewards, mover.state.is_solved(), end_time - start_time, mover.board)

    def maximize_q(self, board):
        '''Calculates the maximum q value that can be reached from the current state in a single action'''
        state = str(board)
        max_q = float('-inf')

        for action in self.actions:
            q = self.get_q(state, action)
            max_q = max(q, max_q)
        return max_q 
    
    def maximize_action(self, board):
        '''Creates a sokoban instance and initializes it with a level'''
        state = str(board)
        max_q = float('-inf')
        max_actions = []

        for action in self.actions:
            q = self.get_q(state, action)
            if q > max_q:
                max_q = q
                max_actions = [action]
            elif q == max_q:
                max_actions.append(action)
        return self.random_action(max_actions)

    def get_q(self, state, action):
        if (state, action) in self.q_values.keys():
            return self.q_values[state, action]
        return 0

    def random_action(self, actions):
        '''Creates a sokoban instance and initializes it with a level'''
        return random.choice(actions)