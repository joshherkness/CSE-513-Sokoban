import sokoenginepy as se
import os
import time
import numpy
import matplotlib.pyplot as plt
from services.state_helper import StateHelper
from services.qlearning_service import Solver

DIRECTIONS = [se.Direction.RIGHT, se.Direction.DOWN, se.Direction.LEFT, se.Direction.UP]

class Sokoban(object):

    def __init__(self, level_file):
        '''Creates a sokoban instance and initializes it with a level'''

        self.board = self.load_board(level_file)
        self.mover = se.Mover(self.board)
        self.identify_simple_deadlocks()

    def load_board(self, level_file):
        '''Loads a level from a file into the board instance'''

        with open(level_file, 'r') as level:
            board = se.SokobanBoard(board_str=''.join(level.readlines()))
        return board

    def identify_simple_deadlocks(self):
        '''Identifies and marks simple deadlock spaces'''

        state = se.HashedBoardState(self.board)
        stack = set(state.goals_positions.values())
        visited = set()
        while len(stack) > 0:
            position = stack.pop()
            visited.add(position)
            for direction in DIRECTIONS:
                (near, far, near_cell, far_cell) = StateHelper.near_far_cells(self.board, position, direction)
                if not near_cell.is_wall and not far_cell.is_wall:
                    if not visited.__contains__(near):
                        stack.add(near)
        all_positions = set(self.board._graph.reachables(10, is_obstacle_callable=lambda x: False))
        deadlocked_positions = all_positions.difference(visited)
        # Apply deadlocks
        for x in deadlocked_positions:
            board_cell = self.board.__getitem__(x)
            board_cell.is_deadlock = True

data = {'episodes': [], 'moves': [], 'average_rewards': [], 'solved': [], 'time': []}
def main():
    sokoban = Sokoban('levels/level_5.txt')
    solver = Solver(DIRECTIONS)

    solver.run(sokoban.board, 450, action_callback=action_callback, episode_callback=episode_callback, run_callback=run_callback)

    f, axarr = plt.subplots(4, sharex=True)
    f.tight_layout()
    f.subplots_adjust(top=0.88)
    axarr[0].plot(data['episodes'], data['moves'], 'r')
    axarr[0].set_ylabel('Number of moves')
    axarr[1].plot(data['episodes'], data['average_rewards'], 'b')
    axarr[1].set_ylabel('Average rewards')
    axarr[2].bar(data['episodes'], list(map(lambda b: 1 if b else 0, data['solved'])), color='g', align="center", width=1)
    axarr[2].set_ylabel('Solved')
    axarr[3].plot(data['episodes'], data['time'], 'm')
    axarr[3].set_ylabel('Seconds')    
    axarr[3].set_xlabel('Episode')

    plt.show()

def run_callback(q_values, board):
    '''Called after solver is run'''
    return None

def episode_callback(episode, moves, rewards, solved, time, board):
    data['episodes'].append(episode)
    data['moves'].append(moves)
    data['average_rewards'].append(numpy.average(rewards))
    data['solved'].append(solved)
    data['time'].append(time)

def action_callback(episode, action, move, reward, board):
    #return None # un comment this to render
    render_board(episode, action, move, reward, board)

def render_board(episode, action, move, reward, board):
    # Render the board
    #os.system('clear')
    print('Episode: ', episode)
    print('Move: ', move)
    print('Action: ', action)
    print('Reward: ', reward)
    print(board)
    # if episode > 380:
    #     time.sleep(0.1)
    # else:
    #     time.sleep(0.04)
    
main()