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
            "Main":    Main(root_container, self)  # noqa
        }
        # Formatting
        self.get_page("Startup").grid(row=0, column=0, sticky="ns")
        self.get_page("Main").grid(row=0, column=0, sticky="ns")

        self.show_frame("Startup")

    # METHODS ( PUBLIC ):
    def callback(self, *args, **kwargs):
        # callable methods are public attrs of Controller
        valid_call = [fn for fn in dir(self.__request) if fn[:1]!='_']
        rtns = []  # result of callback returns

        # ( STAGE 1 - check valid callback )
        for (fn,params) in kwargs.items():
            if fn not in valid_call: raise KeyError(
                f"callback to Sudoku::Controller.{fn} failed."
            )   # Controller.fn DNE

        # ( STAGE 2 - process callback )
        for (fn,params) in kwargs.items():  # callback all
            # Controller.fn(params)
            if isinstance(params, tuple) or isinstance(params, list):
                result = getattr(self.__request, fn)(*iter(params))
            else:  # at least one argument exists
                result = getattr(self.__request, fn)(params)
            if not(result is None): rtns.append(result)  # collect all returns

        if len(rtns) < 2:
            # single callback- unwrap return
            return None if len(rtns)==0 else rtns.pop()
        # multiple callbacks wrapped in list
        return rtns

    def show_frame(self, page_name):
        """ Show a frame for a given page name """
        frame = self.__frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        return self.__frames[page_name]

    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (row:{x}, col:{y}) to {val}.")


from Frames.menu import Startup  # noqa
from Frames.game import Main     # noqa
