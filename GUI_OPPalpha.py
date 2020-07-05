import tkinter as tk
import formats as f


class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (Startup, Main):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

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
                            bg=f.BLACK, bd=5
                            )
        bg_frame.grid(padx=75, pady=(75, 120))
        start_frame = tk.Frame(bg_frame, width=675, height=675, bg=f.WHITE)
        start_frame.grid()

        title = tk.Label(start_frame, text="GAYDOKU", bg=f.WHITE,
                         fg=f.BLACK, font=f.FONTS[55]
                         )
        title.grid(padx=10, pady=10)

        # GAMEMODE SELECT
        mode_frame = tk.Frame(start_frame, bg=f.WHITE)
        mode_frame.grid(row=1, padx=10, pady=10)
        tk.Label(mode_frame, text="MODE: ", bg=f.WHITE, fg=f.BLACK,
                 font=f.FONTS[30]
                 ).grid()

        computer_button = tk.Button(mode_frame, text='COMP PLAY', bg=f.WHITE, fg=f.BLACK,
                                    font=f.FONTS[25]
                                    )
        user_button = tk.Button(mode_frame, text='USER PLAY', bg=f.WHITE, fg=f.BLACK,
                                font=f.FONTS[25]
                                )
        computer_button.grid(row=0, column=1, padx=5, pady=5)
        user_button.grid(row=0, column=2, padx=5, pady=5)

        play_button = tk.Button(start_frame, text='PLAY', bg=f.WHITE, fg=f.BLACK,
                                font=f.FONTS[25],
                                command=lambda: controller.show_frame("Main")
                                )
        play_button.grid()


class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        bg_frame = tk.Frame(self, width=675, height=675,
                            bg=f.BLACK, bd=5
                            )
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

                cell_frame = tk.Frame(bg_frame, width=75, height=75, bg=f.WHITE)
                cell_frame.grid(row=i, column=j,
                                padx=(xborder, 0.5),
                                pady=(yborder, 0.5)
                                )
                cell_number = tk.Label(bg_frame, bg=f.WHITE, fg="#0A3095",
                                       text=i,
                                       font=f.FONTS[20],
                                       )
                cell_number.grid(row=i, column=j)
                cell_data = {"number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        exit_button = tk.Button(self, text='EXIT', bg=f.WHITE, fg=f.BLACK,
                                font=f.FONTS[25],
                                command=lambda: controller.show_frame("Startup")
                                )
        exit_button.place(x=75, y=5)


if __name__ == "__main__":
    app = Game()
    app.mainloop()
