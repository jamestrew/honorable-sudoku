from view import View
from resource import *
import re
import string
import tkinter as tk


class WidgetManager(object):

    def __init__(self, root, interact, feedback):
        super().__init__()
        self.__root = root  # app
        self.__interact = interact  # interact wsub
        self.__feedback = feedback  # feedback wsub

    def get_frm_root(self): return self.__root
    def get_frm_interact(self): return self.__interact
    def get_frm_feedback(self): return self.__feedback


class WidgetDisplay(tk.Tk, View):
    """ Sudoku::WidgetDisplay """

    def __init__(self, handle=None, *args, **kwargs):
        super().__init__()

        self.__request = handle

        self.title("honorable-sudoku")
        self.__wsize(justify="MID")

        frm_root = tk.Frame(self, **ROOT)
        frm_root.pack(**P_FILL)
        frm_root.grid_columnconfigure(0, weight=1)
        interact_w, interact_h = (
            int(self.wsize_width*(5/8)),
            int(self.wsize_height*(2/3)) - 18
        )
        feedback_w, feedback_h = (
            int(self.wsize_width*(5/8)),
            int(self.wsize_height*(1/3) - 18)
        )

        grp_interact = tk.Frame(frm_root, width=interact_w, height=interact_h, **GRP_INTERACT)
        grp_feedback = tk.Frame(frm_root, width=feedback_w, height=feedback_h, **GRP_FEEDBACK)
        grp_interact.grid_propagate(False)
        grp_feedback.grid_propagate(False)
        grp_interact.grid(**G_MENU_INTERACT)
        grp_feedback.grid(**G_MENU_FEEDBACK)

        self.__w_mgr = WidgetManager(frm_root, grp_interact, grp_feedback)

        # key=page_name, val=page_object
        self.__frames = {  # Instantiate all frames
            "Menu": Menu,  # main-menu
            "Game": Game,  # play screen
            "GameConfigure": GameConfigure  # pre-game config
        }
        self.cur_frame = None
        self.open_frame("Menu")  # view entry-point

    # METHODS ( PRIVATE ):
    def __wsize(self, width=1280, height=800, *args, **kwargs):
        self.__user_res = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.__scrn_res = (width, height)
        user_w, user_h = self.__user_res[W], self.__user_res[H]  # system res
        scrn_w, scrn_h = self.__scrn_res[W], self.__scrn_res[H]  # window res

        x_offset, y_offset = (12, 32)
        h_align = ["MID", "LHS", "RHS"]
        for (kw, arg) in kwargs.items():
            if kw == "justify" and isinstance(arg, str) and arg in h_align:
                x_offset = {
                    h_align[0]: max(x_offset, user_w//2 - scrn_w//2),
                    h_align[1]: x_offset,
                    h_align[2]: user_w - x_offset
                }.get(arg)
                y_offset = max(y_offset, user_h//2 - scrn_h//2)
            else: raise KeyError(f"justify options: MID, LHS, RHS.")

        metric = f"{scrn_w}x{scrn_h}+{x_offset}+{y_offset}"
        self.geometry(metric)
        self.resizable(False, False)

    # METHODS ( PUBLIC ):
    def open_frame(self, page_name:str):
        """
        Initializes interact and/or feedback frames.

        :param page_name: see self.__frames for mapping
        """
        self.cur_frame = self.__frames[page_name](self.__w_mgr, self)

    def frame_destroy(self):
        frm_interact = self.__w_mgr.get_frm_interact()
        frm_feedback = self.__w_mgr.get_frm_feedback()
        for w in frm_interact.winfo_children():
            w.destroy()
        for w in frm_feedback.winfo_children():
            w.destroy()
        self.unbind("<Escape>")
        self.unbind("<Button-1>")
        self.unbind("<Button-2>")
        [
            self.unbind(num) for num in string.digits
        ]
        self.unbind("<space>")

    def close_app(self):
        self.frame_destroy()  # clean exit
        self.__w_mgr.get_frm_root().destroy()
        del self  # mem access denied from this point
        exit()

    def notify(self, x, y, val, /):
        if self.cur_frame is None: return
        self.cur_frame.notify(x, y, val)

    def callback(self, *args, **kwargs):
        """
        Main access to the Controller instance for requests to mutate Puzzle.
        Valid callback attributes include all public methods of Controller.

        :raises KeyError: if callback function does not exist
        :param args: (n/a)
        :param kwargs: request.keyword(args)
        :return: the returns of each callback are forwarded
        """
        if len(args) > 0: raise KeyError(f"callback requires keyword for all requests.")

        # callable methods are public attrs of Controller
        valid_call = [fn for fn in dir(self.__request) if fn[:1] != '_']
        rtns = []  # result of callback returns

        # ( STAGE 1 - check valid callback )
        for (fn, params) in kwargs.items():
            if fn not in valid_call: raise KeyError(
                f"callback to Sudoku::Controller.{fn} failed."
            )  # Controller.fn DNE

        # ( STAGE 2 - process callback )
        for (fn, params) in kwargs.items():  # callback all
            if isinstance(params, tuple) or isinstance(params, list):
                # expansion of multiple arguments
                result = getattr(self.__request, fn)(*iter(params))
            elif params is not None:  # one argument exists
                result = getattr(self.__request, fn)(params)
            else:  # no parameters exist
                result = getattr(self.__request, fn)()
            if not (result is None): rtns.append(result)  # collect all returns

        if len(rtns) < 2:
            # single callback, unwrap return
            return None if len(rtns) == 0 else rtns.pop()
        # multiple callbacks wrapped in list
        return rtns

    @property
    def wsize_width(self): return self.__scrn_res[W]

    @property
    def wsize_height(self): return self.__scrn_res[H]

    @staticmethod
    def hoverstyle_toggle(event):
        event_name = re.search(r"(?<=<)([A-Za-z]+)", str(event)).group()
        {
            "Enter": lambda: [
                event.widget.config(**CMD_HOVER_ACTIVE),
            ],
            "Leave": lambda: [
                event.widget.config(**CMD_HOVER_INACTIVE),
            ]
        }.get(event_name)()


from Frames.menu import Menu                     # noqa: E402
from Frames.game_configure import GameConfigure  # noqa: E402
from Frames.game import Game                     # noqa: E402
