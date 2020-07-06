from puzzle import *
from view import *


class Controller(Notification):
    """ Sudoku::CONTROLLER """
    __p = None  # Puzzle
    __v = None  # View

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        """
        notify(x, y, val) sends an update-cmd for the given x,y-indices of the View.
            val is fwd'd to View upon successful update to the main Puzzle.
        """
        self.__v.notify(x, y, val)
        self.__print_puzzle()

    def reset(self, game=None, /):
        """
        reset(game) resets the Puzzle and View with the given game.
        """
        self.__p = Puzzle(grid=game, handle=self)
        self.__v = None

    def start_game(self):
        """
        start_game() initializes the start of a new Sudoku game.
        """
        self.__v = WidgetDisplay()
        while not(self.__check_win()):
            # input three numbers (x, y, val)
            x, y, val = list(map(int, input().strip().split()))
            if not(self.__p.update(x, y, val)):
                print(f"[Debug] {type(self)}: invalid move.")

    # METHODS ( PRIVATE ):
    def __print_puzzle(self):
        print(self.__p)

    def __check_win(self):
        return self.__p.complete
