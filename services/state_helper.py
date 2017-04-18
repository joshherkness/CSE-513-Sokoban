
import sokoenginepy as se

class StateHelper(object):
    '''Helper for state'''

    @staticmethod
    def take_action(mover, direction):
        '''Takes an action, returning a reward'''
        board = mover.board
        state = se.HashedBoardState(board)
        pusher_id = mover.selected_pusher
        pusher_position = state.pusher_position(pusher_id)
        neighbor_board_cells = StateHelper.near_far_cells(board, pusher_position, direction)
        n_0 = neighbor_board_cells['near']
        n_1 = neighbor_board_cells['far']

        # if ():
        #     # unrecoverable
        # elif ():
        #     # Box would be pushed
        # elif ():
        #     #

        try:
            mover.move(direction)
        except se.IllegalMoveError:
            print("IllegalMoveError risen!")

    @staticmethod
    def near_far_cells(board, position, direction):
        '''
        returns the nearest two cells in the direction at the specified position.
        '''
        near, far = StateHelper.near_far_positions(board, position, direction)
        near_cell = board.__getitem__(near) if near is not None else None
        far_cell = board.__getitem__(far) if far is not None else None
        return near, far, near_cell, far_cell

    @staticmethod
    def near_far_positions(board, position, direction):
        '''
        returns the positions of the nearest two cells in the direction at the 
        specified position.
        '''
        near = board.neighbor(position, direction)
        far = board.neighbor(near, direction)
        return near, far

    @staticmethod
    def neighbor_cells(board, position):
        '''
        returns the imediate neigbor cells of the specified position.
        '''
        up, down, left, right = StateHelper.neighbor_positions(board, position)
        up_cell = board.__getitem__(up) if up is not None else None
        down_cell = board.__getitem__(down) if down is not None else None
        left_cell = board.__getitem__(left) if left is not None else None
        right_cell = board.__getitem__(right) if right is not None else None
        return up_cell, down_cell, left_cell, right_cell

    @staticmethod
    def neighbor_positions(board, position):
        '''
        returns the positions of the imediate neigbor cells at the specified position.
        '''
        up = board.neighbor(position, se.Direction.UP)
        down = board.neighbor(position, se.Direction.DOWN)
        left = board.neighbor(position, se.Direction.LEFT)
        right = board.neighbor(position, se.Direction.RIGHT)
        return up, down, left, right