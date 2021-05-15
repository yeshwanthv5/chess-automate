import random
import automate
import math
import operator
import chess
import constants
import time

class TreeNode:
    # Tree Node: keeps track of node stats visits and wins, stores list of unexpanded moves and keeps pointers to expanded children nodes
    def __init__(self, pos):
        self.pos = pos
        self.visits = 0
        self.wins = 0
        self.terminal = False
        if self.pos.game_over():
            self.terminal = True
        self.unexpanded_moves = pos.legal_moves()
        self.expanded_children = {} # Dictionary of children keys are moves and values are node

def random_choice(position):
    # Returns a random move given a position
    moves = position.legal_moves()
    return random.choice(moves)

def default_policy(node, engine):
    # Runs default policy of selecting random moves until a terminal position is reached
    pos = node.pos
    while pos.game_over() == False:
        pos = pos.result(*random_choice(pos))
    score = pos.get_winner(engine)
    node.visits += 1
    if score == 1:
        node.wins += 1
    elif score == 0:
        node.wins += 0.5
    return score    

def traverse_tree(node, lookup_table, engine):
    if node.terminal: # If current node is terminal return zero
        score = node.pos.get_winner(engine)
    else:
        if len(node.unexpanded_moves): # If there are unexpanded children expand one of them
            choice = random.randint(0, len(node.unexpanded_moves) - 1)
            node_to_expand = TreeNode(node.pos.result(*node.unexpanded_moves[choice]))
            lookup_table[node.pos.result(*node.unexpanded_moves[choice])] = node_to_expand
            node.expanded_children[node.unexpanded_moves[choice]] = node_to_expand
            node.unexpanded_moves.pop(choice)
            score = default_policy(node_to_expand, engine)
        else: # If all the nodes are expanded choose the child based on UCT policy
            if node.pos.next_player() == True:
                choices = {move:(child.wins/child.visits + math.sqrt(0.5*math.log(node.visits)/child.visits)) for move, child in node.expanded_children.items()}
            else:
                choices = {move:(1-1*child.wins/child.visits + math.sqrt(0.5*math.log(node.visits)/child.visits)) for move, child in node.expanded_children.items()}
            score = traverse_tree(node.expanded_children[max(choices.items(), key=operator.itemgetter(1))[0]], lookup_table, engine)
    # Update stats for nodes. Backprop is handled through recursion.
    node.visits += 1
    if score == 1:
        node.wins += 1
    elif score == 0:
        node.wins += 0.5
    return score

def mcts(pos, num_iters, lookup_table, engine):
    # Given a position, run mcts for the given number of iterations and return the best move
    if pos in lookup_table.keys():
        root = lookup_table[pos]
    else:
        root = TreeNode(pos)
        lookup_table[pos] = root
    while num_iters:
        score = traverse_tree(root, lookup_table, engine)
        num_iters -= 1
    moves = pos.legal_moves()

    choices = {move: (child.wins/child.visits) for move, child in root.expanded_children.items()} # Exploration term is omitted from this

    if root.pos.next_player() == True:
        ans = max(choices.items(), key=operator.itemgetter(1))[0] # Pick max node for player 0
    else:
        ans = min(choices.items(), key=operator.itemgetter(1))[0] # Pick min node for player 1
    return ans

def mcts_strategy(num_iters, engine):
    # Main function. Creates a new tree whenever this function is called. Returns a function that takes in position and returns the best move
    root = None
    lookup_table = {}
    def fxn(pos):
        if pos.is_initial():
            root = TreeNode(pos)
            lookup_table[pos] = root
        move = mcts(pos, num_iters, lookup_table, engine)
        return move
    return fxn

def main():
    n = 50
    num_games = 20
    p1_wins = 0
    p2_wins = 0
    draws = 0
    engine = chess.engine.SimpleEngine.popen_uci(constants.SF_PATH)
    mcts_player = lambda: mcts_strategy(n, engine)
    total_moves = 0
    total_time = 0
    for i in range(num_games):
        mcts_strat = mcts_player()
        game = automate.AutomateGame()
        pos = game.initial_position()
        while not pos.game_over():
            move_list = pos.legal_moves()
            if len(move_list) == 0:
                break
            if pos.turn:
                start_t = time.time()
                m = mcts_strat(pos)
                end_t = time.time()
                total_time += (end_t - start_t)
                total_moves += 1
                print("White:", m)
                print("Time:", end_t-start_t)
            else:
                m = random.choice(move_list)
                print("Black:", m)
            pos = pos.result(*m)
        # game.print_game()
        winner = pos.get_winner(engine)
        print("Winner:", winner)
        if winner == 0:
            # p1_wins += 0.5
            # p2_wins += 0.5
            draws += 1
        elif winner > 0:
            p1_wins += 1
        else:
            p2_wins += 1
    engine.quit()
    print("P1/P2/Draw/Games: {}/{}/{}/{}".format(p1_wins, p2_wins, draws, num_games))
    print("Avg time per move:", total_time/total_moves)

if __name__ == '__main__':
    main()