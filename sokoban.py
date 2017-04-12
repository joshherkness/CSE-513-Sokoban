
import sokoenginepy as se
from services.state_helper import StateHelper

ALL_DIRECTIONS = [se.Direction.RIGHT, se.Direction.DOWN,
                  se.Direction.LEFT, se.Direction.UP]

class Sokoban(object):

    '''Sokoban'''

    def __init__(self):
        self.board = self.load_board('levels/level_0.txt')
        self.mover = se.Mover(self.board)
        self.validate_board()
        return

    def load_board(self, level_file):
        '''Loads a board'''

        with open(level_file, 'r') as level:
            board = se.SokobanBoard(board_str=''.join(level.readlines()))
        return board

    def validate_board(self):
        state = se.HashedBoardState(self.board)
        stack = set(state.goals_positions.values())
        visited = set()
        while len(stack) > 0:
            position = stack.pop()
            visited.add(position)
            for direction in ALL_DIRECTIONS:
                (near, far, near_cell, far_cell) = StateHelper.get_neighbor_cells(self.board, position, direction)
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
    sokoban = Sokoban()
    #print(set(sokoban.board._graph.reachables(1)))
    #StateHelper.take_action(sokoban.mover, se.Direction.RIGHT)
    #print(sokoban.board)
    

main()