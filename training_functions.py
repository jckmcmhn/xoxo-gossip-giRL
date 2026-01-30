from xo_functions import prettify_board, prettify_boards, columns
from time import sleep

# Should this script really be called "training_and_evaluation_functions.py"? Maybe....

def run_training_loop(p1, p2, n, epsilon, alternate_x = "YES", log_level = "NORMAL"):
    delay = 0.1 #TODO: Should be an argument and parameter
    demo_mode = False #TODO: Should be an argument and parameter
    print_vertical_only = True

    x_wins, o_wins, draws = 0, 0, 0
    
    for episode in range(0,n):
        if alternate_x == "YES":
            if 0 == episode % 2: # alternate who goes first
                x_player, o_player = p1, p2
            else:
                x_player, o_player = p2, p1
        elif alternate_x == "P1":
            x_player, o_player = p1, p2
        elif alternate_x == "P2":
            x_player, o_player = p2, p1
        else:
            raise ValueError("Invalid alternate_x value")
        x_player_m, o_player_m, x_player_b, o_player_b = [], [], [], []

        p1.actions, p1.states, p2.actions, p2.states = [], [], [], []
        turn_end_states = []

        print(f"----------------------------------")
        print(f"Episode {episode + 1}: {x_player.name} is X and {o_player.name} is O")
        print(p1.actions)

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
        print(f"This game is over\n")
        if status == 1:
            if x_turn:
                if log_level != "MINIMAL":
                    print(f"{x_player.name} (playing as X) won.\n")
                    if not demo_mode:
                        prettify_board(b)
                x_wins += 1
                x_player.wins += 1
                x_player.wins_as_x += 1
                winner = x_player.name

            else:
                if log_level != "MINIMAL":
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
            draws += 1
        if demo_mode:
            sleep(delay * 1.5)

    print(f"\nX wins: {x_wins}")
    print(f"O wins: {o_wins}")
    print(f"draws: {draws}")
    if p1.wins != 0:
        print(f"\n{p1.name} total wins: {p1.wins}. Of those, {p1.wins_as_x} ({round(100 * p1.wins_as_x / p1.wins, 2)}%) were as X.")
    else:
        print(f"\n{p1.name} total wins: 0")
    if p2.wins != 0:
        print(f"{p2.name} total wins: {p2.wins}. Of those, {p2.wins_as_x} ({round(100 * p2.wins_as_x / p2.wins, 2)}%) were as X.")
    else:
        print(f"\n{p2.name} total wins: 0")
    if p2.wins != 0:
        print(f"\n{p1.name} won {p1.wins / p2.wins} more times than {p2.name}")



    if (n > 10) and (p1.mode == "LEARNING"):
        print("\nIf 00, 02, 20 or 22 is not the highest value here, we're in trouble")
        print(p1.model_df.iloc[0][columns])

        print("Here is the first few states of the p1 model at the end of training: ")
        print(p1.model_df[0:5])
        print(f"\nUpdating file {p1.file}")
        p1.model_df.to_csv(p1.file, index = False)

    if p2.mode not in ["LEARNING", "LEARNING_DEMO"]:
        print("p2 model at end of training: ")
        print(p2.model_df)