from resource import *
from view import View
import tkinter as tk


class WidgetDisplay(tk.Frame, View):

    def __init__(self, handle=None):
        super().__init__()
        self.grid()
        self.__request = handle
        self.__accumulator = 0  # temp var to demonstrate link with controller

        self.maindiv = tk.Frame(
            self, width=640, height=640, bg="#F0F"
        )
        self.maindiv.grid(padx=72, pady=(72, 120))

        event_handle = tk.Button(
            self.maindiv, text=self.__accumulator, bg=WHITE, fg=BLACK, font=FONTS[25], padx=72,
            command=self.set_gamemode
        )
        event_handle.grid(row=0, column=1, padx=6, pady=6)

        self.mainloop()

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
