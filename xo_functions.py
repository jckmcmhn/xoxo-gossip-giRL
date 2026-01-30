import random
import numpy as np
import pandas as pd
import copy
from time import sleep

columns = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]

def check_for_winner(b, tt):
    """
    Docstring for check_for_winner
    
    :param b: The current board (state)
    :param tt: Turns taken up to now
    """
    if tt < 4: # No one can win before the fifth move, if tt is 4 we're assessing the 5th #TODO: c'mon now...
        return 0, ""
    if sum(b[0]) in [-3,3]: # is the first row a winner
        return 1, "r1"
    elif sum(b[1]) in [-3,3]: # is the second row a winner
        return 1, "r2"
    elif sum(b[2]) in [-3,3]: # is the third row a winner
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
            return 2, "s" # draw
        else:
            return 0, ""
    
def make_move(p, b, mr, mc, tt, debug = False):
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
    status, description = check_for_winner(b,tt)
    return b, status, description
    
#print("To create a new board where the first player has taken the top left corner, run b, status = make_move(-1,[[0,0,0],[0,0,0],[0,0,0]],0,0)")

def get_possible_moves(b):
    possible_moves = []
    for ir, row in enumerate(b):
        for ic, row_x_column in enumerate(row):
            if row_x_column == 0:
                possible_moves.append((ir,ic))
    return possible_moves

def make_player_move(p,b,m,tt):
    map = {"a1": "00", "a2": "01", "a3": "02", "b1": "10", "b2": "11", "b3": "12", "c1": "20", "c2": "21", "c3": "22"}
    m = map[m]
    mr, mc = int(m[0]), int(m[1])
    b, status, description = make_move(p, b, mr, mc, tt)
    return b, status

def make_computer_move(p,b,tt):
    pm = get_possible_moves(b)
    m = random.choice(pm)
    print(f"Computer's move is {m}")
    b, status, description = make_move(p,b,m[0],m[1],tt)
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

def prettify_boards(boards):
    """
    Docstring for prettify_boards
    
    :param boards: Should be a list of stringified states
    """
    map = {-1: "X", 1: "O", 0: " "}
    print("")
    vert = " ----------- "
    top_row = ""
    for i in boards:
        top_row = top_row + "   " + vert
    print(top_row)
    for i in [0,1,2]:
        row = ""
        for board in boards:
            board_row = eval(board)[i]
            string = f"| {map[board_row[0]]} | {map[board_row[1]]} | {map[board_row[2]] } |"
            row = row + " * " + string
        print(row)
    bottom_row = ""
    for i in boards:
        bottom_row = bottom_row + "   " + vert
    print(bottom_row)
    print("")

