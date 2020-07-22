from puzzle import *
from view import *


class Controller(Notification):
    """ Sudoku::CONTROLLER """
    __p = None  # Puzzle
    __v = None  # View

    __gamemode = 0
    __difficulty = 0

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        """
        notify(x, y, val) sends an update-cmd for the given x,y-indices of the View.
            val is fwd'd to View upon successful update to the main Puzzle.
        """
        if self.__v: self.__v.notify(x, y, val)
        print(f"[Debug] Controller has notified View.")

    def start_game(self):
        """
        start_game() initializes the start of a new Sudoku game.
        """
        self.__v = WidgetDisplay(handle=self)

        # If you play game, and exit game with regular windows close button,
        #   TypeError is raised.
        #   Closing game using the EXIT GAME button in the Startup page doesn't

        if isinstance(self.__v, TextDisplay):
            while not(self.check_win()):
                # input three numbers (x, y, val)
                x, y, val = list(map(int, input().strip().split()))
                if not(self.__p.update(x, y, val)):
                    print(f"[Debug] {type(self)}: invalid move.")
        elif isinstance(self.__v, WidgetDisplay):
            self.__v.mainloop()
        else:
            raise TypeError(
                f"expected {View} or {WidgetDisplay}, but found {self.__v}"
            )

    def gamemode_update(self, state):
        self.__gamemode = state
        gm = self.__gamemode
        print(f"[Debug] Gamemode updated: 0x{hex(gm)[2:].zfill(2).upper()}")

    def load_game(self, gamemode, difficulty):
        """
        load_game(gamemode, difficulty) is called once the required input has
            been fulfilled. The selected gamemode and difficulty is saved.
            A puzzle is generated based on the user's selection.
        """
        self.__gamemode = gamemode
        self.__difficulty = difficulty
        dir_board = {  # all puzzle files
            EASY: "Boards/easy.txt",
            HARD: "Boards/hard.txt",
            MAGI: "Boards/magic.txt"
        }.get(difficulty)
        flat_grid = None  # flattened grid from input
        try:
            with open(dir_board, 'r') as f:
                rows = f.readlines()
        except IOError:
            print(f"[Debug] Puzzle failed to load...")
        else:
            flat_grid = []
            for r in rows:
                flat_grid.extend(map(int, r.strip().split()))
            print(f"[Debug] Puzzle loaded...")
        finally:
            self.__p = Puzzle(flat_grid, handle=self)
            self.print_puzzle()

    def fetch_conflicts(self, x, y, val):
        conflicts = []  # list(pair) of coordinates that conflict with update.

        if val == 0: return set(conflicts)  # clearing a cell cannot cause conflict
        else:
            config_index = {  # { config_key: DIM config }
                'v': self.__p.neighbor(y, COL),  # ROW
                'h': self.__p.neighbor(x, ROW),  # COL
                'b': self.__p.neighbor(DIM//3*(y//3) + x//3)  # BLK
            }
        for (lookup_type, config) in config_index.items():
            config = list(map(int, config))
            if val in config:
                offset = config.index(val)
                conflicts.append({
                    'v': (offset, y),
                    'h': (x, offset),
                    'b': (x//B_DIM + offset//B_DIM, y//B_DIM + offset%B_DIM)
                }.get(lookup_type))
        return set(conflicts)

    def gameboard_update(self, x, y, val):
        return self.__p.update(x, y, val)

    def init_n(self, n=1):
        if isinstance(n, int):
            if n == 0:
                return [
                    self.__p.init_iterator for _ in range(DIM*DIM)
                ]
            if n == 1:
                return self.__p.init_iterator if n>0 else None  # checking if n>0 when n = 1 seems redundant (?)
            if n > 1:
                return [self.__p.init_iterator for _ in range(n)]
            else:
                raise ValueError(
                    f"expected a non-negative integer, but received {n}."
                )
        else:
            raise TypeError(
                f"expected a non-negative integer, but received {type(n)}."
            )

    def perm_n(self, n=1):
        if isinstance(n, int):
            if n == 0:
                return [
                    self.__p.permanent_cell
                    for _ in range(DIM*DIM - self.__p.remaining_moves)
                ]
            if n == 1:
                return self.__p.permanent_cell
            if n > 1:
                return [self.__p.permanent_cell for _ in range(n)]
            else:
                raise ValueError(
                    f"expected a non-negative integer, but received {n}."
                )
        else:
            raise TypeError(
                f"expected a non-negative integer, but received {type(n)}."
            )

    # METHODS ( PRIVATE ):
    def print_puzzle(self):
        print(self.__p)

    def check_win(self):
        return self.__p.complete
