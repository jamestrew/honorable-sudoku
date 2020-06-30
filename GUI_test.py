import tkinter as tk
from PIL import Image


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Sudoku")

        # main border
        self.main_grid = tk.Frame(self, width=675, height=675,
                                  bg="#000000", bd=5
                                  )
        self.main_grid.grid(padx=75, pady=(75, 225))
        self.start_GUI()
        # self.make_GUI()

        self.mainloop()

    def start_GUI(self):
        start_frame = tk.Frame(self.main_grid, width=675, height=675, bg="#FFFFFF")
        start_frame.grid(row=0, column=0)
        title_label = tk.Label(start_frame, text='GAYDOKU',
                               bg="#FFFFFF", fg="#000000",
                               font=("Helvetica", "55", "bold")
                               )
        title_label.grid(row=0, padx=10, pady=10)

        # gamemode select
        self.gamemode = 0
        mode_frame = tk.Frame(start_frame, width=675, height=150, bg="#FFFFFF")
        mode_frame.grid(row=1, padx=10, pady=10)
        tk.Label(mode_frame, text="MODE: ", bg="#FFFFFF", fg="#000000",
                 font=("Helvetica", "30", "bold")
                 ).grid()

        def gamemode(mode):
            if mode == 1:
                computer_button.configure(relief='sunken')
                user_button.configure(relief='raised')
            else:
                computer_button.configure(relief='raised')
                user_button.configure(relief='sunken')
            self.gamemode = mode

        computer_button = tk.Button(mode_frame, text='COMP PLAY', bg="#FFFFFF", fg="#000000",
                                    font=("Helvetica", "25", "bold"),
                                    command=lambda: gamemode(1)
                                    )
        user_button = tk.Button(mode_frame, text='USER PLAY', bg="#FFFFFF", fg="#000000",
                                font=("Helvetica", "25", "bold"),
                                command=lambda: gamemode(2)
                                )
        computer_button.grid(row=0, column=1, padx=5, pady=5)
        user_button.grid(row=0, column=2, padx=5, pady=5)

        # difficulty select
        self.difficulty = 0
        diff_frame = tk.Frame(start_frame, width=675, height=150, bg="#FFFFFF")
        diff_frame.grid(row=2, padx=10, pady=10)
        tk.Label(diff_frame, text="DIFFICULTY: ", bg="#FFFFFF", fg="#000000",
                 font=("Helvetica", "30", "bold")
                 ).grid()

        def difficulty(diff):
            easy_button.configure(relief='raised')
            hard_button.configure(relief='raised')
            magic_button.configure(relief='raised')

            if diff == 1:
                easy_button.configure(relief='sunken')
            elif diff == 2:
                hard_button.configure(relief='sunken')
            else:
                magic_button.configure(relief='sunken')

            self.difficulty = diff
            print(self.difficulty)

        easy_button = tk.Button(diff_frame, text='EASY', bg="#FFFFFF", fg="#000000",
                                font=("Helvetica", "25", "bold"),
                                command=lambda: difficulty(1)
                                )
        hard_button = tk.Button(diff_frame, text='HARD', bg="#FFFFFF", fg="#000000",
                                font=("Helvetica", "25", "bold"),
                                command=lambda: difficulty(2)
                                )
        magic_button = tk.Button(diff_frame, text='MAGIC', bg="#FFFFFF", fg="#000000",
                                 font=("Helvetica", "25", "bold"),
                                 command=lambda: difficulty(3)
                                 )
        easy_button.grid(row=0, column=1, padx=5, pady=5)
        hard_button.grid(row=0, column=2, padx=5, pady=5)
        magic_button.grid(row=0, column=3, padx=5, pady=5)

        # icon

    def make_GUI(self):

        # make grid
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

                cell_frame = tk.Frame(self.main_grid, width=75, height=75, bg="#FFFFFF")
                cell_frame.grid(row=i, column=j,
                                padx=(xborder, 0.5),
                                pady=(yborder, 0.5)
                                )
                cell_number = tk.Label(self.main_grid, bg="#FFFFFF", fg="#000000",
                                       text=f"{i},{j}",
                                       font=("Helvetica", "20", "bold"),
                                       )
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # make 'scoresheet'
        score_frame_top = tk.Frame(self)
        score_frame_top.place(relx=0.5, y=850, anchor="center")
        for i in range(1, 6):
            cell_score_top = tk.Frame(score_frame_top, width=75, height=75, bg="#f2e8cb")
            cell_score_top.grid(row=0, column=i, padx=10, pady=10)
            cell_number_top = tk.Label(score_frame_top, bg="#f2e8cb", fg="#000000",
                                       text=i,
                                       font=("Helvetica", "30", "bold"),
                                       )
            cell_number_top.grid(row=0, column=i)

        score_frame_bottom = tk.Frame(self)
        score_frame_bottom.place(relx=0.5, y=950, anchor="center")
        for i in range(6, 10):
            cell_score_bottom = tk.Frame(score_frame_bottom, width=75, height=75,
                                         bg="#f2e8cb"
                                         )
            cell_score_bottom.grid(row=1, column=i - 5, padx=10, pady=10)
            cell_number_bottom = tk.Label(score_frame_bottom, bg="#f2e8cb", fg="#000000",
                                          text=i,
                                          font=("Helvetica", "30", "bold"),
                                          )
            cell_number_bottom.grid(row=1, column=i - 5)


Game()