class Player:
    def greet(self):
        # We love anthropomorphising the computer, don't we?
        if self.name.startswith("Al"):
            print("\bYou can call me Al")
        else:
            print(f"\nHello, my name is {self.name}.")
        if self.mode.startswith("LEARNING"):
            print(f"I'm an agent in this Reinforcement mode scenario and I learn as I play the game.")
            
            if self.mode == "LEARNING_DEMO":
                print("I save my updated model to disk at the end of every episode for demonstration purposes. This could be quite slow on your computer")
        elif self.mode == "FIXED":
            print(f"I used to be an agent. I learned how to play the game across #TODO episodes.")
            print(f"I REFUSE TO LEARN ANYTHING ELSE!")
            print(f"My model is stored in this location: {self.file} and has {len(self.model_df)} rows.\n")
        elif self.mode.startswith("RULES_IMPERFECT"):
            print(f"I play the game based on a set of simple, fixed rules. My algorithm is 'imperfect'—that is, it won't make 'perfect' moves every time.") # It uses an em-dash because it's technically ai, do you get it? Well? Do you?
            if self.mode.endswith("NOT_LOCKED_IN"):
                print("That said, I'm not really paying attention.")

    def __init__(self, name, file, mode, epsilon = 70, rewards = [0,0,0]):
        self.name = name
        self.file = file
        self.model_df = pd.read_csv(self.file)
        self.model_df.columns = ["state"] + columns
        self.mode = mode
        self.reward_win = rewards[0]
        self.reward_lose = rewards[1]
        self.reward_draw = rewards[2]
        self.epsilon = epsilon # 70

        # The following attributes accumulate over multiple episodes, so it makes sense to set them at player init
        self.wins = 0
        self.wins_as_x = 0
        self.wins_as_o = 0
        self.tt_wins = []
        self.draws = 0
        self.draws_as_x = 0
        self.draws_as_o = 0
        self.greet()

    def make_rules_based_move(self,b,tt,p,locked_in = True):
        # A player that isn't locked in will still always take winning moves, but any moves taken before that may be at random
        # This is to try and simulate a human player who knows how the game works but isn't really paying attention. Maybe they're on their phone?
        pm = get_possible_moves(b)
        m = random.choice(pm) # This is the default move. The following if clause will determine if this gets updated
        m = str(m[0]) + str(m[1])
        if not locked_in:
            looking_at_phone = random.choice([True, False])
        else:
            looking_at_phone = False
        if tt >= 4: # Four moves have been played. After this point it's possible to win
            # The model does this regardless of whether it's locked in
            for m4 in pm: # Don't overwrite the default m from the top of the function yet
                mr, mc = m4[0], m4[1]
                spec_b = copy.deepcopy(b)
                spec_b[mr][mc] = p
                status, description = check_for_winner(spec_b, tt)
                if status:
                    m = str(m[0]) + str(m[1])
                    break
        if not looking_at_phone:
            if tt == 0: # This means it's X's first turn
                m = "00"
            elif tt == 1: # It's Y's first turn
            # This isn't quite right, it should be if X took a corner, take the middle, if X took the middle take a corner, if X took an "edge" (the points on a plus sign) TBD
                if b == [[0,0,0],[0,-1,0],[0,0,0]]: # if X took the middle
                    m = "00"
                elif b in [[[-1,0,0],[0,0,0],[0,0,0]], [[0,0,-1],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[-1,0,0]], [[0,0,0],[0,0,0],[0,0,-1]]]: # X took a corner
                    m = "11"
     
        mr, mc = int(m[0]), int(m[1])
        b, status, description = make_move(p,b,mr,mc,tt)
        return b, status, description, m
    
    def use_learning_table(self):
        """
        if self.mode.startswith("L"):
            check = random.randint(0,100)
            print(self.epsilon)
            if check <= self.epsilon:
                print("would use model here")
        else:
            return 1 == random.choice([1,0,0,0,0,0])
        """
        return 1 == random.choice([1,0,0,0,0,0]) # FOR TESTING

    def make_model_move(self,b,tt,p):
        #print(f"Turns taken so far {tt}")
        #print(f"Making decision for state: {b}")
        choice = self.use_learning_table() # TODO: Define this function properly
        if choice: # Need episode to be available here, not tt
            #print("Making a random choice")
            pm = get_possible_moves(b)
            m = random.choice(pm)
            mr, mc = int(m[0]), int(m[1])
            m = str(m[0]) + str(m[1])
        else:
            hits = self.model_df[self.model_df["state"] == str(b)][columns]
            hits = hits.transpose()
            hits.columns = ["values"]
            hits = hits.reset_index()
            max_value = np.nanmax(hits["values"]) # seems bizzare to have to do this, but if the first value is nan then regular max screws up
            top_answers = hits[hits["values"] == max_value]
            m = str(random.choice(list(top_answers["index"])))
            mr, mc = int(m[0]), int(m[1])
            #print(f"{self.name}'s move is {m}")

        b, status, description = make_move(p,b,mr,mc,tt)
        self.epsilon -= 0.001
        return b, status, description, m
    
    def make_agent_move(self,b,tt,p):
        if self.mode in ["LEARNING", "LEARNING_DEMO", "FIXED"]:
            return self.make_model_move(b,tt,p)
        elif self.mode.startswith("RULES_IMPERFECT"):
            if self.mode.endswith("NOT_LOCKED_IN"):
                return self.make_rules_based_move(b,tt,p)
            else:
                return self.make_rules_based_move(b,tt,p,False)
    
    def update_model(self, status, tt):
        actions_states = list(zip(self.actions, self.states))
        actions_states.reverse()
        reward_left = [self.reward_lose, self.reward_win, self.reward_draw][status]
        positive_reinforcement = reward_left > 0

        for i, reinforce_action in enumerate(self.actions):
            # reinforce_action so named to distinguish from actions which aren't necessarily to be reinforced
            reinforce_state = self.states[i]
            #before = self.model_df[self.model_df["state"] == str(reinforce_state)][reinforce_action]
            self.model_df.loc[self.model_df['state'] == str(reinforce_state), reinforce_action] += reward_left
            #after = self.model_df[self.model_df["state"] == str(reinforce_state)][reinforce_action]
            if self.mode == "LEARNING_DEMO":
                self.model_df.to_csv(self.file, index = False) # This will be a bit slow, but will make a cool visual
                # if you can watch the csv update in real time
                sleep(0.2) # Have to give your PC time to read the new file
            if positive_reinforcement & (reward_left <= 0):
                break
            if (not positive_reinforcement) & (reward_left >= 0):
                break


