import argparse
import pandas as pd
from xo_functions import make_move_v2, make_move, prettify_board, get_possible_moves
import random
import numpy as np

columns = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "What file are you using to load or save the model weights?")
parser.add_argument("-n", "--number_of_episodes", help = "How many training episodes to run?")
parser.add_argument("-r", "--rewards", help = "What rewards are applied. Format: w|l|d Sample: '20|-10|10' ")
parser.add_argument("-e", "--epsilon", help = "todo")

# Read arguments from command line
args = parser.parse_args()

file = args.file
n = int(args.number_of_episodes)
reward_win, reward_lose, reward_draw = args.rewards.split("|")
reward_win, reward_lose, reward_draw = int(reward_win), int(reward_lose), int(reward_draw)

model_df = pd.read_csv(file)

print(model_df)

class player:
    def __init__(self, name, file, learning):
        self.name = name
        self.file = file
        self.model_df = pd.read_csv(self.file)
        self.model_df.columns = ["state"] + columns
        self.learning = learning

    def greet(self):
        if self.learning:
            print(f"Hello, my name is {self.name}. I'm an agent in this Reinforcement Learning scenario and I learn as I play the game.")
            print(f"My model has {len(self.model_df)} rows")
        else:
            print(f"Hello, my name is {self.name}. I'm an agent in this Reinforcement Learning scenario and I'm committed to not learning a damn thing.")
        print(f"My model is stored in this location {file} and it has had #TODO training episodes so far")

    def make_model_move(self,b,tt,p):
        #print(f"Turns taken so far {tt}")
        #print(f"Making decision for state: {b}")
        hits = self.model_df[self.model_df["state"] == str(b)][columns].head(1)
        hits = hits.transpose()
        hits.columns = ["values"]
        hits = hits.reset_index()
        max_value = np.nanmax(hits["values"]) # seems bizzare to have to do this, but if the first value is nan then regular max screws up
        #print(f"max value {max_value}")
        top_answers = hits[hits["values"] == max_value]
        m = str(random.choice(list(top_answers["index"])))
        mr, mc = int(m[0]), int(m[1])
        #print(f"{self.name}'s move is {m}")
        b, status, description = make_move_v2(p,b,mr,mc,tt)
        return b, status, description, m

p1 = player("Rolf",file,True)
p1.greet()
p2 = player("Gregg",file,False)
#p2.greet()

x_player_wins = 0
o_player_wins = 0
stalemates = 0
for episode in range(0,n):
    print(f"episode {episode}")
    if 0 == episode % 2:
        x_player = p1
        o_player = p2
    else:
        x_player = p2
        o_player = p1
    x_player_m = []
    o_player_m = []
    x_player_b = []
    o_player_b = []
    b = [[0,0,0],[0,0,0],[0,0,0]]
    status = 0
    tt = 0
    while status == 0 and tt != 9:
        x_turn = True
        b, status, description, m = x_player.make_model_move(b,tt,-1)
        tt += 1
        x_player_m.append(m)
        x_player_b.append(b)
        #print(f"After this most recent move: b is {b}, status is {status} and tt is {tt}")
        if status == 0 and tt != 9: # I'd forgotten this check at first.
            #Interestingly, when the players just picked at random, it always took up to the 7 turns taken for this to become a problem
            x_turn = False
            b, status, description, m = o_player.make_model_move(b,tt,1)
            tt += 1
            o_player_m.append(m)
            o_player_b.append(b)
            #print(f"After this most recent move: b is {b}, status is {status} and tt is {tt}")
    print(f"final status {status}")
    prettify_board(b)
    if status == 1:
        if x_turn:
            print("X won.")
            x_player_wins += 1
            #print(x_player_m)
            #print(x_player_b)
        else:
            print("O won")
            o_player_wins += 1
    if status == 2:
        print("no one won")
        stalemates += 1

print(f"\nX wins {x_player_wins}")
print(f"O wins {o_player_wins}")
print(f"stalemates wins {stalemates}")

# Even when just picking at random, the player who goes first wins more often
# After 1000 games of totally naive players, no learning in place:
# X won 598 games, O won 284
# The remaining 118 were stalemates