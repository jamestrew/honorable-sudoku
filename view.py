from abc import ABC, abstractmethod


class View(ABC):
    # METHODS ( PUBLIC ):
    @staticmethod
    def notify(self, x, y, val, /): pass


class WidgetDisplay(View):
    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] successfully changed (col:{x}, row:{y}) to {val}.")
