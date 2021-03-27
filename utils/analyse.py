import chess.engine
import constants
import plots

def analyse_board(engine, board, time_limit = constants.PONDER_TIME):
    ### Takes in chess.engine chess.Board object 
    limit = chess.engine.Limit(time=time_limit)
    info = engine.analyse(board, limit)
    score = 0
    score_str = str(info["score"].white())
    if score_str[0] == '#':
        if score_str[1] == '+':
            score = constants.MATE_VALUE
        else:
            score = -1*constants.MATE_VALUE
    else:
        score = int(score_str)
    return score

def find_next_move(engine, board, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    result = engine.play(board, limit)
    return result.move

def analyse_game(engine, init_board, time_limit = constants.PONDER_TIME):
    board = init_board
    limit = chess.engine.Limit(time=time_limit)
    score_list = []
    while not board.is_game_over() and board.fullmove_number<=constants.MAXMOVES:
        score = analyse_board(engine, board)
        score_list.append(score)
        move = find_next_move(engine, board)
        board.push(move)
    return score_list

def analyse_and_plot_game(engine, init_board, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    score_list = analyse_game(engine, init_board, time_limit = time_limit)
    plots.simple_plot(score_list, y_label="Evaluation Score (Centipawns, WHITE Pov)", x_label="Move", title="Game Evaluation")