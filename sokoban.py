
import sokoenginepy as se
from services.state_helper import StateHelper

class Sokoban(object):

    '''Sokoban'''

    def __init__(self):
        self.board = self.load_board('levels/level_0.txt')
        self.mover = se.Mover(self.board)
        return

    def load_board(self, level_file):
        '''Loads a board'''

        with open(level_file, 'r') as level:
            board = se.SokobanBoard(board_str=''.join(level.readlines()))
        return board

def main():
    sokoban = Sokoban()
    print(sokoban.board)
    StateHelper.take_action(sokoban.mover, se.Direction.DOWN)
    print(sokoban.board)
    

main()