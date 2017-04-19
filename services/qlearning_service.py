import sokoenginepy as se
import random
import math
import os
import time
from services.state_helper import StateHelper

MAX_MOVES = 50

class QLearning(object):
    '''Creates a sokoban instance and initializes it with a level'''

    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9):
        '''Creates a sokoban instance and initializes it with a level'''
        self.q_values = {}
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def run(self, board, episodes):
        '''Creates a sokoban instance and initializes it with a level'''
        mover = se.Mover(board)
        self.q_values.clear()
        for e in range(episodes):
            self.run_episode(mover, e)
            mover = se.Mover(mover.initial_board)
        return self.q_values

    def run_episode(self, mover, episode):
        '''Creates a sokoban instance and initializes it with a level'''
        moves = 0
        while not StateHelper.is_terminal(mover.board) and moves < MAX_MOVES:
            moves = moves + 1
            state = str(mover.board)
            action = self.maximize_action(mover.board)
            reward = StateHelper.take_action(mover, action)
            new_q = (self.get_q(state, action) 
                + self.learning_rate * (reward + self.discount_factor * self.maximize_q(mover.board) - self.get_q(state, action)))
            self.q_values[state, action] = new_q

            # Print the board
            os.system('clear')
            print(action, reward, '\n')
            print(mover.board)
            #time.sleep(0.15)

    def maximize_q(self, board):
        '''Creates a sokoban instance and initializes it with a level'''
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