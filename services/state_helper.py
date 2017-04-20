import sokoenginepy as se
from functools import reduce

class StateHelper(object):
    '''Helper for state'''

    @staticmethod
    def take_action(mover, direction):
        '''Takes an action, returning a reward'''
        board = mover.board
        state = mover.state
        pusher_id = mover.selected_pusher
        pusher_position = state.pusher_position(pusher_id)
        near, far, near_cell, far_cell = StateHelper.near_far_cells(board, pusher_position, direction)

        # Determine the reward before moving
        reward = 0
        if near_cell.has_box and (far_cell.is_wall or far_cell.has_box) :
            # Box pushed against wall or box
            reward = -1
        elif near_cell.has_box and near_cell.has_goal and far_cell.has_goal:
            reward = 0
        elif near_cell.has_box and near_cell.has_goal and far_cell.is_empty_floor:
            # Box pushed off goal
            reward = -1
        elif near_cell.has_box and far_cell.has_goal:
            # Box pushed on goal
            reward = 100
        elif near_cell.has_box and far_cell.is_empty_floor:
            # Box pushed 
            reward = 1

        # Take the action
        try:
            mover.move(direction)
        except:
            reward = -1
        pusher_position = state.pusher_position(pusher_id)
        near, far, near_cell, far_cell = StateHelper.near_far_cells(board, pusher_position, direction)

        # Determine the reward after moving
        if near_cell.has_box and near_cell.is_deadlock:
            reward = min(-1000, reward)
        elif near_cell.has_box and StateHelper.is_freeze_deadlock(board, near):
            reward = min(-250, reward)

        return reward

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

    @staticmethod
    def is_freeze_deadlock(board, position):
        '''returns a boolean indicating whether or not there is a freeze deadlock'''
        is_frozen, frozen_cells = StateHelper.is_freeze(board, position, [], [])
        all_on_goals = reduce(lambda x,y: x and y.has_goal, frozen_cells, True)
        return is_frozen and not all_on_goals

    @staticmethod
    def is_freeze(board, position, checked=[], frozen_cells=[]):
        '''returns a boolean indicating whether or not the block at that position is frozen 
        and a list of blocks in the freeze deadlock'''

        # Remember positions we have already checked to avoid circular checks
        checked.append(position)

        # Get the immediate neighbors at the position
        up, down, left, right = StateHelper.neighbor_positions(board, position)
        up_cell, down_cell, left_cell, right_cell = StateHelper.neighbor_cells(board, position)
        
        # Check if there is a vertical deadlock
        horizontal_deadlock = False
        if left_cell.is_wall or left in checked or right_cell.is_wall or right in checked:
            horizontal_deadlock = True
        elif left_cell.is_deadlock and right_cell.is_deadlock:
            horizontal_deadlock = True
        elif left_cell.has_box or right_cell.has_box:
            if left_cell.has_box:
                horizontal_deadlock = horizontal_deadlock or StateHelper.is_freeze(board, left, checked, frozen_cells) 
            if right_cell.has_box:
                horizontal_deadlock = horizontal_deadlock or StateHelper.is_freeze(board, right, checked, frozen_cells) 

        # Check if there is a horizontal deadlock
        vertical_deadlock = False
        if up_cell.is_wall or up in checked or down_cell.is_wall or down in checked:
            vertical_deadlock = True
        elif up_cell.is_deadlock and down_cell.is_deadlock:
            vertical_deadlock = True
        elif up_cell.has_box or down_cell.has_box:
            if up_cell.has_box:
                vertical_deadlock = vertical_deadlock or StateHelper.is_freeze(board, up, checked, frozen_cells) 
            if down_cell.has_box:
                vertical_deadlock = vertical_deadlock or StateHelper.is_freeze(board, down, checked, frozen_cells) 

        cell_is_frozen = vertical_deadlock and horizontal_deadlock

        if cell_is_frozen:
            frozen_cells.append(board.__getitem__(position))

        return cell_is_frozen, frozen_cells

    @staticmethod
    def is_terminal(board):
        '''returns a boolean indicating whether or not the board is terminal'''
        state = se.HashedBoardState(board)
        all_boxes_frozen = False
        any_box_in_simple_deadlock = False
        for box_id, box_pos in state.boxes_positions.items():
            all_boxes_frozen  = all_boxes_frozen or StateHelper.is_freeze_deadlock(board, box_pos)
            any_box_in_simple_deadlock = any_box_in_simple_deadlock or board.__getitem__(box_pos).is_deadlock
        return state.is_solved() or all_boxes_frozen or any_box_in_simple_deadlock