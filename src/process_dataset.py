import sys
import chess
import chess.engine
import constants
import placements
import automate
import analyse
import random
import json
import os

def main_():
    filename = "dataset_0_1_0_1_2.json"
    with open(filename) as json_file:
        dataset = json.load(json_file)
        for game in dataset:
            print(game["white_comb"])
            print(game["black_comb"])
            print(game["init_board"])
            print(game["init_score"])
            print(game["result"])

def read_json(filename):
    processed_dataset = []
    with open(filename) as json_file:
        dataset = json.load(json_file)
        for game in dataset:
            row = {}
            row["k"] = game["board"].count("k")
            row["n"] = game["board"].count("n")
            row["b"] = game["board"].count("b")
            row["r"] = game["board"].count("r")
            row["q"] = game["board"].count("q")
            row["p"] = game["board"].count("p")
            row["K"] = game["board"].count("K")
            row["N"] = game["board"].count("N")
            row["B"] = game["board"].count("B")
            row["R"] = game["board"].count("R")
            row["Q"] = game["board"].count("Q")
            row["P"] = game["board"].count("P")
            row["winner"] = game["winner"]
            processed_dataset.append(row)
    return processed_dataset
    

def main():
    filename = "dataset1619910837.4141111.json"
    filename = "dataset1619910783.3376644.json"
    # read_json(filename)

    directory = "../dataset"
    out_directory = "../processed_dataset"
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            print(os.path.join(directory, filename))
            processed_dataset = read_json(os.path.join(directory, filename))
            print(len(processed_dataset))
            with open(os.path.join(out_directory, filename[:-4] + "processed.json"), 'w') as fout:
                json.dump(processed_dataset, fout)
        else:
            continue

if __name__ == "__main__":
    main()