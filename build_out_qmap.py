from xo_functions import determine_legal_moves, check_for_winner

init = [[0,0,0],[0,0,0],[0,0,0]]
possible_states = []
previous_states = [init]

# how many states are there
# for turn in [2,3]:#,4,5,6,7,8,9]:
for turn in [1,2,3,4,5,6,7,8,9]:
    if turn % 2 == 0:
        p = 1
    else:
        p = -1
    print(f"Turn {turn}. Player {p}")
    new_states = []
    for starting_state in previous_states:
        #print(f"Starting state: {starting_state}")
        legal_moves = determine_legal_moves(starting_state)
        for lm in legal_moves:
            #print(f"Move {lm}")
            new_state = [row[:] for row in starting_state] # Thank you, random redditor, for your help here
            #https://www.reddit.com/r/learnpython/comments/1imbmpo/changing_one_variable_automatically_changes/
            new_state[lm[0]][lm[1]] = p
            if check_for_winner(new_state) is False: # If it's a winning move, the game is over, we don't need to take this branch further
            #print(new_state)
                new_states.append(new_state)
    #print(new_states)
    possible_states.append(new_states)
    previous_states = new_states
#print(possible_states)
print(len(possible_states))
print(len(possible_states[0]))
print(len(possible_states[1]))
possible_states_flat = []
for possìble_state_list in possible_states:
    for possible_state in possìble_state_list:
        possible_states_flat.append(possible_state)
print(len(possible_states_flat)) # This was 986409 before pruning out winning games
