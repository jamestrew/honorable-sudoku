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
        - Takes an optional non-positional argument of type Puzzle to copy
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
        return '\n'.join(' '.join(map(str, self.__grid[i:i + DIM]))
                         for (i) in range(0, len(self.__grid), DIM))

    def __getitem__(self, key):
        return self.__grid[key[0]*9 + key[1]]

    def __setitem__(self, key, val):
        self.__grid[key[0]*9 + key[1]] = val

    # METHODS ( PRIVATE ):
    '''
    validate() returns True when the grid is correclty confirgured, otherwise False.
        Config assertion:
        - Puzzle is a 9*9 matrix
        - Each cell value is of <class: 'int'>
        - BLKS,COLS,ROWS are composed of unique integers (excluding zero/empty)
    '''
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

    '''
    vlookup(index) returns a ROW at the specified ROW-index.
        index follows 0..DIM convention (LHS to RHS)
    '''
    def __vlookup(self, index, /):
        return self.__grid[index:: DIM]

    '''
    hlookup(index) returns a COL at the specified COL-index.
        index follows 0..DIM convention (TOP to BOT)
    '''
    def __hlookup(self, index, /):
        return self.__grid[index*DIM: DIM*(index+1)]

    '''
    blookup(index) returns a BLK at the specified BLK-index.
        index follows 0..DIM convention (TOP-LHS to BOT-RHS)
    '''
    def __blookup(self, index, /):
        offset = index//3  # skip to next row of submatrices
        n = DIM//3         # submatrix size (n*n)
        blk_nbr = (
            self.__grid[(n*k)+(2*DIM*offset): n*(k+1)+(2*DIM*offset)]
            for k in range(index, (2*n+index)+1, n)
        )
        return reduce(operator.concat, blk_nbr, [])

    # public:
    '''
    neighbor(index, lookup=0) returns the i-th BLK. Optionally takes in a lookup code.
        Specifying a lookup code changes function to return the i-th BLK, COL, or ROW.
        Range:
        - (int)index is in [0..DIM-1]
        - (int)lookup is in [0..2] or [BLK,COL,ROW]
    '''
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

    def remainingMoves(self):
        return self.__remainingMoves

    def empty(self):
        return self.__remainingMoves == DIM*DIM

    def complete(self):
        return self.__remainingMoves == 0
