import random
import numpy as np
import pandas as pd

columns = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]

def check_for_winner_v2(b, tt):
    """
    Docstring for check_for_winner
    
    :param b: The current board (state)
    :param tt: Turns taken up to now
    """
    if tt < 4: # No one can win before the fifth move, if tt is 4 we're assessing the 5th #TODO: c'mon now...
#        print("stopping check early")
        return 0, ""
#    print("Doing rest of check")
    if sum(b[0]) in [-3,3]: # is the first row a winner
#        print("r1")
        return 1, "r1"
    elif sum(b[1]) in [-3,3]: # is the second row a winner
#        print("r2")
        return 1, "r2"
    elif sum(b[2]) in [-3,3]: # is the third row a winner
#        print("r3")
        return 1, "r3"
    elif (b[0][0] + b[1][0] + b[2][0]) in [-3,3]: # is the first column a winning column
        return 1, "c1"
    elif (b[0][1] + b[1][1] + b[2][1]) in [-3,3]: # is the second column a winner
        return 1, "c2"
    elif (b[0][2] + b[1][2] + b[2][2]) in [-3,3]: # is the third column a winner
        return 1, "r3"
    elif (b[0][0] + b[1][1] + b[2][2]) in [-3,3]: # is the top left to bottom right diagonal a winner
        return 1, "d1"
    elif (b[0][2] + b[1][1] + b[2][0]) in [-3,3]: # is the bottom left to top right diagonal a winner
        return 1, "d2"
    else:
        if tt == 8: #See TODO above
            print("STALEMATE")
            return 2, "s" # Stalemate
        else:
            return 0, ""
    
def check_for_winner(b):
    """
    Legacy function
    Docstring for check_for_winner
    Delete this duplicate once all scripts that rely on check_for_winner returning a boolean are fixed
    
    :param b: The current board (state)
    """
    if sum(b[0]) in [-3,3]: # is the first row a winner
        return True
    elif sum(b[1]) in [-3,3]: # is the second row a winner
        return True
    elif sum(b[2]) in [-3,3]: # is the third row a winner
        return True
    elif (b[0][0] + b[1][0] + b[2][0]) in [-3,3]: # is the first column a winning column
        return True
    elif (b[0][1] + b[1][1] + b[2][1]) in [-3,3]: # is the second column a winner
        return True
    elif (b[0][2] + b[1][2] + b[2][2]) in [-3,3]: # is the third column a winner
        return True
    elif (b[0][0] + b[1][1] + b[2][2]) in [-3,3]: # is the top left to bottom right diagonal a winner
        return True
    elif (b[0][2] + b[1][1] + b[2][0]) in [-3,3]: # is the bottom left to top right diagonal a winner
        return True
    else:
        return False

def make_move_v2(p, b, mr, mc, tt, debug = False):
    """
    Docstring for make_move
    
    :param p: Player, either -1 (x) or 1 (o)
    :param b: The current board. At the start of the game the board will be [[0,0,0],[0,0,0],[0,0,0]]
    :param mr: The row of the square the current player wants to take
    :param mc: The column of the square the current player wants to take
    :param debug: Description
    """
    if (not debug) and b[mr][mc] != 0:
        raise ValueError("Invalid move. That square has already been taken.")
    b[mr][mc] = p
    status, description = check_for_winner_v2(b,tt)
    return b, status, description

def make_move(p, b, mr, mc, debug = False):
    """
    Docstring for make_move
    
    :param p: Player, either -1 (x) or 1 (o)
    :param b: The current board. At the start of the game the board will be [[0,0,0],[0,0,0],[0,0,0]]
    :param mr: The row of the square the current player wants to take
    :param mc: The column of the square the current player wants to take
    :param debug: Description
    """
    if (not debug) and b[mr][mc] != 0:
        raise ValueError("Invalid move. That square has already been taken.")
    b[mr][mc] = p
    status = check_for_winner(b)
    return b, status
    
#print("To create a new board where the first player has taken the top left corner, run b, status = make_move(-1,[[0,0,0],[0,0,0],[0,0,0]],0,0)")

def get_possible_moves(b):
    possible_moves = []
    for ir, row in enumerate(b):
        for ic, row_x_column in enumerate(row):
            if row_x_column == 0:
                possible_moves.append((ir,ic))
    return possible_moves

def make_player_move(p,b,m):
    mr, mc = m.split(",")
    mr, mc = int(mr), int(mc)
    b, status = make_move(p, b, mr, mc)
    return b, status

def make_computer_move(p,b):
    pm = get_possible_moves(b)
    m = random.choice(pm)
    print(f"Computer's move is {m}")
    b, status = make_move(p,b,m[0],m[1])
    return b, status

def prettify_board(b):
    map = {-1: "X", 1: "O", 0: " "}
    print("")
    vert = " -----------" 
    print(vert)
    for row in b:
        new = f"| {map[row[0]]} | {map[row[1]]} | {map[row[2]] } |"
        print(new)
        print(vert)
    print("")

class Player:
    def __init__(self, name, file, learning):
        self.name = name
        self.file = file
        self.model_df = pd.read_csv(self.file)
        self.model_df.columns = ["state"] + columns
        self.learning = learning
        self.wins = 0
        self.wins_as_x = 0

    def greet(self):
        if self.learning:
            print(f"Hello, my name is {self.name}. I'm an agent in this Reinforcement Learning scenario and I learn as I play the game.")
            print(f"My model has {len(self.model_df)} rows")
        else:
            print(f"Hello, my name is {self.name}. I used to be an agent. I learned how to play the game across #TODO episodes.")
            print(f"I REFUSE TO LEARN ANYTHING ELSE!")
        print(f"My model is stored in this location {self.file}.\n")

    def make_model_move(self,b,tt,p):
        #print(f"Turns taken so far {tt}")
        #print(f"Making decision for state: {b}")
        choice = random.choice([0,1])
        if (choice == 0): # Need episode to be available here, not tt
            print("Making a random choice")
            pm = get_possible_moves(b)
            m = random.choice(pm)
            mr, mc = int(m[0]), int(m[1])
            m = str(m[0]) + str(m[1])
        else:
            # Using model choice
            print("Using the model's preferred choice")
            hits = self.model_df[self.model_df["state"] == str(b)][columns]#.head(1)
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