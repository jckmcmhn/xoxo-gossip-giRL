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
    | 0,0 | 0,1 | 0,2 |
    | 1,0 | 1,1 | 1,2 |
    | 2,0 | 2,1 | 2,2 |
      
    To quit, enter "q"
    """)

if p == -1:
    print("You are going first")
    m = input("Input your move: ")
    if m == "q":
        exit()
    b, status = make_player_move(p,b,m)
    print("The Computer is making its first move")
    b, status = make_computer_move(c,b)

if p == 1:
    print("The Computer is going first")
    b, status = make_computer_move(-1,b)

status = False
winner = 0

while status is False:
    print(f"Your move. Here is the board. You are {p_name} and The Computer is {c_name}")

    prettify_board(b)

    valid_move = False
    while valid_move is False:
        try:
            m = input("Input your move: ")
            if m == "q":
                exit()
            b, status = make_player_move(p,b,m)
            valid_move = True
            if status == True:
                print("\nCongrats! You Won!")
                winner = p
        except ValueError:
            print("An error occurred, try again")
    if status is False:
        b, status = make_computer_move(c,b)
        if status == True:
            print("\nOh no! The Computer won :(")
            winner = c

if status:
    print("\nHere's the final board:")
    prettify_board(b)