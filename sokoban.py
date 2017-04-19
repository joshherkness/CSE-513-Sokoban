import sokoenginepy as se
from services.state_helper import StateHelper

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

def main():
    sokoban = Sokoban('levels/level_0.txt')
    print('reward:', StateHelper.take_action(sokoban.mover, se.Direction.UP))
    print(sokoban.board)
    
main()