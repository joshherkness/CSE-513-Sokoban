import sokoenginepy as se
import os
import sys, getopt
import time
import numpy
import pprint
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
def main(argv):
    
    # Default Values
    learning_rate = 0.2
    discount_factor = 0.8
    level_file = 'levels/level_0.txt'
    max_actions = -1
    episodes = 450
    should_render_level = True
    should_plot_data = False

    # User specified values
    try:
      opts, args = getopt.getopt(argv,"hl:d:f:a:e:r:p",["learning-rate=", 
        "discount-factor=", 
        "level-file=", 
        "max-actions=", 
        "episodes=", 
        "render-level=", 
        "plot-data="])
    except getopt.GetoptError:
        print('sokoban.py -l <learning rate> -d <discount factor> -f <level file> -a <max actions> -e <episodes> -r <render level> -p <plot_data>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", '--help'):
            print('sokoban.py -l <learning rate> -d <discount factor> -f <level file> -a <max actions> -e <episodes> -r <render level> -p <plot_data>')
            sys.exit()
        elif opt in ("-l", "--learning-rate"):
            learning_rate = eval(arg)
        elif opt in ("-d", "--discount-factor"):
            discount_factor = eval(arg)
        elif opt in ("-f", "--level-file"):
            level_file = arg
        elif opt in ("-a", "--max-actions"):
            max_actions = eval(arg)
        elif opt in ("-e", "--episodes"):
            episodes = int(arg)
        elif opt in ("-r", "--render-level"):
            should_render_level = True if arg in ['True', 'true', 't', 'y', 'yes'] else False
        elif opt in ("-p", "--plot-data"):
            should_plot_data = True if arg in ['True', 'true', 't', 'y', 'yes'] else False
    
    # Load the level
    sokoban = Sokoban(level_file)
    solver = Solver(actions=DIRECTIONS, learning_rate=learning_rate, discount_factor=discount_factor, max_actions=max_actions)

    # Create action callback for when any action is completed
    def action_callback(episode, action, move, reward, board):
        if should_render_level:
            render_board(episode, action, move, reward, board)
        else:
            return None

    # Run solver
    solver.run(sokoban.board, episodes, action_callback=action_callback, episode_callback=episode_callback, run_callback=run_callback)

    # Plot data
    if should_plot_data:
        plot_data(data)

def run_callback(q_values, board):
    '''Called after solver is run'''
    print('COMPLETED')
    print('The program was', 'not' if not data['solved'][-1] else 'indeed', 'able to solve the puzzle')
    print(board)
    #print('Here are the Q values:')
    #pp = pprint.PrettyPrinter(depth=6)
    #pp.pprint(q_values)

def episode_callback(episode, moves, rewards, solved, time, board):
    data['episodes'].append(episode)
    data['moves'].append(moves)
    data['average_rewards'].append(numpy.average(rewards))
    data['solved'].append(solved)
    data['time'].append(time)

def render_board(episode, action, move, reward, board):
    # Render the board
    os.system('clear')
    print('Episode: ', episode)
    print('Move: ', move)
    print('Action: ', action)
    print('Reward: ', reward)
    print(board)
    time.sleep(0.1)
    
def plot_data(data):
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
    
if __name__ =='__main__':
    main(sys.argv[1:])