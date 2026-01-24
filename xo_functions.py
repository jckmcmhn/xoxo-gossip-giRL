import random

def check_for_winner(b):
    if sum(b[0]) in [-3,3]: # is the first row a winner
        return True
    elif sum(b[1]) in [-3,3]: # is the second row a winner
        return True
    elif sum(b[2]) in [-3,3]: # is the third row a winner
        return True
    elif (b[0][0] + b[1][0] + b[2][0]) in [-3,3]: # is the first column a winning column
        return True
    elif (b[0][1] + b[1][1] + b[2][1]) in [-3,3]: # is the second column a winner
        return True
    elif (b[0][2] + b[1][2] + b[2][2]) in [-3,3]: # is the third column a winner
        return True
    elif (b[0][0] + b[1][1] + b[2][2]) in [-3,3]: # is the top left to bottom right diagonal a winner
        return True
    elif (b[0][2] + b[1][1] + b[2][0]) in [-3,3]: # is the bottom left to top right diagonal a winner
        return True
    else:
        return False

def make_move(p, b, mr, mc, debug = False):
    """
    Docstring for make_move
    
    :param p: Player, either -1 (x) or 1 (o)
    :param b: The current board. At the start of the game the board will be [[0,0,0],[0,0,0],[0,0,0]]
    :param mr: The row of the square the current player wants to take
    :param mc: The column of the square the current player wants to take
    :param debug: Description
    """
    if (not debug) and b[mr][mc] != 0:
        raise ValueError("Invalid move. That square has already been taken.")
    b[mr][mc] = p
    status = check_for_winner(b)
    return b, status
    
#print("To create a new board where the first player has taken the top left corner, run b, status = make_move(-1,[[0,0,0],[0,0,0],[0,0,0]],0,0)")

def get_possible_moves(b):
    possible_moves = []
    for ir, row in enumerate(b):
        for ic, row_x_column in enumerate(row):
            if row_x_column == 0:
                possible_moves.append((ir,ic))
    return possible_moves

def make_player_move(p,b,m):
    mr, mc = m.split(",")
    mr, mc = int(mr), int(mc)
    b, status = make_move(p, b, mr, mc)
    return b, status

def make_computer_move(p,b):
    pm = get_possible_moves(b)
    m = random.choice(pm)
    print(f"Computer's move is {m}")
    b, status = make_move(p,b,m[0],m[1])
    return b, status

def prettify_board(b):
    map = {-1: "X", 1: "O", 0: " "}
    print("")
    vert = " -----------" 
    print(vert)
    for row in b:
        new = f"| {map[row[0]]} | {map[row[1]]} | {map[row[2]] } |"
        print(new)
        print(vert)
    print("")