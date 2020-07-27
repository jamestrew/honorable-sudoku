from resource import *
from MVC.View.widget_display import WidgetDisplay
from functools import partial
import tkinter as tk


class GameConfigure(tk.Frame, WidgetDisplay):

    def __init__(self, wm, instance):
        super().__init__()

        self.__wdisplay = instance
        self.__delta_state = False  # change-config state
        self.__modes = {
            USER_PLAY: "user",
            COMP_PLAY: "computer"
        }
        self.__diffs = {
            EASY_DIFF: "easy",
            HARD_DIFF: "hard",
            MAGI_DIFF: "magic"
        }
        self.__mode_select = USER_PLAY
        self.__diff_select = EASY_DIFF

        grp_interact = wm.get_frm_interact()
        grp_feedback = wm.get_frm_feedback()

        grp_interact.grid_columnconfigure(0, weight=1)
        grp_interact.grid_rowconfigure(1, weight=1)
        grp_feedback.grid_columnconfigure(0, weight=1)

        """ HEAD """
        self.__grp_head = tk.Frame(grp_interact, **TRANSPARENT)
        self.__head_markup()
        self.__grp_head.grid(padx=16, pady=(48, 32), sticky="ew")

        """ FOOT """
        self.__grp_foot = tk.Frame(grp_feedback, **TRANSPARENT)
        self.__foot_markup()
        self.__grp_foot.grid(padx=16, pady=(32, 32), sticky="ew")

        """ BODY """
        self.__grp_body = tk.Frame(grp_interact, **TRANSPARENT)
        self.__body_markup()
        self.__grp_body.grid(padx=16, pady=(32, 72), sticky="nsew")

        self.__wdisplay.bind("<Escape>", lambda e: self.cancl_invoke())

    def __head_markup(self):
        self.__grp_head.grid_rowconfigure((0, 1), weight=1)

        frm_navbar = tk.Frame(self.__grp_head, **TRANSPARENT)
        lbl_navbar_abs = tk.Label(frm_navbar, text="/honorable sudoku/", **NAV_BAR)
        lbl_navbar_abs.pack(side=tk.LEFT, fill=tk.X)
        frm_navbar.grid(sticky="ew")
        head_title = tk.Label(self.__grp_head, text="Configuration", **SUBMENU_TITLE)
        head_title.grid(sticky="w")

    def __foot_markup(self):
        self.__grp_head.grid_rowconfigure((0, 1), weight=1)

        foot_note = tk.Label(
            self.__grp_foot, **FOOT_TOOLTIP,
            text="Select a mode and difficulty to start.",
            wraplength=int(self.__wdisplay.wsize_width*(5/8)) - 32,
        )
        foot_note.grid(pady=(0, 6), sticky="w")
        foot_addr = tk.Label(
            self.__grp_foot, **FOOT_TOOLTIP,
            text="Press (change) to select a different mode or difficulty.",
            wraplength=int(self.__wdisplay.wsize_width*(5/8)) - 32,
        )
        foot_addr.grid(pady=(0, 6), sticky="w")

    def __body_markup(self):
        self.__grp_body.grid_columnconfigure(0, weight=1)
        self.__grp_body.grid_rowconfigure(0, weight=1)

        frm_config = tk.Frame(self.__grp_body, **TRANSPARENT)
        frm_config.grid_columnconfigure(2, weight=1)
        frm_config.grid_columnconfigure(1, weight=2)
        frm_config.grid(padx=16, pady=(0, 6), sticky="nsew")

        frm_start = tk.Frame(self.__grp_body, **TRANSPARENT)
        frm_start.grid_columnconfigure((0, 1), weight=1)
        frm_start.grid(padx=16, pady=(0, 6), sticky="sew")

        self.__reset_config(frm_config)

        start_opts = {
            "START": tk.Button(frm_start, text="START"),
            "CANCL": tk.Button(frm_start, text="CANCEL")
        }
        n_start_opts = 0
        for (name, o) in start_opts.items():
            o.config(CMD_CENTER)
            o.grid(
                padx=32, pady=(24, 0), sticky="new", row=0, column=n_start_opts
            )
            o.bind("<Enter>", self.hoverstyle_toggle)
            o.bind("<Leave>", self.hoverstyle_toggle)
            n_start_opts += 1
        start_opts["START"].config(command=self.start_invoke)
        start_opts["CANCL"].config(command=self.cancl_invoke)

    def __reset_config(self, master:tk.Frame):
        for w in master.winfo_children(): w.destroy()  # clean-up before reset
        config_opts = {
            "MODE": [
                tk.Label(master, text="mode:"),
                tk.Label(master, text=f"({self.__modes[self.__mode_select]})"),
                tk.Button(master, text="change")
            ],
            "DIFF": [
                tk.Label(master, text="difficulty:"),
                tk.Label(master, text=f"({self.__diffs[self.__diff_select]})"),
                tk.Button(master, text="change")
            ]
        }
        # iterable enum(config_opts) where the final result is len(config_opts)
        n_config_opts = 0
        for (config, w_lst) in config_opts.items():  # dynamic gen of settings
            (hdr, cur, chg) = range(len(w_lst))  # enum of widgets
            # ( formatting )
            w_lst[hdr].config(**TBL_HDR)
            w_lst[cur].config(**TBL_DEFAULT_CVAL)
            w_lst[chg].config(
                **CMD_UPDATE,
                command=partial(self.__change_config, master, n_config_opts, len(w_lst))
            )
            # ( painting onto options layout )
            w_lst[hdr].grid(  # header
                padx=(0, 16), pady=(2, 6), sticky="nw",
                row=n_config_opts, column=hdr
            )
            w_lst[cur].grid(  # current selection
                padx=(0, 16), pady=(2, 6), sticky="nw",
                row=n_config_opts, column=cur
            )
            w_lst[chg].grid(padx=(0, 64), pady=(2, 6), row=n_config_opts, column=chg, sticky="ne")
            # ( next setting )
            n_config_opts += 1

    def __change_config(self, master:tk.Frame, select:int, span:int):
        # disallow multiple change states
        if self.__delta_state: self.__reset_config(master)
        self.__delta_state = True  # entering change-config mode

        # clear selected configuration-row
        delta_prop = master.winfo_children()[select*span + 1: span*(select+1)]
        for w in delta_prop: w.destroy()

        # options span right-hand side of config header
        frm_delta = tk.Frame(master, **TRANSPARENT)
        frm_delta.grid(row=select, column=1, sticky="ew", columnspan=2)
        delta_opts = {
            0: {
                "USER": tk.Button(frm_delta, text="user"),
                "COMP": tk.Button(frm_delta, text="computer")
            },
            1: {
                "EASY": tk.Button(frm_delta, text="easy"),
                "HARD": tk.Button(frm_delta, text="hard"),
                "MAGI": tk.Button(frm_delta, text="magic")
            }
        }.get(select)
        n_delta_opts = 0
        for (name, o) in delta_opts.items():
            o.config(width=(9 if select else 12), **CMD_UPDATE)
            o.config(command=partial(self.diff_invoke if select else self.mode_invoke, master, n_delta_opts))
            o.grid(padx=(0, 6), pady=(2, 6), row=0, column=n_delta_opts, sticky="w")
            n_delta_opts += 1

    # METHODS ( PUBLIC ):
    def mode_invoke(self, master, mode):
        self.__delta_state = False  # leaving change-config mode
        self.__mode_select = mode
        self.__reset_config(master)

    def diff_invoke(self, master, diff):
        self.__delta_state = False  # leaving change-config mode
        self.__diff_select = diff
        self.__reset_config(master)

    def start_invoke(self):
        self.__wdisplay.page_destroy()
        self.__wdisplay.callback(load_game=(self.__mode_select, self.__diff_select))
        self.__wdisplay.open_page("Game")

    def cancl_invoke(self):
        self.__wdisplay.page_destroy()
        self.__wdisplay.open_page("Menu")
