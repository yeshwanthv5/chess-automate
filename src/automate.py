import chess
import chess.engine
import constants
import placements
import random

def setup_random_game(white_preferred_combs = constants.COMBINATIONS, black_preferred_combs = constants.COMBINATIONS):
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

        board = placements.generate_board(white_mini_board, black_mini_board)
        # placements.print_full_board(board)
        fen = placements.generate_fen(board)
        # print(fen)
        board = chess.Board(fen)
        if board.is_valid():
            break
    return board

def main():
    pondertime = 1.0
    maxmoves = 200
    dictsidetomove = {True:'white',False:'black'}
    notationdict = {True:'.', False:'...'}
    board = setup_random_game()
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

if __name__ == "__main__":
    main()