from MVC.View.view import View
from resource import *
from string import digits
import re
import tkinter as tk


class WidgetManager(object):
    """
    Sudoku::WidgetManager
        Container to reference different levels/parents of the app.
        Root frame contains two child frames: frm_interact and frm_feedback.

        All pages depend on the reference to the interact and feedback frames
        upon initialization using WidgetDisplay.open_frame(page_name).
    """

    def __init__(self, root, interact, feedback):
        super().__init__()
        self.__root = root  # app
        self.__interact = interact  # interact wsub
        self.__feedback = feedback  # feedback wsub

    # Fetch ref to parent widgets
    def get_frm_root(self): return self.__root
    def get_frm_interact(self): return self.__interact
    def get_frm_feedback(self): return self.__feedback


class WidgetDisplay(tk.Tk, View):
    """
    Sudoku::View::WidgetDisplay
        A display using tkinter.
        Upon initialization, mainloop() must be started outside the instance
        declaration.

        This class handles all callbacks to Controller from every page.
        All notififications are forwarded to the respective page/Frame classes.
    """

    def __init__(self, handle=None):
        super().__init__()

        self.__request = handle     # callback ref to Controller

        self.title("honorable-sudoku")
        self.__wsize(justify="MID")

        # ( main container )
        frm_root = tk.Frame(self, **ROOT)
        frm_root.pack(**P_FILL)     # fills entire window
        frm_root.grid_columnconfigure(0, weight=1)

        # ( main interact and feedback containers )
        interact_w, interact_h = (  # dimension-calc of interact frame
            int(self.wsize_width*(5/8)),
            int(self.wsize_height*(2/3)) - 18
        )
        feedback_w, feedback_h = (  # dimension-calc of feedback frame
            int(self.wsize_width*(5/8)),
            int(self.wsize_height*(1/3) - 18)
        )
        grp_interact = tk.Frame(frm_root, width=interact_w, height=interact_h, **GRP_INTERACT)
        grp_feedback = tk.Frame(frm_root, width=feedback_w, height=feedback_h, **GRP_FEEDBACK)
        grp_interact.grid_propagate(False)      # prevent resize of containers in presence of wchildren
        grp_feedback.grid_propagate(False)
        grp_interact.grid(**G_MENU_INTERACT)    # baseline established for all pages
        grp_feedback.grid(**G_MENU_FEEDBACK)
        """
            All wchildren past this point are considered page elements
            All wchildren are destroyed upon page_destroy()
        """
        # ( saving refs to main containers )
        self.__w_mgr = WidgetManager(frm_root, grp_interact, grp_feedback)

        # key=page_name, val=page_object
        self.__frames = {  # Instantiate all frames
            "Menu": Menu,                   # main menu
            "Game": Game,                   # game screen
            "GameConfigure": GameConfigure  # game configuration
        }
        self.cur_frame = None   # current page in view
        self.open_page("Menu")  # entry-point

    # METHODS ( PRIVATE ):
    def __wsize(self, width:int = 1280, height:int = 800, *args, **kwargs):
        """
        Adjust geometry of application.
        Creates an unresizeable window with a defined size.

        :param width:   window width    (default=1280)
        :param height:  window height   (default=800)
        :param args:    (n/a)
        :param kwargs:  options to `justify` window on system screen using str.

        :keyword justify: [ "MID", "LHS", "RHS" ]

        :raises KeyError: no recognized option was given
        """
        self.__user_res = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.__scrn_res = (width, height)
        user_w, user_h = self.__user_res[W], self.__user_res[H]  # system res
        scrn_w, scrn_h = self.__scrn_res[W], self.__scrn_res[H]  # window res

        """
        H-alignment (x-offset) is dependent on justification arg.
        V-alignment (y-offset) is always centered.
        """
        x_offset, y_offset = (12, 32)       # avoid overlap with system taskbar/menubar
        h_align = ["MID", "LHS", "RHS"]     # options for justify kwarg
        for (kw, arg) in kwargs.items():
            # keyword justify matched with valid arg-type
            if kw == "justify" and isinstance(arg, str) and arg in h_align:
                # ( alignment )
                x_offset = {
                    h_align[0]: max(x_offset, user_w//2 - scrn_w//2),
                    h_align[1]: x_offset,
                    h_align[2]: user_w - scrn_w - x_offset
                }.get(arg)
                y_offset = max(y_offset, user_h//2 - scrn_h//2)
            else: raise KeyError(f"justify options: MID, LHS, RHS.")
        # ( setting geometric properties )
        metric = f"{scrn_w}x{scrn_h}+{x_offset}+{y_offset}"
        self.geometry(metric)
        self.resizable(False, False)

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        if self.cur_frame is None: return   # a page must be open
        self.cur_frame.notify(x, y, val)    # notify the page of successful update

    def open_page(self, page_name:str):
        """
        Initializes the page view for the specified page_name given.
        Page elements are appended to the main containers: frm_interact, frm_feedback.

        :param page_name: see self.__frames for page map
        """
        # ( page constructor called )
        self.cur_frame = self.__frames[page_name](self.__w_mgr, self)

    def page_destroy(self):
        """
        Destroys the page view by destroying all main-container children.
        All binds to the app are removed manually. Binds by individual pages are
        not tracked; thus, new binds must be added below.
        """
        # ( destruction of wchildren )
        frm_interact = self.__w_mgr.get_frm_interact()  # get interact container
        frm_feedback = self.__w_mgr.get_frm_feedback()  # get feedback container
        for w in frm_interact.winfo_children():
            w.destroy()  # interact page elements
        for w in frm_feedback.winfo_children():
            w.destroy()  # feedback page elements
        # ( unbind all mouse-keyboard )
        self.unbind("<Escape>")     # ESCAPE
        self.unbind("<Button-1>")   # MOUSE1
        self.unbind("<Button-2>")   # MOUSE2
        [   # NUMKEYS
            self.unbind(num) for num in digits
        ]

    def close_app(self):
        """
        Destroys main containers for clean sys.exit.
        Reference to WidgetDisplay is removed to prevent static method calls, and
        access to memory that is now invalid.
        """
        self.page_destroy()  # clean exit
        self.__w_mgr.get_frm_root().destroy()
        del self  # mem access denied from this point
        exit()    # kill process

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

        if len(rtns) < 2:  # single callback, unwrap return
            return None if len(rtns) == 0 else rtns.pop()
        return rtns         # multiple callbacks wrapped in list

    @property   # window width
    def wsize_width(self): return self.__scrn_res[W]

    @property   # window height
    def wsize_height(self): return self.__scrn_res[H]

    @staticmethod
    def hoverstyle_toggle(event):
        """
        Updates the style of the widget that is bound by this hover-toggle.

        :param event: event listener
        """
        # Parsing event name from eventlistener
        event_name = re.search(r"(?<=<)([A-Za-z]+)", str(event)).group()
        {   # Filter dictionary for hover events
            "Enter": lambda: [  # <Enter> event
                event.widget.config(**CMD_HOVER_ACTIVE),
            ],
            "Leave": lambda: [  # <Leave> event
                event.widget.config(**CMD_HOVER_INACTIVE),
            ]
        }.get(event_name)()  # Configure widget based on state of eventlistener


""" PAGE IMPORTS """
from Pages.menu import Menu                     # noqa: E402
from Pages.game_configure import GameConfigure  # noqa: E402
from Pages.game import Game                     # noqa: E402
