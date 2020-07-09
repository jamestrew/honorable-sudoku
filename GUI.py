import tkinter as tk
from resource import *
import sys


class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (Startup, Main):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='ns')

        self.show_frame("Startup")

    def show_frame(self, page_name):
        ''' Show a frame for a given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Startup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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
            '''
            Incomplete function
            Raises/sinks button
            Implement: pass gamemode
            '''
            computer_button.configure(relief='raised')
            user_button.configure(relief='raised')
            if mode == 1:
                computer_button.configure(relief='sunken')
            else:
                user_button.configure(relief='sunken')

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
            '''
            Incomplete function
            Raises/sinks button
            Implement: pass difficulty
            '''
            easy_button.configure(relief='raised')
            hard_button.configure(relief='raised')
            magic_button.configure(relief='raised')

            if diff == 1:
                easy_button.configure(relief='sunken')

            elif diff == 2:
                hard_button.configure(relief='sunken')

            else:
                magic_button.configure(relief='sunken')

        diff_frame = tk.Frame(start_frame, bg=WHITE)
        diff_frame.grid(row=2, padx=5, pady=5)
        tk.Label(diff_frame, text="MODE: ", bg=WHITE, fg=BLACK,
                 font=FONTS[30]
                 ).grid()

        easy_button = tk.Button(diff_frame, text='COMP PLAY', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=lambda: set_difficulty(1)
                                )
        hard_button = tk.Button(diff_frame, text='USER PLAY', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=lambda: set_difficulty(2)
                                )
        magic_button = tk.Button(diff_frame, text='USER PLAY', bg=WHITE, fg=BLACK,
                                 font=FONTS[25], command=lambda: set_difficulty(3)
                                 )
        easy_button.grid(row=0, column=1, padx=2, pady=2)
        hard_button.grid(row=0, column=2, padx=2, pady=2)
        magic_button.grid(row=0, column=3, padx=2, pady=2)

        # PLAY BUTTON
        play_button = tk.Button(start_frame, text='PLAY', bg=WHITE, fg=BLACK,
                                font=FONTS[25],
                                command=lambda: controller.show_frame("Main")
                                )
        play_button.grid(padx=2, pady=2)

        # EXIT GAME BUTTON
        kill_button = tk.Button(start_frame, text='EXIT GAME', bg=WHITE, fg=BLACK,
                                font=FONTS[25], command=sys.exit
                                )
        kill_button.grid(pady=(150, 2))


class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        bg_frame = tk.Frame(self, width=675, height=675, bg=BLACK, bd=5)
        bg_frame.grid(padx=75, pady=(75, 120))

        self.cells = []
        for i in range(9):
            row = []
            yborder = 0.5
            if i % 3 == 0 and i != 0:
                yborder = 5
            for j in range(9):
                xborder = 0.5
                if j % 3 == 0 and j != 0:
                    xborder = 5

                cell_frame = tk.Frame(bg_frame, width=75, height=75, bg=WHITE)
                cell_frame.grid(row=i, column=j,
                                padx=(xborder, 0.5),
                                pady=(yborder, 0.5)
                                )
                cell_number = tk.Label(bg_frame, bg=WHITE, fg=NUMS,
                                       text=i,
                                       font=FONTS[20],
                                       )
                cell_number.grid(row=i, column=j)
                cell_data = {"number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        exit_button = tk.Button(self, text='EXIT', bg=WHITE, fg=BLACK,
                                font=FONTS[25],
                                command=lambda: controller.show_frame("Startup")
                                )
        exit_button.place(x=75, y=5)


# if __name__ == "__main__":
#     app = Game()
#     app.mainloop()
