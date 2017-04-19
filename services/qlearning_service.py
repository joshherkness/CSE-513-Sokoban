import sokoenginepy as se
import random
import math
from state_helper import StateHelper

class QLearning(object):
    '''Creates a sokoban instance and initializes it with a level'''

    def __init__(self):
        '''Creates a sokoban instance and initializes it with a level'''
        self.q_values = {}

    def run_episode(self, board, actions):
        state = se.HashedBoardState(board)
        while not StateHelper.is_terminal(board):
            

    def maximize_q(self, board, actions):
        '''Creates a sokoban instance and initializes it with a level'''
        state = se.HashedBoardState(board)
        max_q = float('-inf')

        for action in actions:
            q = self.q_values[state, action]
            max_q = max(q, max_q)
        return max_q 
    
    def maximize_action(self, board, actions):
        '''Creates a sokoban instance and initializes it with a level'''
        state = se.HashedBoardState(board)
        max_q = float('-inf')
        max_actions = []

        for action in actions:
            q = self.q_values[state, action]
            if q > max_q:
                max_q = q
                max_actions = [action]
            elif q == max_q:
                max_actions.append(action)
        return self.random_action(actions)

    def random_action(self, actions):
        return random.choice(actions)

    
