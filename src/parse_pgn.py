import chess.pgn
import copy

def extract_games_from_pgn(pgn):
    game_list = []
    while True:
        game = chess.pgn.read_game(pgn)
        if game == None:
            break
        game_list.append(game)
    return game_list
