import chess.engine
import constants
import plots
import copy

def analyse_board(engine, board, time_limit = constants.PONDER_TIME):
    ### Takes in chess.engine and chess.Board objects and returns evaluation score (Centipawns) in white's pov
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
        if score_str[0] == '+':
            score = min(int(score_str), constants.MATE_VALUE)
        else:
            score = max(int(score_str), -1*constants.MATE_VALUE)
    return score

def find_next_move(engine, board, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    result = engine.play(board, limit)
    return result.move

def simulate_game(engine, init_board, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    board = init_board
    move_history = [copy.deepcopy(board)]
    while not board.is_game_over() and board.fullmove_number<=constants.MAXMOVES:
        move = find_next_move(engine, board, time_limit=time_limit)
        board.push(move)
        move_history.append(copy.deepcopy(board))
    return move_history

def analyse_game(engine, move_history, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    score_list = []
    for curr_board in move_history:
        score = analyse_board(engine, curr_board, time_limit=time_limit)
        score_list.append(score)
    return score_list

def simulate_and_analyse_game(engine, init_board, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    move_history = simulate_game(engine, init_board, time_limit = time_limit)
    score_list = analyse_game(engine, move_history, time_limit=time_limit)
    return score_list

def simulate_analyse_and_plot_game(engine, init_board, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    score_list = simulate_and_analyse_game(engine, init_board, time_limit = time_limit)
    path = plots.simple_plot(score_list, y_label="Evaluation Score (Centipawns, WHITE Pov)", x_label="Move", title="Game Evaluation")
    return path

def analyse_and_plot_history(engine, move_history, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    score_list = analyse_game(engine, move_history, time_limit=time_limit)
    path = plots.simple_plot(score_list, y_label="Evaluation Score (Centipawns, WHITE Pov)", x_label="Move", title="Game Evaluation")
    return path

def analyse_pgn_game(engine, game, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    board = game.board()
    move_history = [copy.deepcopy(board)]
    for move in game.mainline_moves():
        board.push(move)
        move_history.append(copy.deepcopy(board))
    score_list = analyse_game(engine, move_history, time_limit=time_limit)
    return score_list

def analyse_and_plot_pgn_game(engine, game, time_limit = constants.PONDER_TIME):
    limit = chess.engine.Limit(time=time_limit)
    score_list = analyse_pgn_game(engine, game, time_limit = time_limit)
    path = plots.simple_plot(score_list, y_label="Evaluation Score (Centipawns, WHITE Pov)", x_label="Move", title="Game Evaluation")
    return path
