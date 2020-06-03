class Puzzle(object):
    DIM = 9
    # private:
    __grid = []

    def __init__(self, grid=None):
        if grid is None:
            # fill empty grid
            self.__grid = [0] * (self.DIM**2)
        else:
            # load grid
            self.__grid = grid

    def __str__(self):
        return '\n'.join(' '.join(map(str, self.__grid[i:i+self.DIM])) for (i) in range(0, len(self.__grid), self.DIM))

    def __getitem__(self, key):
        return self.__grid[key[0]*9+key[1]]

    def __setitem__(self, key, val):
        self.__grid[key[0]*9+key[1]] = val
