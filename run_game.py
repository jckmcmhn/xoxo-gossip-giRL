from xo_functions import make_player_move, make_computer_move

b = [[0,0,0],[0,0,0],[0,0,0]]

player_name = input("Are you X (going first) or O (going second)? ").lower()
if player_name == "x":
    print("You are X")
    p = -1
    c = 1
elif player_name in ["o", "0"]:
    print("You are O")
    p = 1
    c = -1
else:
    print("Invalid input")

print("""
      Here are the inputs:
      | 0,0 | 0,1 | 0,2 |
      | 1,0 | 1,1 | 1,2 |
      | 2,0 | 2,1 | 2,2 |
      """)

if p == -1:
    print("You are going first")
    m = input("Input your move: ")
    b, status = make_player_move(p,b,m)
    print("Computer's first turn")
    b, status = make_computer_move(c,b)

if p == 1:
    print("Computer is going first")
    b, status = make_computer_move(-1,b)

status = False
winner = 0

while status is False:
    print(f"Your move. Here is the board. You are {p} and the computer is {c}")
    print(b[0])
    print(b[1])
    print(b[2])
    valid_move = False
    while valid_move is False:
        try:
            m = input("Input your move: ")
            b, status = make_player_move(p,b,m)
            valid_move = True
            if status == True:
                print("Congrats! You Won!")
                winner = p
        except:
            print("An error occurred, try again")
    if status is False:
        b, status = make_computer_move(c,b)
        if status == True:
            print("Oh no! The computer won :(")
            winner = c