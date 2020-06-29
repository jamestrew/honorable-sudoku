import tkinter as tk


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
        self.make_GUI()

        self.mainloop()

    def make_GUI(self):

        # make grid
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_frame = tk.Frame(self.main_grid, width=75, height=75, bg="#FFFFFF")
                cell_frame.grid(row=i, column=j, padx=border_thickness, pady=border_thickness)
                cell_number = tk.Label(self.main_grid, bg="#FFFFFF", fg="#000000",
                                       text='5',
                                       font=("Helvetica", "30", "bold"),
                                       )
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # make 'scoresheet'
        score_frame_top = tk.Frame(self)
        score_frame_bottom = tk.Frame(self)
        score_frame_top.place(relx=0.5, y=850, anchor="center")
        score_frame_bottom.place(relx=0.5, y=950, anchor="center")
        for i in range(1, 6):
            cell_score_top = tk.Frame(score_frame_top, width=75, height=75, bg="#f2e8cb")
            cell_score_top.grid(row=0, column=i, padx=10, pady=10)
            cell_number_top = tk.Label(score_frame_top, bg="#f2e8cb", fg="#000000",
                                       text=i,
                                       font=("Helvetica", "30", "bold"),
                                       )
            cell_number_top.grid(row=0, column=i)

        for i in range(6, 10):
            cell_score_bottom = tk.Frame(score_frame_bottom, width=75, height=75, bg="#f2e8cb")
            cell_score_bottom.grid(row=1, column=i - 5, padx=10, pady=10)
            cell_number_bottom = tk.Label(score_frame_bottom, bg="#f2e8cb", fg="#000000",
                                          text=i,
                                          font=("Helvetica", "30", "bold"),
                                          )
            cell_number_bottom.grid(row=1, column=i - 5)


Game()
