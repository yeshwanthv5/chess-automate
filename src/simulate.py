import sys
import chess
import chess.engine
import constants
import placements
import random
import automate
import analyse

engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
board = automate.setup_random_game()
analyse.simulate_analyse_and_plot_game(engine, board)
engine.quit()