from resource import *
from widget_display import WidgetDisplay
import re
import random
import json
import tkinter as tk


class Menu(tk.Frame, WidgetDisplay):
    """
    Sudoku::WidgetDisplay::Menu
        Display for the main-menu screen. Always shown first when WidgetDisplay
        is instantiated.
        Requires:
        - To proceed using PLAY command, user must select gamemode and difficulty.
        Affects:
        - Controller.gamemode
        - Controller.difficulty
    """

    def __init__(self, wm, instance):
        super().__init__()

        self.__wdisplay = instance

        grp_interact = wm.get_frm_interact()
        grp_feedback = wm.get_frm_feedback()

        grp_interact.grid_columnconfigure(0, weight=1)
        grp_feedback.grid_columnconfigure(0, weight=1)

        """ HEAD """
        self.__grp_head = tk.Frame(grp_interact, **TRANSPARENT)
        self.__head_markup()
        self.__grp_head.grid(padx=16, pady=(48, 32), sticky="ew")

        """ FOOT """
        self.__grp_foot = tk.Frame(grp_feedback, **TRANSPARENT)
        self.__splash_tooltips = dict()
        self.__foot_markup()
        self.__grp_foot.grid(padx=16, pady=(32, 32), sticky="ew")

        """ BODY """
        self.__grp_body = tk.Frame(grp_interact, **TRANSPARENT)
        self.__body_markup()  # dependency: footer markup
        self.__grp_body.grid(padx=16, pady=(24, 72), sticky="ew")

    # METHODS ( PRIVATE ):
    def __head_markup(self, /):
        self.__grp_head.grid_columnconfigure(0, weight=1)
        self.__grp_head.grid_rowconfigure(0, weight=1)

        head_title = tk.Label(self.__grp_head, text="Honorable Sudoku", **MENU_TITLE)
        head_title.grid(sticky="nsew")

    def __foot_markup(self, /):
        self.__grp_head.grid_columnconfigure(0, weight=1)
        self.__grp_head.grid_rowconfigure(0, weight=1)
        foot_tip = tk.Label(
            self.__grp_foot, **FOOT_TOOLTIP,
            wraplength=int(self.__wdisplay.wsize_width*(5/8))-32
        )
        foot_tip.grid()

    def __body_markup(self, /):
        self.__grp_body.grid_columnconfigure(0, weight=1)
        self.__grp_body.grid_rowconfigure((0, 1, 2, 3), weight=1)

        grp_opts = {
            "PLAY": tk.Button(self.__grp_body, text="NEW GAME"),
            "LOAD": tk.Button(self.__grp_body, text="LOAD GAME"),
            "SETT": tk.Button(self.__grp_body, text="SETTINGS"),
            "HELP": tk.Button(self.__grp_body, text="HELP"),
            "EXIT": tk.Button(self.__grp_body, text="EXIT")
        }
        try:
            with open("./Pages/splash.json", encoding="utf-8") as tooltips:
                splash = json.load(tooltips)
            for s in splash:
                self.__splash_tooltips[grp_opts.get(s).winfo_id()] = splash[s]
        except FileNotFoundError:
            for (name, o) in grp_opts.items():
                self.__splash_tooltips[o.winfo_id()] = [f"{name}:<splash message not found>"]

        for (name, o) in grp_opts.items():
            o.config(**CMD_CENTER)
            o.grid(padx=240, pady=(2, 3), sticky="ew")
            o.bind("<Enter>", self.__hoverstyle_toggle)
            o.bind("<Leave>", self.__hoverstyle_toggle)
        grp_opts["PLAY"].config(command=self.play_invoke)
        grp_opts["EXIT"].config(command=self.__wdisplay.close_app)

    def __hoverstyle_toggle(self, event):
        foot_tip = self.__grp_foot.winfo_children()[0]  # dangerous assumption
        event_name = re.search(r"(?<=<)([A-Za-z]+)", str(event)).group()
        {
            "Enter": lambda: [
                event.widget.config(**CMD_HOVER_ACTIVE),
                foot_tip.config(
                    text=random.choice(self.__splash_tooltips.get(event.widget.winfo_id()))
                )
            ],
            "Leave": lambda: [
                event.widget.config(**CMD_HOVER_INACTIVE),
                foot_tip.config(text="")
            ]
        }.get(event_name)()

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (row:{x}, col:{y}) to {val}.")

    def play_invoke(self):
        self.__wdisplay.page_destroy()
        self.__wdisplay.open_page("GameConfigure")
