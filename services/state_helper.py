
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
        neighbor_board_cells = StateHelper.get_neighbor_board_cells(board,
                                                                    pusher_position,
                                                                    direction)
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
    def get_neighbor_cells(board, position, direction):
        '''
        retrieves the board cells in the nearest two locations in a direction
        of a position.
        '''

        near, far = StateHelper.get_neighbor_positions(board, position, direction)
        try:
            near_cell = board.__getitem__(near)
        except:
            near_cell = None

        try:
            far_cell = board.__getitem__(far)
        except:
            far_cell = None

        return near, far, near_cell, far_cell

    @staticmethod
    def get_neighbor_positions(board, position, direction):
        '''
        retrieves the board cells in the nearest two locations in a direction
        of a position.
        '''

        near = board.neighbor(position, direction)
        far = board.neighbor(near, direction)
        return near, far

