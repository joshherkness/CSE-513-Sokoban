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

    def is_freeze_deadlock(self, position, checked=[]):
        '''returns a boolean indicating whether or not the block at that position is frozen'''
        # Remember positions we have already checked to avoid circular checks
        checked.append(position)

        # Get the immediate neighbors at the position
        up, down, left, right = StateHelper.neighbor_positions(self.board, position)
        up_cell, down_cell, left_cell, right_cell = StateHelper.neighbor_cells(self.board, position)
        
        # Check if there is a vertical deadlock
        vertical_deadlock = False
        if left_cell.is_wall or left in checked or right_cell.is_wall or right in checked:
            vertical_deadlock = True
        elif left_cell.is_deadlock and right_cell.is_deadlock:
            vertical_deadlock = True
        elif left_cell.has_box or right_cell.has_box:
            if left_cell.has_box:
                vertical_deadlock = vertical_deadlock or self.is_freeze_deadlock(left, checked) 
            if right_cell.has_box:
                vertical_deadlock = vertical_deadlock or self.is_freeze_deadlock(right, checked) 

        # Check if there is a horizontal deadlock
        horizontal_deadlock = False
        if up_cell.is_wall or up in checked or down_cell.is_wall or down in checked:
            horizontal_deadlock = True
        elif up_cell.is_deadlock and down_cell.is_deadlock:
            horizontal_deadlock = True
        elif up_cell.has_box or down_cell.has_box:
            if up_cell.has_box:
                horizontal_deadlock = horizontal_deadlock or self.is_freeze_deadlock(up, checked) 
            if down_cell.has_box:
                horizontal_deadlock = horizontal_deadlock or self.is_freeze_deadlock(down, checked) 

        return vertical_deadlock and horizontal_deadlock

def main():
    sokoban = Sokoban('levels/level_0.txt')
    print(sokoban.is_freeze_deadlock(20))
    #StateHelper.take_action(sokoban.mover, se.Direction.RIGHT)
    #print(sokoban.board)
    

main()