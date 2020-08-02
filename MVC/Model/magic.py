from MVC.Model.puzzle import *
from itertools import permutations


class Magic_Puzzle(Puzzle):
    """
    Sudoku::Puzzle with magic ruleset.
    Inherits base rules, methods/properties from Puzzle.

    Adds three new lookups for neighbor:
        - __nlookup (max len = 8)
        - __klookup (max len = 8)
        - __alookup (max len = 4)
    """

    def __nlookup(self, index:int, /) -> list:
        """
        Neighboring cells created by Chess' knight's move.

        :param index: range(0, DIM*DIM)
        :return: list of cell values of valid knight moves.
        """
        bounds = self.__blk_helper(index, 2)
        upper, lower = bounds.get(UPPER), bounds.get(LOWER)
        left, right = bounds.get(LEFT), bounds.get(RIGHT)

        cells = []
        for dx, dy in permutations([1,2,-1,-2], 2):
            if abs(dx) != abs(dy):
                move = (index+dx) + (DIM*dy)
                move_row = move//DIM
                move_col = move%DIM
                if move >= 0 and move < DIM**2 and \
                        upper <= move_row <= lower and \
                        left <= move_col <= right:
                    cells.append(self.__grid[move])
        return cells

    def __klookup(self, index:int, /) -> list:
        """
        Neighboring cells created by Chess' king's move.

        :param index: range(0, DIM*DIM)
        :return: list of cell values of valid king moves.
        """
        bounds = self.__blk_helper(index, 1)
        height = bounds.get(LOWER) - bounds.get(UPPER) + 1  # height of move
        width = bounds.get(RIGHT) - bounds.get(LEFT) + 1  # width of move
        start = bounds.get(UPPER)*DIM + bounds.get(LEFT)  # top-left index of move rng

        blk = (
            self.__grid[i:i+width]
            for i in range(start, height*DIM+start, DIM)
        )
        return reduce(concat, blk, [])

    def __alookup(self, index:int, /) -> list:
        """
        Adjacent neighboring cells (up/down, left/right by 1 cell).
        AKA king's move minus diagonals.

        :param index: range(0, DIM*DIM)
        :return: list of cell values of adjacent cells.
        """
        cells = []
        if index < DIM*DIM - DIM:  # get cell below
            cells.append(self.__grid[index + DIM])
        if index >= DIM:  # get cell above
            cells.append(self.__grid[index - DIM])
        if index%DIM != 0:  # get cell left
            cells.append(self.__grid[index - 1])
        if (index+1)%DIM != 0:  # get cell right
            cells.append(self.__grid[index + 1])
        return cells

    def __blk_helper(self, index:int, rng:int, /) -> dict:
        """
        Calculate upper/lower bounds of the rows/cols for respective moves.
        Helper function for __nlookup, kings_move.

        :param index: range(0, DIM*DIM)
        :param rng: num of cells away from the index cell to move (1 for king, 2 for knight)
        :return: two sets of row and col numbers.
        """
        return {
            UPPER: index//DIM - rng if (index//DIM - rng) > -1 else 0,
            LOWER:index//DIM + rng if (index//DIM + rng) < DIM else DIM - 1,
            LEFT:index%DIM - rng if (index%DIM - rng) > -1 else 0,
            RIGHT:index%DIM + rng if (index%DIM + rng) < DIM else DIM - 1
        }

    # METHODS ( PUBLIC ):
    def neighbor(self, index:int, lookup=BLK) -> list:
        """
        Purposed to fetch one of the five configurations at the given index.
        The three configurations include BLK, COL, ROW, NTE, KNG and ADJ.

        :param index: range(0, DIM*DIM)
        :param lookup: (default=BLK) range(0, 3) or in [BLK,COL,ROW,NTE,KNG,ADJ]
        :return: Given index, return corresponding block, column, row, knight's moves,
            king's move and adjacent cells (vertically & horizontally)

        :raise TypeError: lookup constant type must be int
        :raise ValueError: parameter out-of-range
        """
        # ASSERTS:
        if not isinstance(lookup, int):
            raise TypeError   # invalid type
        elif (0 <= lookup <= 5):
            if 0 <= lookup <= 3:
                if not (0 <= index < DIM):
                    raise ValueError  # index out of range
            else:
                if not (0 <= index < DIM*DIM):
                    raise ValueError  # index out of range
        else: raise ValueError  # lookup out of range

        return {  # fetch by lookup-code at given index
            BLK: lambda idx: self.__blookup(idx),
            COL: lambda idx: self.__vlookup(idx),
            ROW: lambda idx: self.__hlookup(idx),
            NTE: lambda idx: self.__nlookup(idx),
            KNG: lambda idx: self.__klookup(idx),
            ADJ: lambda idx: self.__alookup(idx)
        }.get(lookup)(index)

    def update(self, x:int, y:int, val:int, /) -> bool:
        """
        Updates the grid at the given (x, y)-coordinate with val.

        :param x: ROW in range(0, 9)
        :param y: COL in range(0, 9)
        :param val: value to mutate cell into.
        :return: True if the given move was successful; otherwise, False.
        """
        idx = DIM*x + y
        valid = (val==0)
        # An unchanged update is considered invalid
        if 0 < val != self[x, y]:
            # Find neighbor at specified (x,y) of grid
            v_nbr = list(map(int, self.neighbor(y, COL)))
            h_nbr = list(map(int, self.neighbor(x, ROW)))
            b_nbr = list(map(int, self.neighbor(SUB*(x//SUB) + y//SUB)))
            n_nbr = list(map(int, self.neighbor(idx, NTE)))
            k_nbr = list(map(int, self.neighbor(idx, KNG)))
            a_nbr = list(map(int, self.neighbor(idx, ADJ)))
            v_nbr[x] = h_nbr[y] = b_nbr[SUB*(x%SUB) + y%SUB] = val  # peek-update

            # and-map of indexed col, row, and blk distinctness
            valid = len(list(filter(lambda n: n!=0, v_nbr))) == len(set(v_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, h_nbr))) == len(set(h_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, b_nbr))) == len(set(b_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, n_nbr))) == len(set(n_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, k_nbr))) == len(set(k_nbr)-{0}) and \
                (val-1) not in a_nbr and (val+1) not in a_nbr

        if valid:
            if self.__grid[idx].locked:
                print(f"[Debug] Invalid move. This cell is locked.")
                return False
            else:
                self.__grid[idx].update(val)  # set value
                self.find_counts()
                self.__remaining_moves += 1 if val == 0 else -1
                if self.__notif: self.__notif.notify(x, y, val)
        return valid
