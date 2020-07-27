from MVC.View.view import View


class TextDisplay(View):

    # METHODS ( PUBLIC ):
    def notify(self, x, y, val, /):
        print(f"[Debug] {type(self)}: successfully changed (col:{x}, row:{y}) to {val}.")
