import sys
import chess
import chess.engine
import constants
import placements
import automate
import analyse
import random
import json

def main():
    filename = "dataset_0_1_0_1_2.json"
    with open(filename) as json_file:
        dataset = json.load(json_file)
        for game in dataset:
            print(game["white_comb"])
            print(game["black_comb"])
            print(game["init_board"])
            print(game["init_score"])
            print(game["result"])

if __name__ == "__main__":
    main()