import sys
import chess
import chess.engine
import constants
import placements
import automate
import analyse
import random
import json

def create_dataset(filename, white_range = (0, 1), black_range = (0, 1), reps = 1):
    engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
    all_combs = constants.COMBINATIONS
    dataset = []
    for white_comb in all_combs[white_range[0]:white_range[1]]:
        for black_comb in all_combs[black_range[0]:black_range[1]]:
            for _ in range(reps):
                row = {}
                board = automate.setup_random_game(white_preferred_combs=[white_comb], black_preferred_combs=[black_comb])
                init_board = board.fen()
                score_list = analyse.simulate_and_analyse_game(engine, board)
                if score_list[-1] == 0:
                    result = 0
                elif score_list[-1] < 0:
                    result = -1
                else:
                    result = 1
                row["white_comb"] = white_comb
                row["black_comb"] = black_comb
                row["init_board"] = init_board
                row["init_score"] = score_list[0]
                row["result"] = result
                dataset.append(row)
                print(row)

    with open(filename, 'w') as fout:
        json.dump(dataset, fout)
    engine.quit()

def main():
    white_range = (int(sys.argv[1]), int(sys.argv[2]))
    black_range = (int(sys.argv[3]), int(sys.argv[4]))
    reps = int(sys.argv[5])
    filename = "dataset_" + str(white_range[0]) + "_" + str(white_range[1]) + "_" + str(black_range[0]) + "_" + str(black_range[1]) + "_" + str(reps) + ".json"
    create_dataset(filename, white_range=white_range, black_range=black_range, reps = reps)

if __name__ == "__main__":
    main()