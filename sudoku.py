import operator
from const import *
from functools import reduce


""" Sudoku::MODEL """
class Puzzle(object):
    # grid: Z^1 array for board
    __grid = []
    __remainingMoves = 0

    """
    (Default/Copy) constructor
        - Copies grid to self when given
        - Runs board validation on creation of new instance
        - Instance removed on a non-valid outcome
        Requires:
        - Optional grid arg is of <class 'Puzzle'> or <class 'List>
        - Given grid follows classic logical rules of a Sudoku puzzle
    """
    def __init__(self, grid=None, /):
        if grid is None:  # fill empty grid
            self.__grid = [0]*(DIM**2)
        elif isinstance(grid, Puzzle):  # copy init
            self.__grid = (grid.neighbor(i, ROW) for i in range(DIM))
            self.__grid = reduce(operator.concat, self.__grid, [])
        elif isinstance(grid, list):    # copy init
            self.__grid = [cp%(DIM+1) for cp in grid]
        else:
            raise TypeError\
            (
                f"expected {type(self)} or {type([])}, but found {type(grid)}"
            )
        if not self.__validate():
            del self  # that's unfortunate
            raise ValueError\
            (
                f"validation failed."
            )
        else:
            self.__remainingMoves = reduce(lambda r, x: r if x>0 else r+1, self.__grid, 0)

    # ( OVERRIDES ):
    def __str__(self):
        return '\n'.join(' '.join(map(str, self.__grid[i: i+DIM]))
                         for (i) in range(0, len(self.__grid), DIM))

    def __getitem__(self, key):
        return self.__grid[DIM*key[0] + key[1]]

    def __setitem__(self, key, val):
        if self[key[1], key[0]]!=val:
            self.__grid[DIM*key[0] + key[1]] = val
            self.__remainingMoves += 1 if val==0 else -1

    # METHODS ( PRIVATE ):
    """
    validate() returns True when the grid is correclty confirgured, otherwise False.
        Requires:
        - Puzzle is a 9*9 matrix
        - Each cell value is of <class: 'int'>
        - BLKS,COLS,ROWS are composed of unique integers (excluding zero/empty)
    """
    def __validate(self):
        try:
            if len(self.__grid) != DIM*DIM: raise ValueError
            grid = list(map(int, self.__grid))
        except (TypeError, ValueError) as err:
            return False
        grid= list(map(int, grid))
        result = []  # distinct-check flags
        for i in range(DIM):
            v_nbr = self.__vlookup(i)
            h_nbr = self.__hlookup(i)
            b_nbr = self.__blookup(i)
            result.append(
                # |{non-empty cells}| == |{unique cells}\{0}|
                len(list(filter(lambda n: n!=0, v_nbr))) == len(set(v_nbr)-{0}) and
                len(list(filter(lambda n: n!=0, h_nbr))) == len(set(h_nbr)-{0}) and
                len(list(filter(lambda n: n!=0, b_nbr))) == len(set(b_nbr)-{0})
            )
        return all(result)

    """
    vlookup(index) returns a ROW at the specified ROW-index.
        index follows 0..DIM convention (LHS to RHS)
    """
    def __vlookup(self, index, /):
        return self.__grid[index:: DIM]

    """
    hlookup(index) returns a COL at the specified COL-index.
        index follows 0..DIM convention (TOP to BOT)
    """
    def __hlookup(self, index, /):
        return self.__grid[index*DIM: DIM*(index+1)]

    """
    blookup(index) returns a BLK at the specified BLK-index.
        index follows 0..DIM convention (TOP-LHS to BOT-RHS)
    """
    def __blookup(self, index, /):
        offset = 2*DIM*(index//3)  # skip to next row of submatrices
        n = DIM//3  # submatrix size (n*n)
        blk_nbr = (
            self.__grid[(n*k)+offset: n*(k+1)+offset]
            for k in range(index, (2*n+index)+1, n)
        )
        return reduce(operator.concat, blk_nbr, [])

    # public:
    """
    neighbor(index, lookup=0) returns the i-th BLK. Optionally takes in a
            lookup code, changing return val to the i-th COL, ROW, or BLK.
        Range:
        - (int)index is in range[0..DIM-1]
        - (int)lookup is in range[0..2] or [BLK,COL,ROW]
    """
    def neighbor(self, index, lookup=None):
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

    """
    remainingMoves() returns the number of cells that require input in order to
        complete the puzzle.
    """
    def remainingMoves(self):
        return self.__remainingMoves

    """
    empty() returns True if grid is zero-filled, otherwise False.
    """
    def empty(self):
        return self.__remainingMoves == DIM*DIM

    """
    complete() returns True if all cells are non-zero (puzzle is complete), otherwise False.
    """
    def complete(self):
        return self.__remainingMoves == 0
