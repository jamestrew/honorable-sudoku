from resource import *
from view import View
import tkinter as tk
import sys


class WidgetDisplay(tk.Tk, View):

    def __init__(self, handle=None, *args, **kwargs):
        super().__init__()
        self.__request = handle

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["Startup"] = Startup(parent=container, controller=self, handle=self.__request)
        self.frames["Main"] = Main(parent=container, controller=self, handle=self.__request)

        self.frames["Startup"].grid(row=0, column=0, sticky='ns')
        self.frames["Main"].grid(row=0, column=0, sticky='ns')

        self.show_frame("Startup")

    def show_frame(self, page_name):
        ''' Show a frame for a given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (col:{x}, row:{y}) to {val}.")

    def set_gamemode(self):
        """
        set_gamemode() is a TEMPORARY method (to be removed)
            A request is sent to the controller to update the gamemode.

        IMPORTANT:
            The button is updated instantly, but should not be updated here!
            Request methods in Controller should return bool indiciating successful update, and
            should only update view after ensuring True is returned (kinda like server requests).

            This applies only if the data is tied to the Model or Controller states.
            self.__accumulator is not tied to either; thus, it may be updated here directly.
            Upon receiving False, the View may need to revert to an earlier state.
        """
        self.__accumulator += 1
        self.maindiv.winfo_children()[0].configure(text=self.__accumulator)  # dangerous update
        self.__request.gamemode_update(self.__accumulator)


class Startup(tk.Frame, View):
    '''
    Display for the Startup. Shown first first game is run.
    Enables the selection of gamemode and puzzle type/difficulty.

    PLAY button is disabled until user select and gamemode and difficulty
    '''

    def __init__(self, parent, controller, handle=None):
        super().__init__(parent)
        self.controller = controller
        self.__request = handle
        self.gamemode = None
        self.difficulty = None

        bg_frame = tk.Frame(self, width=675, height=675,
                            bg=BLACK, bd=5
                            )
        bg_frame.grid(padx=75, pady=(75, 120))
        bg_frame.grid_rowconfigure(0, weight=1)
        bg_frame.grid_columnconfigure(0, weight=1)

        start_frame = tk.Frame(bg_frame, width=675, height=675, bg=WHITE)
        start_frame.grid()

        title = tk.Label(start_frame, text="GAYDOKU", bg=WHITE,
                         fg=BLACK, font=FONTS[55]
                         )
        title.grid(padx=10, pady=10)

        # GAMEMODE SELECT
        def set_gamemode(mode):
            ''' Configure buttons and sets gamemode '''
            self.gamemode = mode
            computer_button.configure(relief='raised')
            user_button.configure(relief='raised')
            if mode == 1:
                computer_button.configure(relief='sunken')
            else:
                user_button.configure(relief='sunken')
            check_play()

        mode_frame = tk.Frame(start_frame, bg=WHITE)
        mode_frame.grid(row=1, padx=5, pady=5)
        tk.Label(mode_frame, text="MODE: ", bg=WHITE, fg=BLACK,
                 font=FONTS[30]
                 ).grid()

        computer_button = tk.Button(mode_frame, text='COMP PLAY', bg=WHITE, fg=BLACK,
                                    font=FONTS[25], command=lambda: set_gamemode(1)
                                    )
        user_button = tk.Button(mode_frame, text='USER PLAY', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=lambda: set_gamemode(2)
                                )
        computer_button.grid(row=0, column=1, padx=2, pady=2)
        user_button.grid(row=0, column=2, padx=2, pady=2)

        # DIFFICULTY SELECT
        def set_difficulty(diff):
            ''' Configures buttons and sets difficulty '''
            easy_button.configure(relief='raised')
            hard_button.configure(relief='raised')
            magic_button.configure(relief='raised')

            if diff == 1:
                easy_button.configure(relief='sunken')
                self.difficulty = 'Boards/easy.txt'
            elif diff == 2:
                hard_button.configure(relief='sunken')
                self.difficulty = 'Boards/hard.txt'
            else:
                magic_button.configure(relief='sunken')
                self.difficulty = 'Boards/magic.txt'
            check_play()

        diff_frame = tk.Frame(start_frame, bg=WHITE)
        diff_frame.grid(row=2, padx=5, pady=5)
        tk.Label(diff_frame, text="MODE: ", bg=WHITE, fg=BLACK,
                 font=FONTS[30]
                 ).grid()

        easy_button = tk.Button(diff_frame, text='EASY', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=lambda: set_difficulty(1)
                                )
        hard_button = tk.Button(diff_frame, text='HARD', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=lambda: set_difficulty(2)
                                )
        magic_button = tk.Button(diff_frame, text='MAGIC', bg=WHITE, fg=BLACK,
                                 font=FONTS[25], command=lambda: set_difficulty(3)
                                 )
        easy_button.grid(row=0, column=1, padx=2, pady=2)
        hard_button.grid(row=0, column=2, padx=2, pady=2)
        magic_button.grid(row=0, column=3, padx=2, pady=2)

        # PLAY BUTTON
        def play_game():
            ''' Raises all buttons and loads the MAIN game '''
            computer_button.configure(relief='raised')
            user_button.configure(relief='raised')
            easy_button.configure(relief='raised')
            hard_button.configure(relief='raised')
            magic_button.configure(relief='raised')
            self.__request.gamemode_update(self.gamemode)
            self.__request.gameboard_update(self.difficulty)

            page = self.controller.get_page("Main")
            page.init_board()
            controller.show_frame("Main")

        def check_play():
            ''' Enable the PLAY button if gamemode and difficulty are selected'''
            if self.gamemode is not None and self.difficulty is not None:
                play_button.config(state="normal")

        play_button = tk.Button(start_frame, text='PLAY', bg=WHITE, fg=BLACK,
                                font=FONTS[25],
                                command=play_game
                                )
        play_button.config(state="disabled")
        play_button.grid(padx=2, pady=2)

        # EXIT GAME BUTTON
        kill_button = tk.Button(start_frame, text='EXIT GAME', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=sys.exit
                                )
        kill_button.grid(pady=(150, 2))

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (col:{x}, row:{y}) to {val}.")


class Main(tk.Frame, View):
    def __init__(self, parent, controller, handle=None):
        super().__init__(parent)
        self.controller = controller
        self.__request = handle

        bg_frame = tk.Frame(self, width=675, height=675, bg=BLACK, bd=5)
        bg_frame.grid(padx=75, pady=(75, 120))

        self.cells = []
        for i in range(DIM):
            row = []
            yborder = 0.5
            if i % 3 == 0 and i != 0:
                yborder = 5
            for j in range(DIM):
                xborder = 0.5
                if j % 3 == 0 and j != 0:
                    xborder = 5

                cell_frame = tk.Frame(bg_frame, width=75, height=75, bg=WHITE)
                cell_frame.grid(row=i, column=j,
                                padx=(xborder, 0.5),
                                pady=(yborder, 0.5)
                                )
                cell_number = tk.Label(bg_frame, bg=WHITE)
                cell_number.grid(row=i, column=j)
                cell_data = {"number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        exit_button = tk.Button(self, text='EXIT', bg=WHITE, fg=BLACK,
                                font=FONTS[25],
                                command=lambda: controller.show_frame("Startup")
                                )
        exit_button.place(x=75, y=5)

    def init_board(self):
        self.game = self.__request.get_puzzle()
        for i in range(9):
            for j in range(9):
                if self.game[i, j] != 0:
                    cell_val = self.game[i, j]
                else:
                    cell_val = ''
                self.cells[i][j]["number"].configure(bg=WHITE, fg=NUMS,
                                                     text=cell_val, font=FONTS[20]
                                                     )

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (col:{x}, row:{y}) to {val}.")
