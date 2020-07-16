import sys
from resource import *
from widget_display import WidgetDisplay
import tkinter as tk


class Startup(tk.Frame, WidgetDisplay):
    """
    Sudoku::WidgetDisplay::Startup
        Display for the Startup screen. Always shown first when WidgetDisplay
        is instantiated. It enables the selection of gamemode and difficulty.
        Requires:
        - To proceed using PLAY command, user must select gamemode and difficulty.
        Affects:
        - Controller.gamemode
        - Controller.difficulty
    """
    # selection within groups specified below
    __gamemode = None
    __difficulty = None

    __btn_modes = None  # modes group
    __btn_diffs = None  # difficulty group
    __btn_start = None  # start button

    def __init__(self, root, instance):
        super().__init__(root)
        self.__root_instance = instance

        # background
        bg = tk.Frame(self, width=675, height=675, bg=BLACK, bd=5)
        bg.grid(padx=75, pady=(75, 120))
        bg.grid_rowconfigure(0, weight=1)
        bg.grid_columnconfigure(0, weight=1)

        start_frame = tk.Frame(bg, width=675, height=675, bg=WHITE)
        start_frame.grid()

        title = tk.Label(
            start_frame, bg=WHITE, fg=BLACK, text="GAYDOKU", font=CMD_HELVETICA[55]
        )
        title.grid(padx=10, pady=10)

        # MODE
        mode_frame = tk.Frame(start_frame, bg=WHITE)
        tk.Label(  # MODE HEADER
            mode_frame, text="MODE: ", bg=WHITE, fg=BLACK, font=CMD_HELVETICA[30]
        ).grid()
        self.__btn_modes = {
            USER_PLAY: tk.Button(mode_frame, text='USER PLAY', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25]),
            COMP_PLAY: tk.Button(mode_frame, text='COMP PLAY', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25])
        }
        mode_frame.grid(row=1, padx=5, pady=5)
        self.__btn_modes[USER_PLAY].grid(row=0, column=1, padx=2, pady=2)
        self.__btn_modes[COMP_PLAY].grid(row=0, column=2, padx=2, pady=2)

        # DIFFICULTY
        diff_frame = tk.Frame(start_frame, bg=WHITE)
        tk.Label(
            diff_frame, text="DIFFICULTY: ", bg=WHITE, fg=BLACK, font=CMD_HELVETICA[30]
        ).grid()
        self.__btn_diffs = {
            EASY: tk.Button(diff_frame, text='EASY', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25]),
            HARD: tk.Button(diff_frame, text='HARD', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25]),
            MAGI: tk.Button(diff_frame, text='MAGIC', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25])
        }
        diff_frame.grid(row=2, padx=5, pady=5)
        self.__btn_diffs[EASY].grid(row=0, column=1, padx=2, pady=2)
        self.__btn_diffs[HARD].grid(row=0, column=2, padx=2, pady=2)
        self.__btn_diffs[MAGI].grid(row=0, column=3, padx=2, pady=2)

        option_btns = [*list(self.__btn_modes.values()), *list(self.__btn_diffs.values())]
        play_button = tk.Button(
            start_frame, text='PLAY', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25], state="disabled",
            command=lambda: self.play_game(option_btns)
        )
        play_button.grid(padx=2, pady=2)
        self.__btn_start = play_button

        self.__btn_diffs[EASY].config(command=lambda: [
            self.set_difficulty(0, list(self.__btn_diffs.values())),
            self.check_play(self.__btn_start)
        ])
        self.__btn_diffs[HARD].config(command=lambda: [
            self.set_difficulty(1, list(self.__btn_diffs.values())),
            self.check_play(self.__btn_start)
        ])
        self.__btn_diffs[MAGI].config(command=lambda: [
            self.set_difficulty(2, list(self.__btn_diffs.values())),
            self.check_play(self.__btn_start)
        ])

        self.__btn_modes[USER_PLAY].config(command=lambda: [
            self.set_gamemode(0, list(self.__btn_modes.values())),
            self.check_play(self.__btn_start)
        ])
        self.__btn_modes[COMP_PLAY].config(command=lambda: [
            self.set_gamemode(1, list(self.__btn_modes.values())),
            self.check_play(self.__btn_start)
        ])

        # EXIT GAME BUTTON
        kill_button = tk.Button(
            start_frame, text='EXIT GAME', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25], command=sys.exit
        )
        kill_button.grid(pady=(150, 2))

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (col:{x}, row:{y}) to {val}.")

    def set_gamemode(self, gamemode, parent=None):
        """ Configures buttons and sets gamemode """
        self.__gamemode = gamemode
        self.group_select(gamemode, parent)

    def set_difficulty(self, difficulty, parent=None):
        """ Configures buttons and sets difficulty """
        self.__difficulty = difficulty
        self.group_select(difficulty, parent)

    def check_play(self, play_button=None):
        """ Enables the PLAY button if gamemode and difficulty are selected """
        play_button.config(
            state="disabled"
            if None in[self.__gamemode, self.__difficulty] else "normal"
        )

    def play_game(self, buttons):
        """ Raises all buttons and loads the MAIN game """
        self.group_select(-1, buttons)
        self.__root_instance.callback(
            load_game=(self.__gamemode, self.__difficulty)
        )
        page = self.__root_instance.get_page("Main")
        page.init_board()

        self.__root_instance.show_frame("Main")

    @staticmethod
    def group_select(select, parent=None):
        for (i) in range(len(parent)):
            parent[i].configure(relief="sunken" if select == i else "raised")
