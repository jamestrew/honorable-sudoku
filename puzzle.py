from abc import ABCMeta, abstractmethod
from cell import Cell
from functools import reduce
from operator import concat
from resource import *


class Notification(metaclass=ABCMeta):
    @abstractmethod
    def notify(self, x, y, val, /): pass


class Puzzle(object):
    """ Sudoku::Puzzle """
    __grid = []         # grid: Z^1 array for board
    __remaining_moves = 0  # number of moves until complete

    def __init__(self, grid=None, original=None, handle=None):
        """
        (Default/Copy) constructor
            - Copies grid to self when given
            - Runs board validation on creation of new instance
            - Instance removed on a non-valid outcome
            Requires:
            - Optional grid arg is of <class 'Puzzle'> or <class 'List>
            - Given grid follows classic logical rules of a Sudoku puzzle
        """
        self.__notif = handle  # ref back to Controller for notify

        def cell_parser(m_src):
            """
            cell_parser(m_src) returns a list of Cells, representing the grid,
                from the given mutable source (m_src)
            """
            try:  # ASSERTS:
                # Check for valid dimensions of given grid
                if len(m_src) != DIM*DIM: raise ValueError
                return list(map(Cell, m_src))
            except (AttributeError, TypeError, ValueError):
                print(f"[Debug] the puzzle could not be parsed.")
                return None

        # STAGE 1 - generate flat container for puzzle grid
        if grid is None:  # fill empty grid
            self.__grid = [0]*(DIM**2)
        elif isinstance(grid, Puzzle):  # copy init
            self.__grid = (grid.neighbor(i, ROW) for i in range(DIM))
            self.__grid = reduce(concat, self.__grid, [])  # noqa
        elif isinstance(grid, list):    # copy init
            self.__grid = cell_parser(grid)
        else:  # the given grid is type-checked; otherwise, undefined behavior
            raise TypeError(
                f"expected {type(self)} or {type([])}, but found {type(grid)}"
            )
        # STAGE 2 - validation of given grid
        if not self.__validate():
            del self  # that's unfortunate
            raise ValueError(
                f"validation failed."
            )
        else:  # passed validation
            self.__remaining_moves = reduce(lambda r, x: r if x>0 else r+1, self.__grid, 0)
            self.__permanent_cell = self.permanent_iterator
            self.__init_generate = (self.__grid[i] for i in range(DIM*DIM))

    # ( OVERRIDES ):
    def __str__(self):
        return '\n'.join(' '.join(map(str, self.__grid[i: i+DIM]))
                         for (i) in range(0, len(self.__grid), DIM))

    def __getitem__(self, key):
        return self.__grid[DIM*key[0] + key[1]]

    def __setitem__(self, key, val):
        if not self.update(key[1], key[0], val):
            raise ValueError

    # METHODS ( PRIVATE ):
    def __validate(self):
        """
        validate() returns True when the grid is correclty confirgured, otherwise False.
            Requires:
            - Puzzle is a 9*9 matrix
            - Each cell value is of <class: 'int'>
            - BLKS,COLS,ROWS are composed of unique integers (excluding zero/empty)
        """
        if self.__grid is None: return False  # parsing stage failed
        result = []  # distinctness check
        for i in range(DIM):
            v_nbr = self.__vlookup(i)  # column
            h_nbr = self.__hlookup(i)  # row
            b_nbr = self.__blookup(i)  # block
            result.append(  # and-map of indexed col, row, and blk distinctness
                # |{non-empty cells}| == |{unique cells}\{0}|
                len(list(filter(lambda n: n!=0, v_nbr))) == len(set(v_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, h_nbr))) == len(set(h_nbr)-{0}) and \
                len(list(filter(lambda n: n!=0, b_nbr))) == len(set(b_nbr)-{0})
            )
        return all(result)

    def __vlookup(self, index, /):
        """
        vlookup(index) returns a COL at the specified COL-index.
            index follows 0..DIM convention (TOP to BOT)
        """
        return self.__grid[index:: DIM]

    def __hlookup(self, index, /):
        """
        hlookup(index) returns a ROW at the specified ROW-index.
            index follows 0..DIM convention (LHS to RHS)
        """
        return self.__grid[index*DIM: DIM*(index+1)]

    def __blookup(self, index, /):
        """
        blookup(index) returns a BLK at the specified BLK-index.
            index follows 0..DIM convention (TOP-LHS to BOT-RHS)
        """
        offset = 2*DIM*(index//3)  # skip to next row of submatrices
        n = DIM//3  # submatrix size (n*n)
        blk_nbr =(  # expected: DIM/3 x DIM/3 submatrix
            self.__grid[(n*k)+offset: n*(k+1)+offset]
            for k in range(index, (2*n+index)+1, n)
        )
        return reduce(concat, blk_nbr, [])  # noqa

    # METHODS ( PUBLIC ):
    def neighbor(self, index, lookup=None):
        """
        neighbor(index, lookup=0) returns the i-th BLK. Optionally takes in a
                lookup code, changing return val to the i-th COL, ROW, or BLK.
            Range:
            - (int)index is in range[0..DIM-1]
            - (int)lookup is in range[0..2] or [BLK,COL,ROW]
        """
        # ASSERTS:
        if index<0 or index>=DIM:
            raise ValueError      # out of range
        if lookup:
            if not isinstance(lookup, int):
                raise TypeError   # invalid type
            elif lookup<0 or lookup>2:
                raise ValueError  # out of range
        else: lookup = BLK        # default

        return {  # fetch by lookup-code at given index
            BLK: lambda idx: self.__blookup(idx),
            COL: lambda idx: self.__vlookup(idx),
            ROW: lambda idx: self.__hlookup(idx)
        }.get(lookup)(index)

    def update(self, x, y, val, /):
        """
        update(index, val) returns True if the given move was successful,
                otherwise False.
            Requires: (int)x,(int)y is in range[0..DIM-1]
            Affects: grid changes at the specified index with the given val
        """
        # An unchanged update is considered invalid
        if self[x, y]==val: return False

        self.__conflicts = []  # list(tuple) of coords of cells that conflict (max len = 3)

        # Find neighbor at specified (x,y) of grid
        v_nbr = self.neighbor(y, COL)
        h_nbr = self.neighbor(x, ROW)
        b_nbr = self.neighbor(DIM//3*(y//3) + x//3)

        # Peek-update
        try:
            c = Cell(val)
            v_nbr.pop(x)
            v_nbr.append(c)
            h_nbr.pop(y)
            h_nbr.append(c)
            b_nbr.pop(DIM//3*(x%3) + y%3)
            b_nbr.append(c)
            del c
        except AttributeError as err:
            print(f"[Debug] Invalid move. {str.capitalize(str(err))}")
            return False

        # and-map of indexed col, row, and blk distinctness
        valid = len(list(filter(lambda n: n!=0, v_nbr))) == len(set(v_nbr)-{0}) and \
            len(list(filter(lambda n: n!=0, h_nbr))) == len(set(h_nbr)-{0}) and \
            len(list(filter(lambda n: n!=0, b_nbr))) == len(set(b_nbr)-{0})
        if valid:
            self.__grid[DIM*x + y].update(val)  # set value
            self.__remaining_moves += 1 if val == 0 else -1
            if self.__notif: self.__notif.notify(x, y, val)
        return valid

    @property
    def remaining_moves(self):
        """ number of moves away from completion """
        return self.__remaining_moves

    @property
    def empty(self):
        """ True if grid is zero-filled, otherwise False """
        return self.__remaining_moves == DIM*DIM

    @property
    def complete(self):
        """ True if all cells are non-zero (puzzle is complete), otherwise False. """
        return self.__remaining_moves == 0

    @property
    def permanent_iterator(self):
        """
        Returns a generator for all the cell indices that were non-empty in
            the original puzzle.
        """
        return (i for i in range(DIM*DIM) if self.__grid[i].locked)

    @property
    def permanent_cell(self):
        """
        Returns a single coordinate on the puzzle board that represents a cell
            from the original puzzle; therefore, being locked/permanent.

            This operation is cyclic and will loop back to the first cell when
            running into a StopIteration.
        """
        c = None
        while c is None:  # cyclic iterator
            try:
                c = next(self.__permanent_cell)
            except StopIteration:
                self.__permanent_cell = self.permanent_iterator
        return c//DIM, c%DIM

    @property
    def init_iterator(self):
        return next(self.__init_generate)
