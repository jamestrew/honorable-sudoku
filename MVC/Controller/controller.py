from MVC.Model.puzzle import *
from MVC.View.view import *
from MVC.Model.lp_compute import LpCompute


class Controller(Notification):
    """ Sudoku::CONTROLLER """

    def __init__(self):
        self.__p = None  # Puzzle
        self.__v = None  # View

        self.__gamemode = USER_PLAY
        self.__difficulty = EASY_DIFF

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        """
        notify(x, y, val) sends an update-cmd for the given x,y-indices of the View.
            val is fwd'd to View upon successful update to the main Puzzle.
        """
        if self.__v: self.__v.notify(x, y, val)

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

    def computer_ping(self):
        # ( constraint problem )
        lp = LpCompute()
        lp.solve(self.__p)
        if lp.optimal:
            print(lp)
            return lp.update_iter
        else:
            return self.backtracking_iter()

    def backtracking_iter(self):
        """
        Generator for update callbacks used by the computer-play mode.
        :return: arguments in order to callback updates
        """
        # ( main loop - grid traversal )
        for c in range(DIM * DIM):
            x, y = (c // DIM, c % DIM)  # read constants
            # skip cell upon lock or occupied value
            if self.lock_check(x, y) or self.peek(x, y) != 0: continue
            # ( possible values )
            for value in range(1, DIM + 1):
                valid = self.__p.update(x, y, value)  # attempt update
                if valid:
                    yield x, y, value  # update args
                    yield from self.computer_ping()
                # collapse-of-recursion check
                if valid and not self.__p.complete:
                    self.__p.update(x, y, 0)  # revert
            break  # STOP ITER

    def fetch_gamemode(self):
        return self.__gamemode

    def fetch_difficulty(self):
        return self.__difficulty

    def load_game(self, gamemode, difficulty):
        """
        load_game(gamemode, difficulty) is called once the required input has
            been fulfilled. The selected gamemode and difficulty is saved.
            A puzzle is generated based on the user's selection.
        """
        self.__gamemode = gamemode
        self.__difficulty = difficulty

        dir_board = {  # all puzzle files
            EASY_DIFF: "Boards/easy.puzzle",
            HARD_DIFF: "Boards/hard.puzzle",
            MAGI_DIFF: "Boards/magic.puzzle"
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
            print(f"[Debug] Puzzle loaded: gamemode({gamemode}), difficulty({difficulty})")
            # self.print_puzzle()  # [Debug]
        finally:
            self.__p = Puzzle(flat_grid, handle=self)

    def fetch_conflicts(self, x, y, val):
        conflicts = []  # list(pair) of coordinates that conflict with update.

        if val == 0: return set(conflicts)      # clearing a cell cannot cause conflict
        blk_x, blk_y = (x - x%SUB, y - y%SUB)   # rounded to factor of 3
        config_index = {  # { config_key: DIM config }
            ROW: self.__p.neighbor(x, ROW),  # ROW
            COL: self.__p.neighbor(y, COL),  # COL
            BLK: self.__p.neighbor(blk_x + y//SUB)  # BLK
        }
        for (lookup_type, config) in config_index.items():
            config = list(map(int, config))
            if val in config:
                offset = config.index(val)
                conflicts.append({
                    ROW: (x, offset),
                    COL: (offset, y),
                    BLK: (blk_x + offset//SUB, blk_y + offset%SUB)
                }.get(lookup_type))
        return set(conflicts)

    def gameboard_update(self, x, y, val):
        return self.__p.update(x, y, val)

    def count_update(self):
        return self.__p.counts

    def init_next(self):
        return self.__p.init_iterator

    def lock_check(self, x:int, y:int, /) -> bool:
        return self.__p.lock_check(x, y)

    def peek(self, x, y):
        return self.__p.peek(x, y)

    def print_puzzle(self):
        print(self.__p)

    def check_win(self):
        return self.__p.complete
