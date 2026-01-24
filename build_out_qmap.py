from xo_functions import determine_legal_moves, check_for_winner
import re
import pandas as pd

remove = "[\[\]\, \(\)]"
def create_name(state):
    return re.sub(remove, "", str(state))

init = [[0,0,0],[0,0,0],[0,0,0]]
possible_states = [[init]]
previous_states = [init]
#possible_actions = []

cols = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]
df = pd.DataFrame(columns = cols)
new_rows = []

# how many possible "start of turn" states are there
for turn in [1,2,3,4]:#,5,6,7,8,9]:
    if turn % 2 == 0:
        p = 1
    else:
        p = -1
    print(f"Turn {turn}. Player {p}")
    new_states = []
    for starting_state in previous_states:
        new_row = pd.DataFrame(columns = cols, index = [str(starting_state)])
        actions = determine_legal_moves(starting_state)
        #action_strings = [ create_name(action) for action in actions]
        #possible_actions.append(action_strings)
        for action in actions:
            action_str = create_name(action)
            new_row[action_str] = [0]


            new_state = [row[:] for row in starting_state] # Thank you, random redditor, for your help here
            #https://www.reddit.com/r/learnpython/comments/1imbmpo/changing_one_variable_automatically_changes/
            new_state[action[0]][action[1]] = p
            if check_for_winner(new_state) is False: # If it is a winning move, the game is over, we don't need to take this branch further
                new_states.append(new_state)
        #print(new_row)
        #df = pd.concat([df, new_row]) # TODO: confirm new index
        new_rows.append(new_row)
    possible_states.append(new_states)
    previous_states = new_states

possible_states_flat = []
for possible_state_list in possible_states:
    for possible_state in possible_state_list:
        possible_states_flat.append(possible_state)
print(len(possible_states_flat)) # This was 986410 before pruning out winning games
#340858

df = pd.concat(new_rows) # TODO: confirm new index
print(df)

row_names = []
for state in possible_states_flat:
    row_name = str(state)
    row_names.append(row_name)

cols = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]


exit()
df = pd.DataFrame(columns = cols, index = row_names)
print(df)

print(possible_actions[0])
print(possible_actions[1])
print(len(possible_actions))
print(len(possible_states_flat))

#for ps in possible_states_flat
