import random
import constants
import chess

def init_mini_board():
    # Generate an empty board of 3 ranks
    mini_board = ['-']*24
    return mini_board

def init_full_board():
    # Generate an empty board
    full_board = ['-']*64
    return full_board

def find_idxs(arr, value):
    # Find indexes of a particular value in the array
    # Can be used for finding postions of empty squares or maybe finding occurances of a piece
    indexes = [index for index in range(len(arr)) if arr[index] == value]
    return indexes

def print_mini_board(mini_board):
    print(mini_board[:8])
    print(mini_board[8:16])
    print(mini_board[16:])
    print()

def print_full_board(board):
    for i in range(8):
        print(board[i*8:i*8+8])
    print()

def get_chess_board(board):
    fen = generate_fen(board)
    chess_board = chess.Board(fen)
    return chess_board

def compute_total_points(pawns, knights, bishops, rooks, queens):
    return constants.W_PAWN*pawns + constants.W_KNIGHT*knights + constants.W_BISHOP*bishops + constants.W_ROOK*rooks + constants.W_QUEEN*queens

def check_feasible_comb(pawns, knights, bishops, rooks, queens):
    # Check if number of pawns is within limits
    if pawns > constants.MAX_PAWNS | pawns < constants.MIN_PAWNS:
        return False
    # Check if total points is within limits
    total_points = compute_total_points(pawns, knights, bishops, rooks, queens)
    if total_points > constants.W_TOTAL or total_points < constants.W_TOTAL - 2:
        return False
    return True

def square_to_index(sq):
    col = ord(sq[0]) - ord('a')
    row = 8 - int(sq[1])
    return row*8 + col

def index_to_square(idx):
    row = idx//8
    row = 8 - row
    col = idx%8
    col = chr(ord('a') + col)
    sq = str(col) + str(row)
    return sq

def isempty(board, idx):
    if board[idx] == "-":
        return True
    return False

def isempty_square(board, square):
    idx = square_to_index(square)
    return isempty(board, idx)

def isterminal(board):
    if 'k' in board and 'K' in board:
        return True
    return False

def place_fboard_piece(board, piece, sq):
    # Place given piece on full board at a given position
    idx = square_to_index(sq)
    if not isempty(board, idx):
        print("Square already occupied.")
        return False
    
    board[idx] = piece
    return True

def remove_piece(board, square):
    # Remove the piece from the given square
    idx = square_to_index(square)
    if isempty(board, idx):
        print("No piece in the square.")
        return False
    
    board[idx] = '-'
    return True

def place_piece(board, piece, square):
    # Make a move in automate variant
    # Here the move means a player placing his/her piece in one of the feasible squares
    # Piece is case sensitve
    rank = int(square[1])
    if piece.isupper(): # White
        if piece == "P": # Pawn
            if not (rank == 2 or rank == 3):
                print("White pawns can only be placed in 2nd and 3rd ranks")
                return False
        else: # Other pieces
            if not (rank == 1 or rank == 2):
                print("White pieces can only be placed in 1st and 2nd ranks")
                return False
    else: # Black
        if piece == "p": # Pawn
            if not (rank == 6 or rank == 7):
                print("Black pawns can only be placed in 6th and 7th ranks")
                return False
        else: # Other pieces
            if not (rank == 7 or rank == 8):
                print("Black pieces can only be placed in 7th and 8th ranks")
                return False

    return place_fboard_piece(board, piece, square)

def count_pieces(board, piece):
    count = 0
    for p in board:
        if p == piece:
            count += 1
    return count

