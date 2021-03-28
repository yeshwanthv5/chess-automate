MAXMOVES = 200
PONDER_TIME = 0.5

W_PAWN = 1
W_KNIGHT = 3
W_BISHOP = 3
W_ROOK = 4
W_QUEEN = 7
W_TOTAL = 35
MAX_PAWNS = 10
MIN_PAWNS = 6

COMBINATIONS = [[6, 0, 0, 2, 3], [6, 0, 1, 3, 2], [6, 0, 2, 4, 1], [6, 0, 3, 5, 0], [6, 0, 5, 0, 2], [6, 0, 6, 1, 1], [6, 0, 7, 2, 0], [6, 1, 0, 3, 2], [6, 1, 1, 4, 1], [6, 1, 2, 5, 0], [6, 1, 4, 0, 2], [6, 1, 5, 1, 1], [6, 1, 6, 2, 0], [6, 2, 0, 4, 1], [6, 2, 1, 5, 0], [6, 2, 3, 0, 2], [6, 2, 4, 1, 1], [6, 2, 5, 2, 0], [6, 3, 0, 5, 0], [6, 3, 2, 0, 2], [6, 3, 3, 1, 1], [6, 3, 4, 2, 0], [6, 4, 1, 0, 2], [6, 4, 2, 1, 1], [6, 4, 3, 2, 0], [6, 5, 0, 0, 2], [6, 5, 1, 1, 1], [6, 5, 2, 2, 0], [6, 6, 0, 1, 1], [6, 6, 1, 2, 0], [6, 7, 0, 2, 0], [7, 0, 0, 0, 4], [7, 0, 1, 1, 3], [7, 0, 2, 2, 2], [7, 0, 3, 3, 1], [7, 0, 4, 4, 0], [7, 0, 7, 0, 1], [7, 0, 8, 1, 0], [7, 1, 0, 1, 3], [7, 1, 1, 2, 2], [7, 1, 2, 3, 1], [7, 1, 3, 4, 0], [7, 1, 6, 0, 1], [7, 1, 7, 1, 0], [7, 2, 0, 2, 2], [7, 2, 1, 3, 1], [7, 2, 2, 4, 0], [7, 2, 5, 0, 1], [7, 2, 6, 1, 0], [7, 3, 0, 3, 1], [7, 3, 1, 4, 0], [7, 3, 4, 0, 1], [7, 3, 5, 1, 0], [7, 4, 0, 4, 0], [7, 4, 3, 0, 1], [7, 4, 4, 1, 0], [7, 5, 2, 0, 1], [7, 5, 3, 1, 0], [7, 6, 1, 0, 1], [7, 6, 2, 1, 0], [7, 7, 0, 0, 1], [7, 7, 1, 1, 0], [7, 8, 0, 1, 0], [8, 0, 0, 5, 1], [8, 0, 2, 0, 3], [8, 0, 3, 1, 2], [8, 0, 4, 2, 1], [8, 0, 5, 3, 0], [8, 0, 9, 0, 0], [8, 1, 1, 0, 3], [8, 1, 2, 1, 2], [8, 1, 3, 2, 1], [8, 1, 4, 3, 0], [8, 1, 8, 0, 0], [8, 2, 0, 0, 3], [8, 2, 1, 1, 2], [8, 2, 2, 2, 1], [8, 2, 3, 3, 0], [8, 2, 7, 0, 0], [8, 3, 0, 1, 2], [8, 3, 1, 2, 1], [8, 3, 2, 3, 0], [8, 3, 6, 0, 0], [8, 4, 0, 2, 1], [8, 4, 1, 3, 0], [8, 4, 5, 0, 0], [8, 5, 0, 3, 0], [8, 5, 4, 0, 0], [8, 6, 3, 0, 0], [8, 7, 2, 0, 0], [8, 8, 1, 0, 0], [8, 9, 0, 0, 0], [9, 0, 0, 3, 2], [9, 0, 1, 4, 1], [9, 0, 2, 5, 0], [9, 0, 4, 0, 2], [9, 0, 5, 1, 1], [9, 0, 6, 2, 0], [9, 1, 0, 4, 1], [9, 1, 1, 5, 0], [9, 1, 3, 0, 2], [9, 1, 4, 1, 1], [9, 1, 5, 2, 0], [9, 2, 0, 5, 0], [9, 2, 2, 0, 2], [9, 2, 3, 1, 1], [9, 2, 4, 2, 0], [9, 3, 1, 0, 2], [9, 3, 2, 1, 1], [9, 3, 3, 2, 0], [9, 4, 0, 0, 2], [9, 4, 1, 1, 1], [9, 4, 2, 2, 0], [9, 5, 0, 1, 1], [9, 5, 1, 2, 0], [9, 6, 0, 2, 0], [10, 0, 0, 1, 3], [10, 0, 1, 2, 2], [10, 0, 2, 3, 1], [10, 0, 3, 4, 0], [10, 0, 6, 0, 1], [10, 0, 7, 1, 0], [10, 1, 0, 2, 2], [10, 1, 1, 3, 1], [10, 1, 2, 4, 0], [10, 1, 5, 0, 1], [10, 1, 6, 1, 0], [10, 2, 0, 3, 1], [10, 2, 1, 4, 0], [10, 2, 4, 0, 1], [10, 2, 5, 1, 0], [10, 3, 0, 4, 0], [10, 3, 3, 0, 1], [10, 3, 4, 1, 0], [10, 4, 2, 0, 1], [10, 4, 3, 1, 0], [10, 5, 1, 0, 1], [10, 5, 2, 1, 0], [10, 6, 0, 0, 1], [10, 6, 1, 1, 0], [10, 7, 0, 1, 0]]

MATE_VALUE = 15000 # A high number specifying the score for checkmate

SF_PATH = "/path/to/stockfish"

# SF_PATH = "/Users/yesh/Documents/S2021/CPSC 674/Stockfish/src/stockfish"