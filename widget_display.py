from view import View
import tkinter as tk


class WidgetDisplay(tk.Frame, View):

    def __init__(self):
        super().__init__()
        self.grid()
        self.maindiv = tk.Frame(
            self, width=640, height=640, bg="#F0F"
        )
        self.maindiv.grid(padx=72, pady=(72, 120))
        self.mainloop()

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (col:{x}, row:{y}) to {val}.")