def place_mboard_rand_pawn(mini_board):
    # A pawn can be placed in the first two rows
    empty_idxs = find_idxs(mini_board[:16], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the pawn
        # Not possible in normal circumstances
        return False
    mini_board[random.choice(empty_idxs)] = 'P'
    return True # For success

def place_mboard_rand_knight(mini_board):
    # A Knight can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the knight
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'N'
    return True # For success

def place_mboard_rand_bishop(mini_board):
    # A Bishop can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the Bishop
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'B'
    return True # For success

def place_mboard_rand_rook(mini_board):
    # A Rook can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the Rook
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'R'
    return True # For success

def place_mboard_rand_queen(mini_board):
    # A Queen can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the Queen
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'Q'
    return True # For success

def place_mboard_rand_king(mini_board):
    king_idxs = find_idxs(mini_board[8:], 'K')
    if len(king_idxs) != 0:
        # There is already a king on the board. Placing another is illegal
        return False
    # A King can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the King
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'K'
    return True # For success

def generate_placement(pawns, knights, bishops, rooks, queens):
    # Simplifying assumption on order of piece placement: pawns -> knights -> bishops -> rooks -> queens
    # To Do: Handle jumbled order 
    # To Do: Implement turn based placement
    # To Do: Implement turn based placement without deciding the combination beforehand
    # To Do: Corner case where black has a check before the very first move - check for validity after the board is generated. handled in consumer (automate.py)
    mini_board = ['-']*24
    while(pawns):
        if not place_mboard_rand_pawn(mini_board):
            print("Pawn not placed!")
        pawns -= 1
    while(knights):
        if not place_mboard_rand_knight(mini_board):
            print("Knight not placed!")
        knights -= 1
    while(bishops):
        if not place_mboard_rand_bishop(mini_board):
            print("Bishop not placed!")
        bishops -= 1
    while(rooks):
        if not place_mboard_rand_rook(mini_board):
            print("Rook not placed!")
        rooks -= 1
    while(queens):
        if not place_mboard_rand_queen(mini_board):
            print("Queen not placed!")
        queens -= 1
    if not place_mboard_rand_king(mini_board):
        print("No place for king!")

    # print_mini_board(mini_board)
    return mini_board

def generate_fen(board):
    fen = ""
    for i in range(8):
        n = 0
        for j in range(i*8, i*8 + 8):
            if board[j] == '-':
                n += 1
            else:
                if n != 0:
                    fen += str(n)
                fen += board[j]
                n = 0
        if n != 0:
            fen += str(n)
        fen += '/' if fen.count('/') < 7 else ''
    fen += ' w - - 0 1\n'
    return fen

def generate_board(white_mini_board, black_mini_board):
    black_mini_board = [x.lower() for x in black_mini_board]
    board = init_full_board()
    for i in range(24):
        board[i] = black_mini_board[24 - 1 - i]
    for i in range(24):
        board[5*8 + i] = white_mini_board[i]
    return board

def unit_tests():
    # Valid combination
    pawns = 6
    queens = 2
    knights = 5
    bishops = 0
    rooks = 0
    comb = [pawns, knights, bishops, rooks, queens]
    print(comb)
    print(check_feasible_comb(*comb))

    # Inalid combination
    pawns = 6
    queens = 2
    knights = 6
    bishops = 0
    rooks = 0
    comb = [pawns, knights, bishops, rooks, queens]
    print(comb)
    print(check_feasible_comb(*comb))

    mini_board = init_mini_board()
    print_mini_board(mini_board)
    place_mboard_rand_pawn(mini_board)
    place_mboard_rand_knight(mini_board)
    place_mboard_rand_bishop(mini_board)
    place_mboard_rand_rook(mini_board)
    place_mboard_rand_queen(mini_board)
    place_mboard_rand_king(mini_board)
    print_mini_board(mini_board)

    print("White's placements")
    comb = random.choice(constants.COMBINATIONS)
    print(comb)
    print(check_feasible_comb(*comb))
    white_mini_board = generate_placement(*comb)

    print("Black's placements")
    comb = random.choice(constants.COMBINATIONS)
    print(comb)
    print(check_feasible_comb(*comb))
    black_mini_board = generate_placement(*comb)

    board = generate_board(white_mini_board, black_mini_board)
    print_full_board(board)
    fen = generate_fen(board)
    print(fen)
    print(square_to_index("h1"))
    print(place_fboard_piece(board, 'n', 'a4'))
    print_full_board(board)
    print(index_to_square(9))

    board = init_full_board()
    print_full_board(board)
    success = place_piece(board, 'P', 'a2')
    print(success)
    print_full_board(board)
    success = place_piece(board, 'P', 'a4')
    print(success)
    print_full_board(board)
    success = place_piece(board, 'p', 'a2')
    print(success)
    print_full_board(board)
    success = place_piece(board, 'K', 'a2')
    print(success)
    print_full_board(board)

# unit_tests()
