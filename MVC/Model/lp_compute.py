from resource import *
from pulp import *
from pulp.solverdir import *
from string import digits
import itertools


class LpCompute(object):
    def __init__(self):
        self.__seq = list(digits.strip('0'))
        self.__rows = self.__seq
        self.__cols = self.__seq
        self.__blks = []
        self.__vals = self.__seq

        for i in range(DIM):
            x, y = (i // SUB, i % SUB)
            self.__blks += [[
                (self.__rows[SUB * x + u], self.__cols[SUB * y + v])
                for u in range(SUB)
                for v in range(SUB)
            ]]
        self.problem = LpProblem("sudoku-classic", LpMinimize)
        self.choices = LpVariable.dicts("choice", (self.__vals, self.__rows, self.__cols), 0, 1, LpInteger)

    def set_objective(self, objective:int or tuple):
        self.problem += objective

    def set_value_constraits(self):
        for v in self.__vals:
            for r in self.__rows:
                self.set_objective(
                    (lpSum([self.choices[v][r][c] for c in self.__cols]) == 1, "")
                )
            for c in self.__cols:
                self.set_objective(
                    (lpSum([self.choices[v][r][c] for r in self.__rows]) == 1, "")
                )
            for b in self.__blks:
                self.set_objective(
                    (lpSum([self.choices[v][r][c] for (r, c) in b]) == 1, "")
                )

    def solve(self, grid):
        self.set_objective(0)

        # classical-sudoku gamerule contraint
        for r in self.__rows:
            for c in self.__cols:
                self.set_objective(
                    (lpSum([self.choices[v][r][c] for v in self.__vals]) == 1, "")
                )
        self.set_value_constraits()

        #
        for i in range(DIM*DIM):
            x, y = (i//DIM, i%DIM)
            v = grid.peek(x, y)
            if v != 0:
                self.set_objective(
                    (self.choices[str(v)][str(x + 1)][str(y + 1)] == 1, "")
                )
        self.problem.solve()

    @property
    def update_iter(self):
        for arg in itertools.product(self.__rows, self.__cols, self.__vals):
            x, y, v = arg
            if value(self.choices[v][x][y]) == 1:
                yield int(x)-1, int(y)-1, int(v)

    @property
    def optimal(self): return self.problem.status

    def __str__(self):
        grid = []
        for r in self.__rows:
            for c in self.__cols:
                for v in self.__vals:
                    if value(self.choices[v][r][c]) == 1:
                        grid.append(v)
        return '\n'.join(' '.join(map(str, grid[i: i+DIM]))
                         for (i) in range(0, len(grid), DIM))
