from xo_functions import make_player_action, make_computer_action, prettify_board, Player
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--opponent", help = "what model to play against")
args = parser.parse_args()
opponent = args.opponent

if opponent == "best":
    p2 = Player("Gregg (P2)","FIXED","experiments/20260201_new_champ_1.csv") # Static trained model
elif opponent == "rlhf":
    p2 = Player("P2","RLHF", "experiments/rlhf.csv", "experiments/rlhf.csv", 1, [2,-4,1])  # The focus here is on punishing losses The one is "epsilon" and is not relevant here
    # Long-term, no reason the players actions couldn't also update the same policy
elif opponent == "rlhf_loser":
    # If you would like to play against and agent that has been trained to lose but which you can in theory train to play better
    p2 = Player("P2 (Loser Mode)","RLHF", "experiments/loser_rlhf.csv", "experiments/loser_rlhf.csv", 1, [2,-2,1]) # The one is "epsilon" and is not relevant here
elif opponent == "bad":
    p2 = Player("Hennimore (P2)","FIXED","experiments/weakly_trained_2.csv")
elif opponent == "loser":
    p2 = Player("Hennimore (P2)","FIXED","experiments/loser.csv")
elif opponent == "rules":
    p2 = Player("Al (P2)","RULES_IMPERFECT")
else:
    p2 = Player("Gregg (P2)","FIXED","blank_q_learning_table.csv")
    
p2.greet()
p2.actions, p2.states = [], []

state = [[0,0,0],[0,0,0],[0,0,0]]

x_or_o = input("Are you X (going first) or O (going second)? ").upper()
if x_or_o == "X":
    print("You are X")
    p = -1
    p_name = "X"
    c = 1
    c_name = "O"
elif x_or_o in ["O", "0"]:
    print("You are O")
    p = 1
    p_name = "O"
    c = -1
    c_name = "X"
else:
    print("Invalid input")

print("""
    Here are the inputs:
    
     --------------
    | a1 | a2 | a3 |
     --------------
    | b1 | b2 | b3 |
     --------------
    | c1 | c2 | c3 |
     --------------
      
    To quit, enter "q"
    """)


if p == -1:
    turns_taken = 0
    print("You are going first")
    m = input("Input your move: ")
    if m == "q":
        exit()

    state, status = make_player_action(p,state,m,turns_taken)
    turns_taken += 1
    print("The Computer is making its first move")
    p2.states.append(str(state))
    state, status, description, m = p2.make_agent_action(state,turns_taken,1)
    p2.actions.append(m)
    turns_taken += 1

if p == 1:
    turns_taken = 0
    print("The Computer is going first")
    p2.states.append(str(state))
    state, status, description, m = p2.make_agent_action(state,turns_taken,-1)
    p2.actions.append(m)
    turns_taken = 1

status = False
winner = 0

while turns_taken != 9 and status == 0:
    print(f"Your move. Here is the board. You are {p_name} and The Computer is {c_name}")

    prettify_board(state)

    valid_action = False
    while valid_action is False:
        try:
            m = input("Input your move: ")
            if m == "q":
                exit()
            state, status = make_player_action(p,state,m,turns_taken)
            turns_taken += 1
            valid_action = True
            print("That's a valid move")
            prettify_board(state)
            if status == True:
                print("\nCongrats! You Won!")
                winner = p
                if opponent.startswith("rlhf"):
                    print("Updating policy to account for computer loss. Thanks for contributing to the training!") # This is a lie, all your contributions will stay on your local machine
                    #print(p2.policy_df.loc[p2.policy_df['state'] == str("[[1, -1, -1], [0, 1, 0], [0, 0, 0]]")])
                    p2.update_policy(0, turns_taken)
                    p2.policy_df.to_csv(p2.out_file, index = False)
                    #print(p2.policy_df.loc[p2.policy_df['state'] == str("[[1, -1, -1], [0, 1, 0], [0, 0, 0]]")])
        except ValueError:
            print("An error occurred, try again")
    if turns_taken != 9 and status == 0:
        print("The computer's turn.")
        p2.states.append(str(state))
        state, status, description, m = p2.make_agent_action(state,turns_taken,c)
        p2.actions.append(m)
        turns_taken += 1
        if status == True:
            print("\nOh no! The Computer won :(")
            winner = c
            if opponent == "rlhf_loser":
                print("Updating policy to account for computer win. Thanks for contributing to the training!") # This is a lie, all your contributions will stay on your local machine
                p2.update_policy(1, turns_taken)
                p2.policy_df.to_csv(p2.out_file, index = False)

if status == 0: #TODO: Fix this so this responds to status = 2 for a draw like everything else
    print("It was a draw")
    if opponent == "rlhf_loser":
        print("Updating policy. Thanks for contributing to the training!") # This is a lie, all your contributions will stay on your local machine
        p2.update_policy(2, turns_taken)
        p2.policy_df.to_csv(p2.out_file, index = False)
print("\nHere's the final board:")
prettify_board(state)

