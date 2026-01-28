import argparse
from xo_functions import prettify_board, prettify_boards, Player, columns
from time import sleep

delay = 0.1 #TODO: Should be an argument
demo_mode = False #TODO: Should be an argument
print_vertical_only = True

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
reward_win, reward_lose, reward_draw = float(reward_win), float(reward_lose), float(reward_draw)

is_p2_learning = False
#p1 = Player("Tom (P1)",file,"LEARNING_DEMO", reward_win)
#p1 = Player("Tom (P1)",file,"LEARNING", reward_win)
p1 = Player("Tom (P1)",file,"NOT_LEARNING", reward_win) # Static trained model
#p2 = Player("Gregg (P2)","blank_q_learning_table.csv","NOT_LEARNING")
p2 = Player("Al (P2)",file,"RULES_IMPERFECT")
p1.greet()
p2.greet()

x_wins, o_wins = 0, 0 # These are wins for X or O
stalemates = 0
for episode in range(0,n):
    if 0 == episode % 2: # alternate who goes first
        x_player, o_player = p1, p2
    else:
        x_player, o_player = p2, p1
    x_player_m, o_player_m, x_player_b, o_player_b = [], [], [], []
    
    p1.actions, p1.states, p2.actions, p2.states = [], [], [], []
    p1_actions, p1_states, p2_actions, p2_states = [], [], [], []
    turn_end_states = []

    print(f"----------------------------------")
    print(f"Episode {episode + 1}: {x_player.name} is X and {o_player.name} is O")
    print(p1.actions)

    b = [[0,0,0],[0,0,0],[0,0,0]]
    status = 0
    tt = 0
    while status == 0 and tt != 9:
        if x_player.name == p1.name:
            p1_states.append(b)
        x_player.states.append(str(b)) # HAS TO BE A STRING, 
        x_player_b.append(b)
        x_turn = True
        b, status, description, m = x_player.make_agent_move(b,tt,-1)
        tt += 1
        x_player_m.append(m)
        x_player.actions.append(m)
        if demo_mode:
            print(f"{x_player.name}'s turn.")
            prettify_board(b)
            sleep(delay * 0.5)
        #print(f"After this most recent move: b is {b}, status is {status} and tt is {tt}")
        turn_end_states.append(str(b))
        if status == 0 and tt != 9:
            o_player.states.append(str(b))
            o_player_b.append(b)
            x_turn = False
            b, status, description, m = o_player.make_agent_move(b,tt,1)
            tt += 1
            o_player_m.append(m)
            o_player.actions.append(m)
            if demo_mode:
                print(f"{o_player.name}'s turn.")
                prettify_board(b)
                sleep(delay * 0.5)
            #print(f"After this most recent move: b is {b}, status is {status} and tt is {tt}")
            turn_end_states.append(str(b))
    print(f"This game is over\n")
    if status == 1:
        if x_turn:
            print(f"{x_player.name} (playing as X) won.\n")
            if not demo_mode:
                prettify_board(b)
            x_wins += 1
            x_player.wins += 1
            x_player.wins_as_x += 1
            winner = x_player.name

        else:
            print(f"{o_player.name} (playing as O) won.\n")
            if not demo_mode:
                print("Final board")
                prettify_board(b)
            o_wins += 1
            o_player.wins += 1
            winner = o_player.name



        # For now, let's take it that p1 is always the one we want to learn
        if winner == p1.name: #TODO: c'mon man
            # TODO training here
            #print(f"Here is {p1.name}'s winning game summary.\n")
            if print_vertical_only is False:
                prettify_boards(turn_end_states)
            p1.update_model()

    if status == 2:
        print("It was a stalemate")
        stalemates += 1
    if demo_mode:
        sleep(delay * 1.5)

print(f"\nX wins: {x_wins}")
print(f"O wins: {o_wins}")
print(f"Stalemates: {stalemates}")
if p1.wins != 0:
    print(f"\n{p1.name} total wins: {p1.wins}. Of those, {p1.wins_as_x} ({round(100 * p1.wins_as_x / p1.wins, 2)}%) were as X.")
else:
    print(f"\n{p1.name} total wins: 0")
if p2.wins != 0:
    print(f"{p2.name} total wins: {p2.wins}. Of those, {p2.wins_as_x} ({round(100 * p2.wins_as_x / p2.wins, 2)}%) were as X.")
else:
    print(f"\n{p2.name} total wins: 0")

print(f"\n{p1.name} won {p1.wins / p2.wins} more times than {p2.name}")



if (n > 10) and (p1.mode == "LEARNING"):
    print("\nIf 00, 02, 20 or 22 is not the highest value here, we're in trouble")
    print(p1.model_df.iloc[0][columns])

    print("Here is the first few states of the p1 model at the end of training: ")
    print(p1.model_df[0:5])
    print(f"\nUpdating file {file}")
    p1.model_df.to_csv(file, index = False)

if is_p2_learning:
    print("p2 model at end of training: ")
    print(p2.model_df) # This should show all zeroes