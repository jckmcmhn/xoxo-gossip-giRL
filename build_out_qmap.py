from xo_functions import determine_legal_moves, check_for_winner
import re
import pandas as pd

remove = "[\[\]\, \(\)]"
def create_name(state):
    return re.sub(remove, "", str(state)) #TODO: is this more performant than just doing a lot of .replace statements

init = [[0,0,0],[0,0,0],[0,0,0]]
possible_states = [[init]]
previous_states = [init]

cols = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]
df = pd.DataFrame(columns = cols)
new_rows = []

i = 0
# how many possible "start of turn" states are there
for turn in range(0,9):
    turn += 1
    if turn % 2 == 0:
        p = 1
    else:
        p = -1
    print(f"Turn {turn}. Player {p}")
    new_states = []
    for starting_state in previous_states:
        print(f"State: {i}", end='\r')
        i += 1
        new_row = pd.DataFrame(columns = cols, index = [str(starting_state)])
        actions = determine_legal_moves(starting_state)
        for action in actions:
            action_str = create_name(action)
            new_row[action_str] = [0]
            new_state = [row[:] for row in starting_state] # Thank you, random redditor, for your help here
            #https://www.reddit.com/r/learnpython/comments/1imbmpo/changing_one_variable_automatically_changes/
            new_state[action[0]][action[1]] = p
            if check_for_winner(new_state) is False: # If it is a winning move, the game is over, we don't need to take this branch further
                new_states.append(new_state)
        new_rows.append(new_row)
    possible_states.append(new_states)
    previous_states = new_states

possible_states_flat = []
for possible_state_list in possible_states:
    for possible_state in possible_state_list:
        possible_states_flat.append(possible_state)

print(f"Length of new_rows: {len(new_rows)}")
df = pd.concat(new_rows) # TODO: confirm new index
print(df)

print(f"Length of possible_states_flat: {len(possible_states_flat)}") # This was 986410 before pruning out winning games
#340858
print(f"Length of df: {len(df)}")

df.to_csv("qmap.csv")

print("----------------")


#for s in possible_states_flat:
#    if str(s) not in df.index:
#        print(s)