import chess
import chess.engine
import constants
import placements
import random
import analyse
import copy

class AutomateGame:
    def __init__(self):
        self.board = placements.init_full_board() # Board
        self.white_pts = constants.W_TOTAL # Total points left with white
        self.black_pts = constants.W_TOTAL # Total points left with black
        self.turn = True # Whose turn is it - 'True' for white 'False' for black
        self.white_king = False # Is white king already placed
        self.black_king = False # Is black king already placed
        self.move_count = 0 # Keep track of number of moves played
        self.move_history = []

    def is_initial(self):
        return self.move_count == 0

    def legal_moves(self):
        move_list = []
        if self.turn:
            if self.white_king:
                return [] # If king already placed. No legal moves available
            avail_pieces = []
            if self.move_count < constants.MIN_PAWNS:
                avail_pieces.append('P')
            else:
                if self.white_pts >= constants.W_PAWN and placements.count_pieces(self.board, 'P') < constants.MAX_PAWNS:
                    avail_pieces.append('P')
                if self.white_pts >= constants.W_KNIGHT:
                    avail_pieces.append('N')
                if self.white_pts >= constants.W_BISHOP:
                    avail_pieces.append('B')
                if self.white_pts >= constants.W_ROOK:
                    avail_pieces.append('R')
                if self.white_pts >= constants.W_QUEEN:
                    avail_pieces.append('Q')
                # King can be placed only if no other piece can be placed
                # It is possible when the player has spent all the points or he/she is left with no other piece to play
                if self.white_pts == 0 or (self.white_pts < min(constants.W_KNIGHT, constants.W_BISHOP, constants.W_ROOK, constants.W_QUEEN) and placements.count_pieces(self.board, 'P') == constants.MAX_PAWNS):
                    avail_pieces.append('K')
            for piece in avail_pieces:
                if piece == "P":
                    for i in range(8):
                        square = chr(ord('a') + i) + "2"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
                        square = chr(ord('a') + i) + "3"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
                else:
                    for i in range(8):
                        square = chr(ord('a') + i) + "1"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
                        square = chr(ord('a') + i) + "2"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
        else:
            if self.black_king:
                return [] # If king already placed. No legal moves available
            avail_pieces = []
            if self.move_count < constants.MIN_PAWNS:
                avail_pieces.append('p')
            else:
                if self.black_pts >= constants.W_PAWN and placements.count_pieces(self.board, 'p') < constants.MAX_PAWNS:
                    avail_pieces.append('p')
                if self.black_pts >= constants.W_KNIGHT:
                    avail_pieces.append('n')
                if self.black_pts >= constants.W_BISHOP:
                    avail_pieces.append('b')
                if self.black_pts >= constants.W_ROOK:
                    avail_pieces.append('r')
                if self.black_pts >= constants.W_QUEEN:
                    avail_pieces.append('q')
                # King can be placed only if no other piece can be placed
                # It is possible when the player has spent all the points or he/she is left with no other piece to play
                if self.black_pts == 0 or (self.black_pts < min(constants.W_KNIGHT, constants.W_BISHOP, constants.W_ROOK, constants.W_QUEEN) and placements.count_pieces(self.board, 'p') == constants.MAX_PAWNS):
                    avail_pieces.append('k')
            for piece in avail_pieces:
                if piece == "p":
                    for i in range(8):
                        square = chr(ord('a') + i) + "6"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
                        square = chr(ord('a') + i) + "7"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
                else:
                    for i in range(8):
                        square = chr(ord('a') + i) + "8"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))
                        square = chr(ord('a') + i) + "7"
                        if placements.isempty_square(self.board, square):
                            move_list.append((piece, square))

        return move_list
    
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
                self.turn = not self.turn
            elif piece  == 'K':
                self.white_king = True
                self.turn = not self.turn
            else:
                # Reduce the value from the total available points by the piece value
                if piece.isupper():
                    self.white_pts -= constants.PIECE_VALUES[piece]
                    if self.black_king: # Don't switch the turn if black king is already placed
                        pass
                    else:
                        self.turn = not self.turn # Switch the turn to other player
                else:
                    self.black_pts -= constants.PIECE_VALUES[piece]
                    if self.white_king: # Don't switch the turn if white king is already placed
                        pass
                    else:
                        self.turn = not self.turn # Switch the turn to other player
            
            self.move_count += 0.5 # Increment the move count
            self.move_history.append((piece, square))
            return True
        print("Illegal Move")
        return False

    def undo_move(self):
        piece, square = self.move_history[-1]
        return placements.remove_piece(self.board, square)

    def print_board(self):
        placements.print_full_board(self.board)
    
    def print_game(self):
        print("Automate Game Object")
        print("Board ---")
        self.print_board()
        print("White's available points: ", self.white_pts)
        print("Black's available points: ", self.black_pts)

    def get_chess_board(self):
        return placements.get_chess_board(self.board)

    def game_over(self):
        if len(self.legal_moves()) == 0:
            return True
        return False

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
            self.final_board = self.get_chess_board()
            if self.final_board.is_valid():
                break
        return self.final_board

    def initial_position(self):
        return AutomateGame.Position(self.board, self.turn, self.white_pts, self.black_pts, self.move_count)

    class Position():
        def __init__(self, board, turn=True, white_pts=0, black_pts=0, move_count=200):
            self.board = board
            self.turn = turn
            self.white_pts = white_pts
            self.black_pts = black_pts
            self.white_king = 'K' in self.board
            self.black_king = 'k' in self.board
            self.move_count = move_count
            self.winner = None
            self._compute_hash()
        
        def print_board(self):
            placements.print_full_board(self.board)

        def print_position(self):
            print("Automate Position Object")
            print("Board ---")
            self.print_board()
            print("White's available points: ", self.white_pts)
            print("Black's available points: ", self.black_pts)

        def is_initial(self):
            return self.board.count('-') == len(self.board)

        def next_player(self):
            return self.turn
        
        def legal_moves(self):
            move_list = []
            if self.turn:
                if self.white_king:
                    return [] # If king already placed. No legal moves available
                avail_pieces = []
                if self.move_count < constants.MIN_PAWNS:
                    avail_pieces.append('P')
                else:
                    if self.white_pts >= constants.W_PAWN and placements.count_pieces(self.board, 'P') < constants.MAX_PAWNS:
                        avail_pieces.append('P')
                    if self.white_pts >= constants.W_KNIGHT:
                        avail_pieces.append('N')
                    if self.white_pts >= constants.W_BISHOP:
                        avail_pieces.append('B')
                    if self.white_pts >= constants.W_ROOK:
                        avail_pieces.append('R')
                    if self.white_pts >= constants.W_QUEEN:
                        avail_pieces.append('Q')
                    # King can be placed only if no other piece can be placed
                    # It is possible when the player has spent all the points or he/she is left with no other piece to play
                    if self.white_pts == 0 or (self.white_pts < min(constants.W_KNIGHT, constants.W_BISHOP, constants.W_ROOK, constants.W_QUEEN) and placements.count_pieces(self.board, 'P') == constants.MAX_PAWNS):
                        avail_pieces.append('K')
                for piece in avail_pieces:
                    if piece == "P":
                        for i in range(8):
                            square = chr(ord('a') + i) + "2"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
                            square = chr(ord('a') + i) + "3"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
                    else:
                        for i in range(8):
                            square = chr(ord('a') + i) + "1"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
                            square = chr(ord('a') + i) + "2"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
            else:
                if self.black_king:
                    return [] # If king already placed. No legal moves available
                avail_pieces = []
                if self.move_count < constants.MIN_PAWNS:
                    avail_pieces.append('p')
                else:
                    if self.black_pts >= constants.W_PAWN and placements.count_pieces(self.board, 'p') < constants.MAX_PAWNS:
                        avail_pieces.append('p')
                    if self.black_pts >= constants.W_KNIGHT:
                        avail_pieces.append('n')
                    if self.black_pts >= constants.W_BISHOP:
                        avail_pieces.append('b')
                    if self.black_pts >= constants.W_ROOK:
                        avail_pieces.append('r')
                    if self.black_pts >= constants.W_QUEEN:
                        avail_pieces.append('q')
                    # King can be placed only if no other piece can be placed
                    # It is possible when the player has spent all the points or he/she is left with no other piece to play
                    if self.black_pts == 0 or (self.black_pts < min(constants.W_KNIGHT, constants.W_BISHOP, constants.W_ROOK, constants.W_QUEEN) and placements.count_pieces(self.board, 'p') == constants.MAX_PAWNS):
                        avail_pieces.append('k')
                for piece in avail_pieces:
                    if piece == "p":
                        for i in range(8):
                            square = chr(ord('a') + i) + "6"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
                            square = chr(ord('a') + i) + "7"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
                    else:
                        for i in range(8):
                            square = chr(ord('a') + i) + "8"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))
                            square = chr(ord('a') + i) + "7"
                            if placements.isempty_square(self.board, square):
                                move_list.append((piece, square))

            return move_list
        
        def result(self, piece, square):
            if piece.isupper():
                if self.turn == False:
                    print("Not white's turn")
                    return None
                if self.move_count < constants.MIN_PAWNS and piece != 'P':
                    print("The first few moves has to be pawns")
                    return None
                if self.white_king:
                    print("King has to be placed at the end")
                    return None
                if self.white_pts - constants.PIECE_VALUES[piece] < 0:
                    print("Can't spend more than available points")
                    return None
            else:
                if self.turn == True:
                    print("Not black's turn")
                    return None
                if self.move_count < constants.MIN_PAWNS and piece != 'p':
                    print("The first few moves has to be pawns")
                    return None
                if self.black_king:
                    print("King has to be placed at the end")
                    return None
                if self.black_pts - constants.PIECE_VALUES[piece] < 0:
                    print("Can't spend more than available points")
                    return None
            clone_board = copy.deepcopy(self.board)
            if placements.place_piece(clone_board, piece, square):
                # Will return false if not placed in feasible ranks and if the square is already occupied
                # Set king placements if king is placed
                succ = AutomateGame.Position(clone_board, self.turn, self.white_pts, self.black_pts, self.move_count)
                if piece == 'k':
                    succ.black_king = True
                    succ.turn = True
                elif piece  == 'K':
                    succ.white_king = True
                    succ.turn = False
                else:
                    # Reduce the value from the total available points by the piece value
                    if piece.isupper():
                        succ.white_pts -= constants.PIECE_VALUES[piece]
                        if succ.black_king: # Don't switch the turn if black king is already placed
                            pass
                        else:
                            succ.turn = not self.turn # Switch the turn to other player
                    else:
                        succ.black_pts -= constants.PIECE_VALUES[piece]
                        if succ.white_king: # Don't switch the turn if white king is already placed
                            pass
                        else:
                            succ.turn = not self.turn # Switch the turn to other player
                
                succ.move_count += 0.5 # Increment the move count
                return succ
            print("Illegal Move")
            return None

        def game_over(self):
            return self.white_king and self.black_king

        def get_winner(self, engine):
            ''' Determines the winner of a game in this position, or None
                if this position is not final.  The return value is 1 if
                player 1 won, -1 if player 2 won, and 0 if the game is a draw.
            '''
            if self.game_over() and self.winner is None:
                self.winner = analyse.simulate_and_report_result(engine, placements.get_chess_board(self.board))
            return self.winner
        
        def _compute_hash(self):
            # faster hash computation; thanks to CF
            self.hash = hash(tuple(self.board)) * 2 + int(self.turn)

        def __hash__(self):
            return self.hash
        
        def get_chess_board(self):
            return placements.get_chess_board(self.board)

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
    # Tests
    game = AutomateGame()
    print(game.legal_moves())
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
    game.print_game()
    success = game.move('p', 'e6')
    game.print_game()
    success = game.undo_move()
    game.print_game()
    success = game.move('N', 'a1')
    success = game.move('n', 'a8')
    success = game.move('B', 'h1')
    success = game.move('b', 'h8')
    print(game.legal_moves())
    success = game.move('Q', 'g2')
    print(game.legal_moves())
    # random_game()
    game = AutomateGame()
    while True:
        move_list = game.legal_moves()
        if len(move_list) == 0:
            break
        m = random.choice(move_list)
        game.move(m[0], m[1])
    game.print_game()

    engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
    # analyse.simulate_analyse_and_plot_game(engine, game.get_chess_board())
    score_list = analyse.simulate_and_analyse_game(engine, game.get_chess_board())
    print(score_list)

    game = AutomateGame()
    while True:
        move_list = game.legal_moves()
        if len(move_list) == 0:
            break
        m = random.choice(move_list)
        game.move(m[0], m[1])
    game.print_game()

    engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
    winner = analyse.simulate_and_report_result(engine, game.get_chess_board())
    print(winner)
    engine.quit()

if __name__ == "__main__":
    main()