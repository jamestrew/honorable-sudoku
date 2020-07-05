from abc import abstractmethod


class ViewMeta(type):

    def __init__(cls, name, base, attr_dict):
        if not(attr_dict.get("__metaclass__") is ViewMeta) and \
                (name in cls.views):
            cls.views[cls.views.index(name)] = cls
        super().__init__(name, base, attr_dict)


""" Sudoku::VIEW """
class View(metaclass=ViewMeta):
    views = ["TextDisplay", "WidgetDisplay"]  # Required: ORDER(SORTED):ASC

    @abstractmethod
    def notify(self, x, y, val, /): pass


""" ( FWD DECLARATION ) """
class TextDisplay(View): pass
class WidgetDisplay(View): pass
