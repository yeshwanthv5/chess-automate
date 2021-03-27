import random
import constants

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

def place_pawn(mini_board):
    # A pawn can be placed in the first two rows
    empty_idxs = find_idxs(mini_board[:16], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the pawn
        # Not possible in normal circumstances
        return False
    mini_board[random.choice(empty_idxs)] = 'P'
    return True # For success

def place_knight(mini_board):
    # A Knight can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the knight
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'N'
    return True # For success

def place_bishop(mini_board):
    # A Bishop can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the Bishop
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'B'
    return True # For success

def place_rook(mini_board):
    # A Rook can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the Rook
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'R'
    return True # For success

def place_queen(mini_board):
    # A Queen can be placed in the last two rows
    empty_idxs = find_idxs(mini_board[8:], '-')
    if len(empty_idxs) == 0:
        # No empty square for placing the Queen
        return False
    mini_board[8 + random.choice(empty_idxs)] = 'Q'
    return True # For success

def place_king(mini_board):
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
    # To Do: Corner case where black has a check before the very first move
    mini_board = ['-']*24
    while(pawns):
        if not place_pawn(mini_board):
            print("Pawn not placed!")
        pawns -= 1
    while(knights):
        if not place_knight(mini_board):
            print("Knight not placed!")
        knights -= 1
    while(bishops):
        if not place_bishop(mini_board):
            print("Bishop not placed!")
        bishops -= 1
    while(rooks):
        if not place_rook(mini_board):
            print("Rook not placed!")
        rooks -= 1
    while(queens):
        if not place_queen(mini_board):
            print("Queen not placed!")
        queens -= 1
    if not place_king(mini_board):
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
    place_pawn(mini_board)
    place_knight(mini_board)
    place_bishop(mini_board)
    place_rook(mini_board)
    place_queen(mini_board)
    place_king(mini_board)
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

# unit_tests()