import chess
import chess.engine
import constants
import placements
import random

class AutomateGame():
    def __init__(self):
        self.board = placements.init_full_board() # Board
        self.white_pts = constants.W_TOTAL # Total points left with white
        self.black_pts = constants.W_TOTAL # Total points left with black
        self.turn = True # Whose turn is it - 'True' for white 'False' for black
        self.white_king = False # Is white king already placed
        self.black_king = False # Is black king already placed
        self.move_count = 0 # Keep track of number of moves played

    def legal_moves(self, board, player):
        pass
    
    # A move is defined by piece and square
    def move(self, piece, square):
        # Check for feasibility - 1. Check for turn, 2. Check for king, 3. Check for points
        if piece.isupper():
            if self.turn == False:
                print("Not white's turn")
                return False
            if self.move_count < constants.MIN_PAWNS and piece != 'P':
                print("The first few moves has to be pawns")
                return False
            if self.white_king:
                print("King has to be placed at the end")
                return False
            if self.white_pts - constants.PIECE_VALUES[piece] < 0:
                print("Can't spend more than available points")
                return False
        else:
            if self.turn == True:
                print("Not black's turn")
                return False
            if self.move_count < constants.MIN_PAWNS and piece != 'p':
                print("The first few moves has to be pawns")
                return False
            if self.black_king:
                print("King has to be placed at the end")
                return False
            if self.black_pts - constants.PIECE_VALUES[piece] < 0:
                print("Can't spend more than available points")
                return False
        
        if placements.place_piece(self.board, piece, square):
            # Will return false if not placed in feasible ranks and if the square is already occupied
            # Set king placements if king is placed
            if piece == 'k':
                self.black_king = True
            elif piece  == 'K':
                self.white_king = True
            # Reduce the value from the total available points by the piece value
            if piece.isupper():
                self.white_pts -= constants.PIECE_VALUES[piece]
            else:
                self.black_pts -= constants.PIECE_VALUES[piece]
            self.turn = not self.turn
            self.move_count += 0.5
            return True
        print("Illegal Move")
        return False

    def print_board(self):
        placements.print_full_board(self.board)
    
    def print_game(self):
        print("Automate Game Object")
        print("Board ---")
        self.print_board()
        print("White's available points: ", self.white_pts)
        print("Black's available points: ", self.black_pts)

    def setup_random_game(self, white_preferred_combs = constants.COMBINATIONS, black_preferred_combs = constants.COMBINATIONS):
        # Setup a random initial game given the preferred combinations
        while True:
            # print("White's placements")
            comb = random.choice(white_preferred_combs)
            # print(comb)
            # print(placements.check_feasible_comb(*comb))
            white_mini_board = placements.generate_placement(*comb)

            # print("Black's placements")
            comb = random.choice(black_preferred_combs)
            # print(comb)
            # print(placements.check_feasible_comb(*comb))
            black_mini_board = placements.generate_placement(*comb)

            self.board = placements.generate_board(white_mini_board, black_mini_board)
            # placements.print_full_board(board)
            self.fen = placements.generate_fen(self.board)
            # print(fen)
            self.final_board = chess.Board(self.fen)
            if self.final_board.is_valid():
                break
        return self.final_board

def random_game():
    pondertime = 1.0
    maxmoves = 200
    dictsidetomove = {True:'white',False:'black'}
    notationdict = {True:'.', False:'...'}
    game = AutomateGame()
    board = game.setup_random_game()
    engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    print(info)
    print("Score:", info["score"])
    limit = chess.engine.Limit(time=1.0)
    result = engine.play(board, limit)
    print(result.move)
    while not board.is_game_over() and board.fullmove_number<=maxmoves:
        result = engine.play(board,chess.engine.Limit(time=pondertime))
        print(dictsidetomove[board.turn]+' played '+str(board.fullmove_number)+notationdict[board.turn]+str(board.san(result.move)))
        board.push(result.move)
    print(board)
    print('Final position FEN: ',board.fen())
    print('-----')
    engine.quit()

def main():
    # random_game()
    game = AutomateGame()
    success = game.move('P', 'a2')
    success = game.move('p', 'a7')
    success = game.move('P', 'a3')
    success = game.move('p', 'a6')
    success = game.move('P', 'b3')
    success = game.move('p', 'b6')
    success = game.move('P', 'b2')
    success = game.move('p', 'c6')
    success = game.move('P', 'c3')
    success = game.move('p', 'd7')
    success = game.move('P', 'h3')
    success = game.move('p', 'e6')
    success = game.move('N', 'a1')

    game.print_game()
    # game.print_board()


if __name__ == "__main__":
    main()