from abc import ABCMeta, abstractmethod
from MVC.Model.cell import Cell
from functools import reduce
from operator import concat
from resource import *


class Notification(metaclass=ABCMeta):
    @abstractmethod
    def notify(self, x, y, val, /): pass


class Puzzle(object):
    """ Sudoku::Puzzle """

    _grid = []  # grid: Z^1 array for board
    _remaining_moves = 0  # number of moves until complete
    _counts = {}  # counts of each number

    def __init__(self, grid=None, original=None, handle=None):
        """
        (Default/Copy) constructor copies grid to self instance when given.
        The new instance is validated before finishing initialization, and
        removed upon failure of validation.

        :type: None if invalid.

        :param grid: list or Puzzle to instantiate current object.
        :param original: past state of puzzle (used for loading).
        :param handle: ref back to Controller for notifying View.

        :raise TypeError: given (grid, original) not instance of list or Puzzle.
        :raise ValueError: failed validation following classical rules.
        """

        self.__notif = handle  # ref back to Controller for notify

        def cell_parser(m_src, /):
            """
            When puzzle is initialized with instance of list, then each integer
            is parsed with wrapper class Cell to differentiate original from
            updated cells from a prior state.

            :return: list of Cells, representing the grid, from the given
                mutable source (m_src)
            """
            try:  # ASSERTS:
                # Check for valid dimensions of given grid
                if len(m_src) != DIM*DIM: raise ValueError
                return list(map(Cell, m_src))
            except (AttributeError, TypeError, ValueError):
                print(f"[Debug] the puzzle could not be parsed.")
                return None

        # ( STAGE 1 - generate flat container for puzzle grid )
        if grid is None:  # fill empty grid
            self._grid = [0]*(DIM**2)
        elif isinstance(grid, Puzzle):  # copy init
            self._grid = (grid.neighbor(i, ROW) for i in range(DIM))
            self._grid = reduce(concat, self._grid, [])  # noqa
        elif isinstance(grid, list):    # copy init
            self._grid = cell_parser(grid)
        else:  # the given grid is type-checked; otherwise, undefined behavior
            raise TypeError(
                f"expected {type(self)} or {type([])}, but found {type(grid)}"
            )
        # ( STAGE 2 - validation of given grid )
        if not self._validate():
            del self  # that's unfortunate
            raise ValueError(
                f"validation failed."
            )
        else:  # passed validation
            # puzzle properties
            self._remaining_moves = reduce(lambda r, x: r if x>0 else r+1, self._grid, 0)
            self._init_generate = (self._grid[i] for i in range(DIM*DIM))
            self.find_counts()

    # ( OVERRIDES ):
    def __str__(self):
        return '\n'.join(' '.join(map(str, self._grid[i: i+DIM]))
                         for (i) in range(0, len(self._grid), DIM))

    def __getitem__(self, key):
        return self._grid[DIM*key[0] + key[1]]

    def __setitem__(self, key, val):
        if not self.update(key[1], key[0], val):
            raise ValueError

    # METHODS ( PRIVATE ):
    def _validate(self):
        """
        Purpose of this validation method is for instantiation only.
        Not intended to be used outside scope of __init__. Updates to the grid
        are checked before mutating.

        Following the classical rules of Sudoku:
        BLKS,COLS,ROWS are composed of unique integers (excluding zero/empty).

        :return: True when the grid is correclty confirgured, otherwise False.
        """
        if self._grid is None: return False  # parsing stage failed
        result = []  # distinctness check
        for i in range(DIM):
            v_nbr = self._vlookup(i)  # column
            h_nbr = self._hlookup(i)  # row
            b_nbr = self._blookup(i)  # block
            result.append(  # and-map of indexed col, row, and blk distinctness
                # |{non-empty cells}| == |{unique cells}\{0}|
                len(list(filter(lambda n: n!=0, v_nbr))) == len(set(v_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, h_nbr))) == len(set(h_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, b_nbr))) == len(set(b_nbr)-{0})
            )
        return all(result)

    def _vlookup(self, index:int, /) -> list:
        """
        Vertical/column neighboring cells.

        :param index: range(0, DIM)
        :return: a column at the specified COL-index.

        """
        return self._grid[index:: DIM]

    def _hlookup(self, index:int, /) -> list:
        """
        Horizontal/row neighboring cells.

        :param index:  range(0, DIM)
        :return: a row at the specified ROW-index.
        """
        return self._grid[index*DIM: DIM*(index+1)]

    def _blookup(self, index:int, /) -> list:
        """
        Block neighboring cells.
        SUB constant useful for dimensions of sub-matrices.

        :param index: range(0, DIM)
        :return: a block at the specified BLK-index.
        """
        offset = 2*DIM*(index//SUB)  # skip to next row of submatrices
        n = DIM//SUB  # submatrix size (n*n)
        blk_nbr = (  # expected: DIM/3 x DIM/3 submatrix
            self._grid[(n*k)+offset: n*(k+1)+offset]
            for k in range(index, (2*n+index)+1, n)
        )
        return reduce(concat, blk_nbr, [])  # noqa

    # METHODS ( PUBLIC ):
    def neighbor(self, index:int, lookup=BLK) -> list:
        """
        Purposed to fetch one of the three configurations at the given index.
        The three configurations include BLK, COL, and ROW.

        :param index: range(0, DIM)
        :param lookup: (default=BLK) range(0, 3) or in [BLK,COL,ROW]
        :return: the i-th block, where i = index
            Given index, it may return the i-th block, column, or row.

        :raise TypeError: lookup constant type must be int
        :raise ValueError: parameter out-of-range
        """
        # ASSERTS:
        if index<0 or index>=DIM:
            raise ValueError  # out of range
        if not isinstance(lookup, int):
            raise TypeError   # invalid type
        elif lookup<0 or lookup>2:
            raise ValueError  # out of range

        return {  # fetch by lookup-code at given index
            BLK: lambda idx: self._blookup(idx),
            COL: lambda idx: self._vlookup(idx),
            ROW: lambda idx: self._hlookup(idx)
        }.get(lookup)(index)

    def update(self, x:int, y:int, val:int, /) -> bool:
        """
        Updates the grid at the given (x, y)-coordinate with val.

        :param x: ROW in range(0, 9)
        :param y: COL in range(0, 9)
        :param val: value to mutate cell into.
        :return: True if the given move was successful; otherwise, False.
        """
        valid = (val==0)
        # An unchanged update is considered invalid
        if 0 < val != self[x, y]:
            # Find neighbor at specified (x,y) of grid
            v_nbr = list(map(int, self.neighbor(y, COL)))
            h_nbr = list(map(int, self.neighbor(x, ROW)))
            b_nbr = list(map(int, self.neighbor(SUB*(x//SUB) + y//SUB)))
            v_nbr[x] = h_nbr[y] = b_nbr[SUB*(x%SUB) + y%SUB] = val  # peek-update

            # and-map of indexed col, row, and blk distinctness
            valid = len(list(filter(lambda n: n!=0, v_nbr))) == len(set(v_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, h_nbr))) == len(set(h_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, b_nbr))) == len(set(b_nbr)-{0})

        if valid:
            if self._grid[DIM*x + y].locked:
                print(f"[Debug] Invalid move. This cell is locked.")
                return False
            else:
                self._grid[DIM * x + y].update(val)  # set value
                self.find_counts()
                self._remaining_moves += 1 if val == 0 else -1
                if self.__notif: self.__notif.notify(x, y, val)
        return valid

    def lock_check(self, x:int, y:int, /) -> bool:
        return self._grid[x*DIM + y].locked

    def peek(self, x:int, y:int) -> int:
        return int(self._grid[x*DIM + y])

    def find_counts(self):
        for num in range(DIM+1):
            self._counts[num] = self._grid.count(num)

    @property
    def remaining_moves(self) -> int:
        """
        :return: number of moves away from completion.
        """
        return self._remaining_moves

    @property
    def empty(self) -> bool:
        """
        :return: True if grid is zero-filled; otherwise, False.
        """
        return self._remaining_moves == DIM*DIM

    @property
    def complete(self) -> bool:
        """
        :return: True if all cells are non-zero (puzzle is complete);
        otherwise, False.
        """
        return self._remaining_moves == 0

    @property
    def init_iterator(self) -> int:
        """
        A single-use generator for initializaiton.

        :return: a i-th cell value, where i := the number of calls
        """
        return int(next(self._init_generate))

    @property
    def counts(self) -> dict:
        """
        :return: a dict of number of times a number exists in the puzzle
        """
        return self._counts
