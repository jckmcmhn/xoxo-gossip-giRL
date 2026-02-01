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
        player.update_policy(status, tt)
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
        x_player_m, o_player_m, x_player_s, o_player_s = [], [], [], []

        p1.actions, p1.states, p2.actions, p2.states = [], [], [], []
        turn_end_states = []

        if log_level != 0:
            print(f"----------------------------------")
            print(f"Episode {episode + 1}: {x_player.name} is X and {o_player.name} is O")

        state = [[0,0,0],[0,0,0],[0,0,0]]
        status = 0
        tt = 0
        while status == 0 and tt != 9:
            if x_player.name == p1.name:
                p1.states.append(state) #TODO: what is this for?
            x_player.states.append(str(state)) # HAS TO BE A STRING, 
            x_player_s.append(state)
            x_turn = True
            state, status, description, m = x_player.make_agent_action(state,tt,-1)
            tt += 1
            x_player_m.append(m)
            x_player.actions.append(m)
            if demo_mode:
                print(f"{x_player.name}'s turn.")
                prettify_board(state)
                sleep(delay * 0.5)
            #print(f"After this most recent action: b is {b}, status is {status} and tt is {tt}")
            turn_end_states.append(str(state))
            if status == 0 and tt != 9:
                o_player.states.append(str(state))
                o_player_s.append(state)
                x_turn = False
                state, status, description, m = o_player.make_agent_action(state,tt,1)
                tt += 1
                o_player_m.append(m)
                o_player.actions.append(m)
                if demo_mode:
                    print(f"{o_player.name}'s turn.")
                    prettify_board(state)
                    sleep(delay * 0.5)
                #print(f"After this most recent action: state is {state}, status is {status} and tt is {tt}")
                turn_end_states.append(str(state))
        if status == 1: # someone won
            if x_turn: # X won
                if log_level != 0:
                    print(f"This game is over. X won.\n")
                winning_player = x_player
                x_wins += 1
                x_player = update_player_objects(x_player, 1, tt, log_level) # tell X that they won
                o_player = update_player_objects(x_player, 0, tt, log_level) # tell O that they lost
            else: # O won
                if log_level != 0:
                    print(f"This game is over. O won.\n")
                winning_player = o_player
                o_wins += 1
                o_player = update_player_objects(o_player, 1, tt, log_level) # Tell O they won
                x_player = update_player_objects(x_player, 0, tt, log_level) # Tell X they lost
        if status == 2: # Draw
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
            prettify_board(state)
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

    if p2.wins != 0:
        headline = f"{p1.name} won {p1.wins} times. {p2.name} won {p2.wins} times. P1 won {p1.wins / p2.wins} more times than {p2.name}. There were {draws} ({round(100 * draws / n, 2)}%) draws"
        print(f"\n{headline}")
    else:
        headline = f"{p1.name} won {p1.wins} times. {p2.name} did not win once. There were {draws} ({round(100 * draws / n, 2)}%) draws" 
        print(f"\n{headline}")        

    if (n > 10) and (p1.mode.startswith("L")):
        print("Here is the first few states of the p1 policy at the end of training.")
        print("\nAssuming you're training a policy to do well, if one of 00, 02, 20 or 22 is not the highest value for the top row, we're in trouble")      
        print(p1.policy_df[0:4])
        print(f"\nUpdating file {p1.out_file}")
        p1.policy_df.to_csv(p1.out_file, index = False)
        sign_off = p1.sign_off()
        if sign_off is not None:
            headline = headline + "\n" + sign_off

    if p2.mode.startswith("LEARNING"):
        print("p2 policy at end of training: ")
        print(p2.policy_df)
    return(p1.wins, p2.wins, draws, headline)