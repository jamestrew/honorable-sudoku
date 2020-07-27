from resource import *
import tkinter as tk


class GridManager(object):
    """
    Sudoku::GridManager
        Keeps track of the foreground and background widgets of each cell of
        the grid. Helps to manage updates to the collection of cells.
    """
    def __init__(self):
        # Enum of bg and fg of each element of grid
        self.g_ref = {"bg": 0, "fg": 1}
        self.__grid = []  # insertion order maintained

    def append(self, master:tk.Frame, value:tk.Label):
        """
        Adds the (bg, fg)-widget reference pair to the grid.
        :param master:  refers to the background element
        :param value:   refers to the foregorund element
        """
        self.__grid.append((master, value))

    def background(self, x:int, y:int) -> tk.Frame:
        return self.__grid[x*DIM + y][self.g_ref.get("bg")]

    def foreground(self, x:int, y:int) -> tk.Label:
        return self.__grid[x*DIM + y][self.g_ref.get("fg")]

    def update(self, x:int, y:int, val:int):
        self.foreground(x, y).config(text=(val if val>0 else ""))

    @property   # returns depth of cell frame relative to winfo_toplevel()
    def w_depth(self) -> int:
        leaf = self.__grid[0][self.g_ref.get("fg")]
        # the widget pathname is separated by exclamation points
        return leaf.winfo_parent().count('!')  # determining the depth
