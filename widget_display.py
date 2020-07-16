from view import View
import tkinter as tk


class WidgetDisplay(tk.Tk, View):
    """ Sudoku::WidgetDisplay """

    def __init__(self, handle=None, *args, **kwargs):
        super().__init__()
        self.__request = handle

        root_container = tk.Frame(self)
        root_container.pack(side="top", fill="both", expand=True)
        root_container.grid_rowconfigure(0, weight=1)
        root_container.grid_columnconfigure(0, weight=1)

        # key=page_name, val=page_object
        self.__frames = {  # Instantiate all frames
            "Startup": Startup(root_container, self),
            "Main":    Main(root_container, self)
        }
        # Formatting
        self.get_page("Startup").grid(row=0, column=0, sticky="ns")
        self.get_page("Main").grid(row=0, column=0, sticky="ns")

        self.show_frame("Startup")

    # METHODS ( PUBLIC ):
    def callback(self, *args, **kwargs):
        for k,v in kwargs.items():
            if k == "load_game" and isinstance(v, tuple) and len(v)==2:
                gamemode, difficulty = v
                self.__request.load_game(gamemode, difficulty)
            elif k=="init_iterator" and isinstance(v, int):
                return self.__request.init_n(v)
            elif k=="permanent_cell" and isinstance(v,int):
                return self.__request.perm_n(v)
            elif k=="gameboard_update" and isinstance(v, tuple) and len(v)==3:
                x,y,val = v
                return self.__request.gameboard_update(x, y, val)
            else: raise AttributeError
        return None

    def show_frame(self, page_name):
        """ Show a frame for a given page name """
        frame = self.__frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        return self.__frames[page_name]

    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (row:{x}, col:{y}) to {val}.")


from Frames.startup import Startup  # noqa
from Frames.menu import Main        # noqa
