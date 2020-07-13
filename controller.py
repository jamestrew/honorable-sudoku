from puzzle import *
from view import *


class Controller(Notification):
    """ Sudoku::CONTROLLER """
    __p = None  # Puzzle
    __v = None  # View

    __gamemode = 0  # may be moved to another class
    # A middleman between Controller-Model update calls to alter gamerules.

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
        self.__v = WidgetDisplay(handle=self)
        self.__v.mainloop()

        ''' If you play game, and exit game with regular windows close button,
            TypeError is raised.

            Closing game using the EXIT GAME button in the Startup page doesn't
        '''
        if isinstance(self.__v, TextDisplay):
            while not(self.__check_win()):
                # input three numbers (x, y, val)
                x, y, val = list(map(int, input().strip().split()))
                if not(self.__p.update(x, y, val)):
                    print(f"[Debug] {type(self)}: invalid move.")
        elif isinstance(self.__v, WidgetDisplay):
            pass
        else:
            raise TypeError(
                f"expected {View} or {WidgetDisplay}, but found {self.__v}"
            )

    def gamemode_update(self, state):
        self.__gamemode = state
        gm = self.__gamemode
        print(f"[Debug] Gamemode updated: 0x{hex(gm)[2:].zfill(2).upper()}")

    def gameboard_init(self, state):
        self.__gameboard = state
        gb = self.__gameboard
        print(f"[Debug] Gamemode updated: {gb}")

        with open(gb, 'r') as f:
            rows = f.readlines()
        game_list = []
        for row in rows:
            game_list.extend(map(int, row.strip().split()))

        self.reset(game_list)
        self.__print_puzzle()  # Temporary for debugging purposes

    def gameboard_update(self, x, y, val):
        return self.__p.update(x, y, val)

    def get_puzzle(self):
        return self.__p

    # METHODS ( PRIVATE ):
    def __print_puzzle(self):
        print(self.__p)

    def check_win(self):
        return self.__p.complete
