from resource import *
from widget_display import WidgetDisplay
import tkinter as tk


class Main(tk.Frame, WidgetDisplay):
    __grid = []
    __selection = None

    def __init__(self, root, instance):
        super().__init__(root)
        self.__root_instance = instance

        # background
        bg_frame = tk.Frame(self, width=675, height=675, bg=BLACK, bd=5)
        bg_frame.grid(padx=75, pady=(75, 120))

        # create a blank grid
        for x in range(DIM):
            row = []
            yborder = 5.0 if (x%3==0 and x!=0) else 0.5
            for y in range(DIM):
                xborder = 5.0 if (y%3==0 and y!=0) else 0.5

                cell_frame = tk.Frame(bg_frame, width=75, height=75, bg=WHITE)
                cell_frame.grid(
                    row=x, column=y, padx=(xborder, 0.5), pady=(yborder, 0.5)
                )
                cell_number = tk.Label(bg_frame, bg=WHITE)
                cell_number.grid(row=x, column=y)

                row.append({
                    "frm": cell_frame,
                    "num": cell_number
                })
            self.__grid.append(row)

        def return_to_startup():
            # unbind events
            self.__root_instance.unbind("<Button-1>")
            for i in range(1, 10):
                self.__root_instance.unbind(str(i))

            self.__root_instance.show_frame("Startup")  # return to startup menu

        exit_button = tk.Button(
            self, text='EXIT', bg=WHITE, fg=BLACK, font=CMD_HELVETICA[25],
            command=return_to_startup
        )
        exit_button.place(x=75, y=5)

    def init_board(self):
        """ Populate blank grid with new puzzle """
        self.perm_cells = self.__root_instance.callback(permanent_cell=0)
        for i in range(DIM*DIM):
            value = self.__root_instance.callback(init_iterator=1)
            value = "" if value == 0 else str(value)
            self.__grid[i//DIM][i%DIM]["num"].config(
                bg=WHITE, fg=NUMS, text=value, font=CMD_HELVETICA[20]
            )
        self.play()

    def play(self):
        """ set up binds and init coordinates/value for play """
        self.__root_instance.bind("<Button-1>", self.select_cell)  # binds M1 to click event
        for i in range(1, 10):
            self.__root_instance.bind(str(i), self.try_cell)
        self.__selection = None

    def select_cell(self, event):
        """
        Sets clicked cell coordinate based on event.widget (clicked widget).
        Selected cell is highlighted, previously selected cell de-highlighted.
        """
        # filter out all non-valid cell widgets
        widgetlen = len(str(event.widget))
        if widgetlen < 26: return

        cell_index = str(event.widget)[27:]  # gets the cell widget number
        if not cell_index:  # first cell widget is not numbered
            self.__selection = (0, 0)
        else:
            cell_index = int(cell_index) - 1
            self.__selection = (cell_index//DIM, cell_index%DIM)
        self.change_bg(WHITE)  # De-select cell
        self.change_bg(SELECT, [self.__selection])  # Highlight selected cell

    def try_cell(self, event):
        """
        Given a selected give, enables enter of a number in the cell.
        If the value is valid, update Puzzle. Otherwise show conflicts.
        """
        value = int(event.char)

        # enter value in to the cell initially
        x,y = self.__selection
        if self.__selection and (x, y) not in self.perm_cells:
            self.__grid[x][y]["num"].config(
                fg=BLACK, text=value, font=CMD_HELVETICA[20]
            )
        valid = self.__root_instance.callback(gameboard_update=(x, y, value))

        if isinstance(valid, list):
            self.change_bg(CONF, valid)

    def change_bg(self, color, coordinates=None):
        """
        Changes the color of the background.
        By default, changes the bg color of the entire board.

        Provide coordinates as a list(tuple) to change the bg color of a select cells
        """
        if coordinates is None:
            for i in range(DIM):
                for j in range(DIM):
                    self.__grid[i][j]["frm"].configure(bg=color)
                    self.__grid[i][j]["num"].configure(bg=color)
        else:
            for coord in coordinates:
                i, j = coord
                if coord in self.perm_cells:
                    self.__grid[i][j]["frm"].configure(bg=CONF)  # CONF = CONFLICT
                    self.__grid[i][j]["num"].configure(bg=CONF)
                else:
                    self.__grid[i][j]["frm"].configure(bg=color)
                    self.__grid[i][j]["num"].configure(bg=color)

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (row:{x}, col:{y}) to {val}.")
