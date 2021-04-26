import constants
import placements

dictsidetomove = {True:'white',False:'black'}

class AutomateGame():
    def __init__(self):
        self.board = placements.init_full_board()
        self.white_pts = constants.W_TOTAL
        self.black_pts = constants.W_TOTAL
        self.turn = True

    def legal_moves(board, player):
        pass

    def print_board(self):
        placements.print_full_board(self.board)

def main():
    game = AutomateGame()
    game.print_board()

if __name__ == "__main__":
    main()