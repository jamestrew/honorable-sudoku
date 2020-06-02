easy = [
    [5,0,0,8,3,2,4,0,6],
    [0,6,3,7,4,0,0,0,0],
    [8,0,2,1,9,0,0,0,3],
    [0,3,0,0,2,9,1,0,5],
    [1,0,0,0,0,8,9,6,2],
    [0,0,0,5,0,0,0,7,0],
    [0,0,0,0,1,0,0,2,7],
    [0,2,6,0,0,0,5,0,0],
    [3,1,8,0,5,0,0,4,0]
]

game = easy

# show board
def print_board(game):
    for row in game:
        print(" ".join(map(str,row)))

print("Starting Board:")
print_board(game)
print("\n")

# solve mode
#auto_solve = input("\n\nThis is a gay game.\n 1. Play\n 2. Auto solve\n")

# checks whether the move is legal
def is_possible(x, y, n):
    global game
    for i in range(9):
        if game[x][i] == n:
            return False
    for i in range(9):
        if  game[i][y] == n:
            return False

    x0 = (x//3)*3
    y0 = (y//3)*3

    for i in range(x0, x0+3):
        for j in range(y0, y0+3):
            if game[i][j] == n:
                return False
    return True

# checks whether the game is finished, only for auto_solve = 1 (false)
def is_playball(game):
    for i in range(9):
        for j in range(9):
            if game[i][i] == 0:
                return True

# solves sudoko, runs regardless of player choice
solution = []
def solve():
    global game, solution
    for x in range(9):
        for y in range(9):
            if game[x][y] == 0:
                for n in range(1,10):
                    if is_possible(x, y, n):
                        game[x][y] = n
                        """
                        if x == 8 and y == 8:
                            solution = game
                            return
                        """
                        solve()
                        game[x][y] = 0
                return
    print_board(game)
    solution = game

solve()
auto_solve = 2
if auto_solve == 2:
    print("\nSolution:")
    print_board(solution)
elif auto_solve == 1:
    while is_playball(easy_game):
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        n = int(input("Enter number to enter: "))

        if solution[x][y] == n:
            game[x][y] = n
            print_board(game)
        else:
            print("Try again")
