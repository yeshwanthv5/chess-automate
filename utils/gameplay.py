import sys
import chess
import chess.engine
import constants
import placements
import random
import automate
import analyse


dictsidetomove = {True:'white',False:'black'}
notationdict = {True:'.', False:'...'}

def simulate_game(board):
    engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
    score = analyse.analyse_board(engine, board)
    print("Score:", score)
    limit = chess.engine.Limit(time=constants.PONDER_TIME)
    result = engine.play(board, limit)
    print(result.move)
    while not board.is_game_over() and board.fullmove_number<=constants.MAXMOVES:
        score = analyse.analyse_board(engine, board)
        print(score)
        move = analyse.find_next_move(engine, board)
        print(dictsidetomove[board.turn]+' played '+str(board.fullmove_number)+notationdict[board.turn]+str(board.san(move)))
        board.push(move)
    print(board)
    print('Final position FEN: ',board.fen())
    score = analyse.analyse_board(engine, board)
    print("Score:", score)
    print('-----')
    engine.quit()

# board = automate.setup_random_game()
# simulate_game(board)

engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
board = automate.setup_random_game()
analyse.simulate_analyse_and_plot_game(engine, board)
engine.quit()