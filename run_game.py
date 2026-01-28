from xo_functions import make_player_move, make_computer_move, prettify_board

b = [[0,0,0],[0,0,0],[0,0,0]]

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
    b, status = make_player_move(p,b,m,turns_taken)
    turns_taken += 1
    print("The Computer is making its first move")
    b, status = make_computer_move(c,b,turns_taken)
    turns_taken += 1

if p == 1:
    turns_taken = 0
    print("The Computer is going first")
    b, status = make_computer_move(-1,b,turns_taken)
    turns_taken = 1

status = False
winner = 0

while turns_taken != 9 and status == 0:
    print(f"Your move. Here is the board. You are {p_name} and The Computer is {c_name}")

    prettify_board(b)

    valid_move = False
    while valid_move is False:
        try:
            m = input("Input your move: ")
            if m == "q":
                exit()
            b, status = make_player_move(p,b,m,turns_taken)
            turns_taken += 1
            valid_move = True
            print("That's a valid move")
            if status == True:
                print("\nCongrats! You Won!")
                winner = p
        except ValueError:
            print("An error occurred, try again")
    if turns_taken != 9 and status == 0:
        b, status = make_computer_move(c,b,turns_taken)
        turns_taken += 1
        if status == True:
            print("\nOh no! The Computer won :(")
            winner = c

if status == 0:
    print("It was a stalemate")
print("\nHere's the final board:")
prettify_board(b)

