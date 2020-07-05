from sudoku import *


class Controller(Notification):
    __p = None  # Puzzle
    __v = None  # View

    # METHODS ( PUBLIC ):
    """
    notify(x, y, val) sends an update-cmd for the given x,y-indices of the View.
        val is fwd'd to View upon successful update to the main Puzzle.
    """
    def notify(self, x, y, val, /):
        print(f"[Debug] successfully changed (col:{x}, row:{y}) to {val}.")
        self.__print_puzzle()

    """
    reset(game) resets the Puzzle and View with the given game.
    """
    def reset(self, game=None, /):
        self.__p = Puzzle(grid=game, handle=self)
        self.__v = None

    """
    start_game() initializes the start of a new Sudoku game.
    """
    def start_game(self):
        while not(self.__check_win()):
            # input three numbers (x, y, val)
            x, y, val = list(map(int, input().strip().split()))
            if not(self.__p.update(x, y, val)):
                print("[Debug] invalid move.")

    # METHODS ( PRIVATE ):
    def __print_puzzle(self):
        print(self.__p)

    def __check_win(self):
        return self.__p.complete
