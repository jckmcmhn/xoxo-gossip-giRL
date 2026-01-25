import argparse
from xo_functions import prettify_board, Player
from time import sleep

delay = 0.7 #TODO: Should be an argument
demo_mode = False #TODO: Should be an argument

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

p1 = Player("Rolf",file,True)
p2 = Player("Gregg",file,False)
p1.greet()
p2.greet()

x_player_wins = 0
o_player_wins = 0
stalemates = 0
for episode in range(0,n):
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

    print(f"-----------------")
    print(f"Episode {episode + 1}: {x_player.name} is X and {o_player.name} is O")

    b = [[0,0,0],[0,0,0],[0,0,0]]
    status = 0
    tt = 0
    while status == 0 and tt != 9:
        x_turn = True
        b, status, description, m = x_player.make_model_move(b,tt,-1)
        tt += 1
        x_player_m.append(m)
        x_player_b.append(b)
        if demo_mode:
            print(f"{x_player.name}'s turn.")
            prettify_board(b)
            sleep(delay * 0.5)
        #print(f"After this most recent move: b is {b}, status is {status} and tt is {tt}")
        if status == 0 and tt != 9: # I'd forgotten this check at first.
            #Interestingly, when the players just picked at random, it always took up to the 7 turns taken for this to become a problem
            x_turn = False
            b, status, description, m = o_player.make_model_move(b,tt,1)
            tt += 1
            o_player_m.append(m)
            o_player_b.append(b)
            if demo_mode:
                print(f"{o_player.name}'s turn.")
                prettify_board(b)
                sleep(delay * 0.5)
            #print(f"After this most recent move: b is {b}, status is {status} and tt is {tt}")
    print(f"This game is over\n")
    if status == 1:
        if x_turn:
            print(f"{x_player.name} (playing as X) won.\n")
            if not demo_mode:
                prettify_board(b)
            x_player_wins += 1
            x_player.wins += 1
            x_player.wins_as_x += 1
            #print(x_player_m)
            #print(x_player_b)
        else:
            print(f"{o_player.name} (playing as O) won.\n")
            if not demo_mode:
                print("Final board")
                prettify_board(b)
            o_player_wins += 1
            o_player.wins += 1
    if status == 2:
        print("It was a stalemate")
        stalemates += 1
    if demo_mode:
        sleep(delay * 1.5)

print(f"\nX wins: {x_player_wins}")
print(f"O wins: {o_player_wins}")
print(f"Stalemates: {stalemates}")
if p1.wins != 0:
    print(f"\n{p1.name} total wins: {p1.wins}. Of those, {p1.wins_as_x} ({round(100 * p1.wins_as_x / p1.wins, 2)}%) were as X.")
else:
    print(f"\n{p1.name} total wins: 0")
if p2.wins != 0:
    print(f"{p2.name} total wins: {p2.wins}. Of those, {p2.wins_as_x} ({round(100 * p2.wins_as_x / p2.wins, 2)}%) were as X.")
else:
    print(f"\n{p2.name} total wins: 0")