from puzzle import Puzzle
import copy

# User selects difficulty
print("Select difficulty: \nEasy\nHard\nMagic\n")
diff = input()

if diff == "Easy":
    fname = "easy.txt"
elif diff == "Hard":
    fname = "hard.txt"
elif diff == "Magic":
    fname = "magic.txt"


# # Read game from txt file and create game board
with open(fname) as f:
    rows = f.readlines()

game = Puzzle()  # create game instance
for i, row in enumerate(rows):
    for j, num in enumerate(row.strip().split()):
        game[i, j] = int(num)


# queries user for game mode
print(game)
print("\nThis is a gay game.\n 1. Play\n 2. Auto solve")
game_mode = int(input())  # 1 - user play, 2 - computer play
usergame = copy.deepcopy(game)  # copy of the game for user
sol_check = False


def is_possible(x, y, n):
    # checks whether the move is legal
    global game
    for i in range(9):
        if game[x, i] == n:
            return False
    for i in range(9):
        if game[i, y] == n:
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3

    for i in range(x0, x0 + 3):
        for j in range(y0, y0 + 3):
            if game[i, j] == n:
                return False
    return True


def is_playball(game):
    # checks whether the game is finished
    for i in range(9):
        for j in range(9):
            if game[i, j] == 0:
                return True


def solve(game):
    # solves sudoko, runs regardless of player choice
    global sol_check
    for x in range(9):
        for y in range(9):
            if game[x, y] == 0:
                for n in range(1, 10):
                    if is_possible(x, y, n):
                        game[x, y] = n
                        solve(game)
                        if sol_check is False:
                            game[x, y] = 0
                    elif x == 8 and y == 8:
                        sol_check = True
                return


solve(game)
print()
if game_mode == 2:
    print("Solution:")
    print(game)
if game_mode == 1:  # user plays
    while is_playball(usergame):
        print()
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        n = int(input("Enter number to enter: "))
        print()

        if game[x, y] == n:
            usergame[x, y] = n
            print(usergame)
        else:
            print("Try again")
            print(usergame)

    print()
    print("YOU WIN. CONGRATS. UR GAY")
