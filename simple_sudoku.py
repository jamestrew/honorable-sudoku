"""

Classic sudoku
BOARD SOLUTION: https://i.imgur.com/T4hYPQx.png


"""

from sudoku import Puzzle


# setting up an easy game board
# maybe add other options/difficulties later
easy = [
    5, 0, 0, 8, 3, 2, 4, 0, 6,
    0, 6, 3, 7, 4, 0, 0, 0, 0,
    8, 0, 2, 1, 9, 0, 0, 0, 3,
    0, 3, 0, 0, 2, 9, 1, 0, 5,
    1, 0, 0, 0, 0, 8, 9, 6, 2,
    0, 0, 0, 5, 0, 0, 0, 7, 0,
    0, 0, 0, 0, 1, 0, 0, 2, 7,
    0, 2, 6, 0, 0, 0, 5, 0, 0,
    3, 1, 8, 0, 5, 0, 0, 4, 0
]

game = Puzzle(easy)

print("Starting Board:")
#print_board(game)
print(game)
print('\n')

# queries user for game mode
#auto_solve = input("\n\nThis is a gay game.\n 1. Play\n 2. Auto solve\n")

# checks whether the move is legal
def is_possible(x, y, n):
    global game
    for i in range(9):
        if game[x, i] == n:
            return False
    for i in range(9):
        if game[i, y] == n:
            return False

    x0 = (x//3)*3
    y0 = (y//3)*3

    for i in range(x0, x0+3):
        for j in range(y0, y0+3):
            if game[i, j] == n:
                return False
    return True

# checks whether the game is finished, only for auto_solve = 1 (false)
def is_playball(game):
    for i in range(9):
        for j in range(9):
            if game[i, j] == 0:
                return True

# solves sudoko, runs regardless of player choice
solution = []
tmp = 0
def solve(game):
    global tmp
    for x in range(9):
        for y in range(9):
            if game[x, y] == 0:
                for n in range(1, 10):
                    if is_possible(x, y, n):
                        game[x, y] = n
                        solve(game)
                        if (tmp == 0):
                            game[x, y] = 0  # necessary for proper backtracking
                    elif y*9+x == 80:
                        tmp = 1
                return
    print(game)  # only time the solution exists/prints
    print()

print(solve(game))
print()
auto_solve = 2  # temporary
if auto_solve == 2:
    print("Solution:")
    print(game)  # doesn't print solution
elif auto_solve == 1:  # user plays
    while is_playball(game):
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        n = int(input("Enter number to enter: "))

        if solution[x, y] == n:
            game[x, y] = n
            print(game)
        else:
            print("Try again")
