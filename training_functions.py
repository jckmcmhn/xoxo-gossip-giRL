from xo_functions import prettify_board, prettify_boards, columns
import statistics
from time import sleep

# Should this script really be called "training_and_evaluation_functions.py"? Maybe....

def update_player_objects(player, status, tt, log_level = 1):
    if status == 1: # Win
        winner = player.name
        player.tt_wins.append(tt)
        if log_level > 1:
            print(f"{winner} (playing as {player.playing_as_str}) won.\n")
        player.wins += 1
        if player.playing_as_str == "X":
            player.wins_as_x += 1
        else:
            player.wins_as_o += 1
    if status == 2:
        player.draws += 1
        if player.playing_as_str == "X":
            player.draws_as_x += 1
        else:
            player.draws_as_o += 0
    
    if player.mode.startswith("LEARNING"):
        player.update_model(status, tt)
    return player #todo, is this necessary?


def run_training_loop(p1, p2, n, alternate_x = "ALTERNATE", log_level = 3):
    # log levels: 0 = None, 1 = Minimal, 3 = Normal, 4 = ? 5 = Maximum

    delay = 0.1 #TODO: Should be an argument and parameter
    demo_mode = False #TODO: Should be an argument and parameter
    x_wins, o_wins, draws = 0, 0, 0
    
    for episode in range(0,n):

        # The following attributes and counters are relevant only to this episode. It would not make sense to set them at Player init
        if alternate_x == "ALTERNATE":
            if 0 == episode % 2: # alternate who goes first
                x_player, o_player = p1, p2
                p1.playing_as_str, p2.playing_as_str = "X", "O"
            else:
                x_player, o_player = p2, p1
                p1.playing_as_str, p2.playing_as_str = "O", "X"
        elif alternate_x == "P1":
            x_player, o_player = p1, p2
            p1.playing_as_str, p2.playing_as_str = "X", "O"
        elif alternate_x == "P2":
            x_player, o_player = p2, p1
            p1.playing_as_str, p2.playing_as_str = "O", "X"
        else:
            raise ValueError("Invalid alternate_x value")
        x_player_m, o_player_m, x_player_b, o_player_b = [], [], [], []

        p1.actions, p1.states, p2.actions, p2.states = [], [], [], []
        turn_end_states = []

        if log_level != 0:
            print(f"----------------------------------")
            print(f"Episode {episode + 1}: {x_player.name} is X and {o_player.name} is O")

        b = [[0,0,0],[0,0,0],[0,0,0]]
        status = 0
        tt = 0
        while status == 0 and tt != 9:
            if x_player.name == p1.name:
                p1.states.append(b)
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
        if status == 1:
            if x_turn:
                if log_level != 0:
                    print(f"This game is over. X won.\n")
                winning_player = x_player
                x_wins += 1
                x_player = update_player_objects(x_player, status, tt, log_level)
            else:
                if log_level != 0:
                    print(f"This game is over. O won.\n")
                winning_player = o_player
                o_wins += 1
                o_player = update_player_objects(o_player, status, tt, log_level)
        if status == 2:
            if log_level != 0:
                print("It was a draw")
            draws += 1
            x_player = update_player_objects(x_player, status, tt, log_level)
            o_player = update_player_objects(o_player, status, tt, log_level)
        
        
        if log_level == 5:
            print(f"Here is {winning_player.name}'s winning game summary.\n")
            prettify_boards(turn_end_states)
        if demo_mode:
            print("Final board")
            prettify_board(b)
            sleep(delay * 1.5)

    print(f"\nX wins: {x_wins} ({round(100 * x_wins / n, 2)}%)")
    print(f"O wins: {o_wins} ({round(100 * o_wins / n, 2)}%)")
    print(f"Draws: {draws} ({round(100 * draws / n, 2)}%)")
    if p1.wins != 0:
        print(f"\n{p1.name} total wins: {p1.wins}. Of those, {p1.wins_as_x} ({round(100 * p1.wins_as_x / p1.wins, 2)}%) were as X.")
        print(f"{p1.name} total losses: {n - p1.wins - draws}.")
        print(f"For games where {p1.name} won, the average number of turns taken in winning games was {statistics.mean(p1.tt_wins)}, the max was {max(p1.tt_wins)} and the min was {min(p1.tt_wins)}")
    else:
        print(f"\n{p1.name} total wins: 0")
    if p2.wins != 0:
        print(f"\n{p2.name} total wins: {p2.wins}. Of those, {p2.wins_as_x} ({round(100 * p2.wins_as_x / p2.wins, 2)}%) were as X.")
        print(f"{p2.name} total losses: {n - p2.wins - draws}.")
        print(f"For games where {p2.name} won, the average number of turns taken in winning games was {statistics.mean(p2.tt_wins)}, the max was {max(p2.tt_wins)} and the min was {min(p2.tt_wins)}")
    else:
        headline = f"{p2.name} total wins: 0" 
        print(f"\n{headline}")

    if p2.wins != 0:
        headline = f"{p1.name} won {p1.wins / p2.wins} more times than {p2.name}"
        print(f"\n{headline}")

    if (n > 10) and (p1.mode.startswith("LEARNING")):
        print("Here is the first few states of the p1 model at the end of training.")
        print("\nAssuming you're training a model to do well, if one of 00, 02, 20 or 22 is not the highest value for the top row, we're in trouble")      
        print(p1.model_df[0:4])
        print(f"\nUpdating file {p1.out_file}")
        p1.model_df.to_csv(p1.out_file, index = False)

    if p2.mode.startswith("LEARNING"):
        print("p2 model at end of training: ")
        print(p2.model_df)
    return(p1.wins, p2.wins, draws, headline)