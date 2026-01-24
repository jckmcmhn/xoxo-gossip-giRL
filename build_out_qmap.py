from xo_functions import get_possible_moves, check_for_winner
import re
import pandas as pd

remove = "[\[\]\, \(\)]"
def create_name(state):
    return re.sub(remove, "", str(state)) #TODO: is this more performant than just doing a lot of .replace statements

init = [[0,0,0],[0,0,0],[0,0,0]]
possible_states = [[init]]
previous_states = [init]
possible_action_count = 0


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
        actions = get_possible_moves(starting_state)
        for action in actions:
            possible_action_count += 1
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

print(f"Length of new_rows: {len(new_rows)}") # 294,778
df = pd.concat(new_rows)
print(df)
df.to_csv("qmap.csv")

### Everything below this point was part of an approach which in the end was not necessary
possible_states_flat = []
for possible_state_list in possible_states:
    for possible_state in possible_state_list:
        possible_states_flat.append(possible_state)

print(f"Length of possible_states_flat: {len(possible_states_flat)}") # This was 986,410 before pruning out winning games
#Now it is 340,858

print(f"Number of possible actions to train for: {possible_action_count}") # 549,945
# The length of df and the number of possible states does not match.
# This is because the list of states include winning and end states which do not appear in df.