from resource import *
from MVC.View.widget_display import WidgetDisplay
from functools import partial, update_wrapper
import string
import time
import tkinter as tk

from Pages.Game.grid_manager import GridManager
from Pages.Game.conflict_taskmanager import *


class Game(tk.Frame, WidgetDisplay):
    """
    Sudoku::View::WidgetDisplay::Game
        page_path: "honorable-sudoku/gameconfiguration/game-screen"
        Game screen.
    """

    def __init__(self, wm, instance):
        super().__init__()

        self.__wdisplay = instance

        # ( grid )
        self.__grid = GridManager()     # widget-grid
        self.__selection = None         # selected cell coordinate on widget-grid
        self.__conflict_mgr = ConflictTaskManager(instance)

        # ( stopwatch )
        self.__start = .0
        self.__elapsedtime = .0
        self.__running = False
        self.timestr = tk.StringVar()   # mutable time string
        self.__stopwatch_start()        # start stopwatch

        # fetching main containers
        grp_interact = wm.get_frm_interact()
        grp_feedback = wm.get_frm_feedback()
        # configuring main containers
        grp_interact.grid_columnconfigure(0, weight=1)
        grp_interact.grid_rowconfigure(1, weight=1)
        grp_feedback.grid_columnconfigure(0, weight=1)

        """ HEAD """
        self.__grp_head = tk.Frame(grp_interact, **TRANSPARENT)
        self.__head_markup()
        self.__grp_head.grid(padx=16, pady=(48, 16), sticky="ew")

        """ FOOT """
        self.__grp_foot = tk.Frame(grp_feedback, **TRANSPARENT)
        self.__foot_markup()
        self.__grp_foot.grid(padx=16, pady=(32, 32), sticky="ew")

        """ BODY """
        self.__grp_body = tk.Frame(grp_interact, **TRANSPARENT)
        self.__body_markup()
        self.__grp_body.grid(padx=16, pady=(16, 16), sticky="nsew")

        # ( bindings )
        self.__wdisplay.bind("<Button-1>", self.select_cell)    # MOUSE1
        [  # NUMKEYS bound to gameboard_update (try_cell)
            self.__wdisplay.bind(num, self.try_cell) for num in string.digits
        ]

    def __stopwatch_update(self):
        self.__elapsedtime = time.time() - self.__start
        self.__stopwatch_settime(self.__elapsedtime)
        self.__timer = self.__wdisplay.after(1000, self.__stopwatch_update)

    def __stopwatch_settime(self, elap):
        mins = int(elap/60)
        secs = int(elap - mins*60.0)
        self.timestr.set(f"{mins:02d}:{secs:02d}")

    def __stopwatch_start(self):
        if self.__running: return
        self.__start = time.time() - self.__elapsedtime
        self.__stopwatch_update()
        self.__running = True

    def __stopwatch_stop(self):
        if not self.__running: return
        self.__wdisplay.after_cancel(self._timer)
        self.__elapsedtime = time.time() - self.__start
        self.__stopwatch_settime(self.__elapsedtime)
        self.__running = False

    def __stopwatch_reset(self):
        self.__start = time.time()
        self.__elapsedtime = .0
        self.__stopwatch_settime(self.__elapsedtime)

    def __head_markup(self):
        self.__grp_head.columnconfigure((0, 1), weight=1)

        # ( breadcrumb navigation )
        frm_navbar = tk.Frame(self.__grp_head, **TRANSPARENT)
        frm_navbar.grid(sticky="ew")

        lbl_navbar_root = tk.Label(frm_navbar, text="/honorable sudoku", **NAV_BAR)
        lbl_navbar_root.pack(side=tk.LEFT, fill=tk.Y)
        lbl_navbar_intr = tk.Label(frm_navbar, text="/configuration", **NAV_BAR)
        lbl_navbar_intr.pack(side=tk.LEFT, fill=tk.Y)
        lbl_navbar_curr = tk.Label(frm_navbar, text="/play", **NAV_BAR)
        lbl_navbar_curr.pack(side=tk.LEFT, fill=tk.Y)

        lbl_navbar_root.bind("<Enter>", self.hoverstyle_toggle)
        lbl_navbar_root.bind("<Leave>", self.hoverstyle_toggle)
        lbl_navbar_intr.bind("<Enter>", self.hoverstyle_toggle)
        lbl_navbar_intr.bind("<Leave>", self.hoverstyle_toggle)
        lbl_navbar_root.bind("<Button-1>", self.navbar_root_invoke)
        lbl_navbar_intr.bind("<Button-1>", self.navbar_gc_invoke)

        # ( stopwatch )
        frm_stopwatch = tk.Frame(self.__grp_head, **TRANSPARENT)
        frm_stopwatch.grid_columnconfigure(0, weight=1)
        frm_stopwatch.grid_rowconfigure(0, weight=1)
        frm_stopwatch.grid(row=0, column=1, sticky="ns")

        lbl_stopwatch = tk.Label(frm_stopwatch, textvariable=self.timestr, **NAV_BAR)
        lbl_stopwatch.pack(side=tk.LEFT, fill=tk.Y)
        self.__stopwatch_settime(self.__elapsedtime)  # seems redundant. stopwatch runs fine without it?

    def __foot_markup(self):
        pass

    def __body_markup(self):
        self.__grp_body.grid_columnconfigure(0, weight=1)
        self.__grp_body.grid_rowconfigure(0, weight=1)

        # ( widget-grid )
        # outline frame envelopes the grid view
        frm_outline = tk.Frame(self.__grp_body, bg=XIKETIC)
        frm_outline.grid()
        frm_grid = tk.Frame(frm_outline, bg=XIKETIC)
        frm_grid.grid(padx=PAD_THIC, pady=PAD_THIC)

        # ( instantiating grid with loaded puzzle )
        for c in range(DIM*DIM):
            # reading constants
            x, y = (c//DIM, c%DIM)
            padx = (PAD_THIC if (y>0 and y%SUB == 0) else PAD_THIN, PAD_THIN)
            pady = (PAD_THIC if (x>0 and x%SUB == 0) else PAD_THIN, PAD_THIN)
            value = self.__wdisplay.callback(init_next=None)
            locked = self.__wdisplay.callback(lock_check=(x, y))

            # background of cell
            frm_cell = tk.Frame(frm_grid, **CELL_BG)
            frm_cell.grid_columnconfigure(0, weight=1)
            frm_cell.grid_rowconfigure(0, weight=1)
            frm_cell.grid_propagate(False)
            frm_cell.grid(row=x, column=y, padx=padx, pady=pady)
            # foreground of cell
            lbl_cell = tk.Label(
                frm_cell,
                **(CELL_FG_LOCK if locked else CELL_FG),
                text=(value if value>0 else "")
            )
            lbl_cell.grid()
            # track (bg, fg)-widget pair
            self.__grid.append(frm_cell, lbl_cell)

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        self.__grid.update(x, y, val)
        complete = self.__wdisplay.callback(check_win=None)
        if complete: self.navbar_root_invoke(None)

    def select_cell(self, event):
        """
        Detects mouse input to provide feedback of cell selection.
        :param event: event listener
        """

        master = event.widget.master if isinstance(event.widget, tk.Label) \
            else event.widget  # bypass value-label
        try:
            select_info = master.grid_info()  # dict(property, value)
            select_prev = self.__selection    # previous highlight

            x, y = (select_info["row"], select_info["column"])
            depth = master.winfo_parent().count('!') + 1
        except (AttributeError, KeyError): return  # invalid grid_info
        else:  # assign new selection on correct frame-depth
            if depth == self.__grid.w_depth:
                self.__selection = (x, y)
        # Highlight selection
        if select_prev is not None:  # Unselect previous cell
            self.__grid.background(*select_prev).config(**CELL_BG)
            self.__grid.foreground(*select_prev).config(**CELL_BG)
        if self.__selection is not None:
            self.__grid.background(*self.__selection).config(**CELL_SELECT)
            self.__grid.foreground(*self.__selection).config(**CELL_SELECT)

    def try_cell(self, event):
        """
        Tries a gameboard_update callback on the selected cell.
        A failed update highlights all cells that are causing the conflicts.
        Notify is called by Controller upon successful update to the puzzle.
        :param event: event listener
        """
        value = int(event.char)
        conflicts = self.__wdisplay.callback(
            fetch_conflicts=(*self.__selection, value)
        )

        def wrapped_partial(func, *args, **kwargs):
            partial_func = partial(func, *args, **kwargs)
            update_wrapper(partial_func, func)
            return partial_func

        # clear/revert all conflict highlights after 1 sec.
        self.__conflict_mgr.queue(
            *self.__selection,
            value,  # pair with value in which task refers to
            self.__wdisplay.after(1000, wrapped_partial(
                self.reset_conflicts, *self.__selection, value, conflicts
            ))
        )
        self.toggle_conflicts(value, conflicts)  # highlight all conflicts
        self.__wdisplay.callback(gameboard_update=(*self.__selection, value))

    def toggle_conflicts(self, value, conflict_coords, revert=False):
        for c in conflict_coords:
            # reading constants
            x, y = c
            # highlight conflicts
            self.__grid.background(x, y).config(bg=CHAMPAGNE_PINK if revert else POPSTAR)
            self.__grid.foreground(x, y).config(bg=CHAMPAGNE_PINK if revert else POPSTAR)

    def navbar_root_invoke(self, event):
        del self.__conflict_mgr
        self.__wdisplay.page_destroy()
        self.__wdisplay.open_page("Menu")

    def navbar_gc_invoke(self, event):
        del self.__conflict_mgr
        self.__wdisplay.page_destroy()
        self.__wdisplay.open_page("GameConfigure")

    def reset_conflicts(self, x:int, y:int, value, conflict_coords):
        self.toggle_conflicts(value, conflict_coords, revert=True)
        self.__conflict_mgr.dequeue(x, y, value)
